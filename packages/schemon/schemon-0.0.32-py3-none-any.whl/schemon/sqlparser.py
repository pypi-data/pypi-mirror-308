from __future__ import annotations
from schemon.antlr.spark.SqlBaseParser import SqlBaseParser
from schemon.antlr.spark.SqlBaseLexer import SqlBaseLexer
from antlr4.xpath.XPath import XPath
from antlr4 import InputStream, CommonTokenStream, ParserRuleContext
from schemon.common import logger, generic_repr


class Column:
    """
    Represents a column in a query, e.g. t1.col1

    Attributes:
        table_alias (str): Table alias of the column, e.g. t1 in t1.col1.
        field (str): Field name of the column, e.g. col1 in t1.col1.
        query_id (str): ID of the select query that the column in, for debug use.
        table_names (list[str]): The actual table names corresponding to the table alias. Note that there may be
                                 multiple table names for an alias if the SQL is not specific enough.
    """
    __slots__ = ('table_alias', 'field', 'query_id', 'table_names')

    def __init__(self, table_alias: str = None, field: str = None, query_id: str = None, table_names: list[str] = None):
        self.table_alias = table_alias
        self.field = field
        self.query_id = query_id
        self.table_names = table_names

    def __eq__(self, other):
        if not isinstance(other, Column):
            return NotImplemented
        return (self.table_alias == other.table_alias and
                self.field == other.field and
                self.query_id == other.query_id)

    def __repr__(self):
        return generic_repr(self)

    def __hash__(self):
        return hash((self.table_alias, self.field, self.query_id))


class Table:
    """
    Represents a table or subquery in a SQL, usually the entity after "from" / "join" / ...

    Attributes:
        table_name (str): Actual table name, None when the "table" is a subquery.
        alias (str): Table alias, e.g. t1 in t1.col1.
        query_id (str): ID of the select query that the table or subquery in, for debug use.
    """
    __slots__ = ('table_name', 'alias', 'query_id')

    def __init__(self, table_name: str = None, alias: str = None, query_id: str = None):
        self.table_name = table_name
        self.alias = alias
        self.query_id = query_id

    def __repr__(self):
        return generic_repr(self)

    def __eq__(self, other):
        if not isinstance(other, Table):
            return NotImplemented
        return (self.table_name == other.table_name and
                self.alias == other.alias and
                self.query_id == other.query_id)

    def __hash__(self):
        return hash((self.table_name, self.alias, self.query_id))


class SqlParser:
    """
    Sql parser to get the dependency info

    Attributes:
        sql (str): The sql statement to parse.
        dep_tables (list[Table]): All the tables that the SQL depends on.
        dep_columns (list[Column]): All the columns that the SQL depends on.
    """
    __slots__ = ('sql', 'dep_tables', 'dep_columns', 'select_expressions', '__parser',
                 '__select_clause_not_found')

    def __init__(self, sql):
        self.sql = sql
        self.dep_tables = []
        self.dep_columns = []
        self.select_expressions = []
        self.__parser = None
        self.__select_clause_not_found = True
        self.__parse_sql()

    def __parse_sql(self) -> None:
        """sql parse entry"""
        lexer = SqlBaseLexer(InputStream(self.__hide_braces(self.sql)))
        tokens = CommonTokenStream(lexer)
        self.__parser = SqlBaseParser(tokens)
        entry = self.__parser.singleStatement()
        self.__walk_tree(entry, None)
        self.__post_process()

    BRACE1 = "__BRACE_START__"
    BRACE2 = "__BRACE_END__"

    def __hide_braces(self, s: str) -> str:
        """replace braces to other strings to pass the parser validation"""
        return s.replace("{", self.BRACE1).replace("}", self.BRACE2) if s else None

    def __restore_braces(self, s) -> str:
        """restore braces to get the original sql"""
        return s.replace(self.BRACE1, "{").replace(self.BRACE2, "}") if s else None

    def __find_dependencies(self, node: ParserRuleContext, query_id: str) -> bool:
        """find dependent tables and columns from current node"""
        if isinstance(node, SqlBaseParser.RelationPrimaryContext):  # found tables
            table = Table()
            # find table name
            table_name_node = self.__find_one_xpath(node, "/relationPrimary/identifierReference")
            if table_name_node:
                table.table_name = table_name_node.getText()
            table.query_id = self.__get_query_id(node)
            # find table alias
            alias_node = self.__find_one_xpath(node, "//tableAlias/strictIdentifier")
            if alias_node:
                table.alias = alias_node.getText()
            self.dep_tables.append(table)
        elif isinstance(node, (
                SqlBaseParser.DereferenceContext, SqlBaseParser.ColumnReferenceContext,
                SqlBaseParser.StarContext)):  # column
            column = Column()
            column.query_id = query_id
            if isinstance(node, SqlBaseParser.DereferenceContext):  # column with table alias
                column.table_alias = node.base.getText()
                column.field = node.fieldName.getText()
            elif isinstance(node, SqlBaseParser.ColumnReferenceContext):  # column without table alias
                column.field = node.getText()
            elif isinstance(node, SqlBaseParser.StarContext):  # ASTERISK
                column.field = "*"
                alias_node = self.__find_one_xpath(node, "/primaryExpression/qualifiedName")
                if alias_node:
                    column.table_alias = alias_node.getText()
            self.dep_columns.append(column)
        elif self.__select_clause_not_found and isinstance(node, SqlBaseParser.SelectClauseContext):
            # get expressions in main select clause
            self.__select_clause_not_found = False
            expressions = XPath.findAll(node, "/selectClause/namedExpressionSeq/namedExpression/expression",
                                        self.__parser)
            for i, expression in enumerate(expressions):
                expr_str = self.__get_full_text(expression)
                self.select_expressions.append(expr_str)
        # to avoid duplicate parsing, do not go deeper if current node is dereference
        return not isinstance(node, SqlBaseParser.DereferenceContext)

    def __get_full_text(self, ctx: ParserRuleContext) -> str:
        """get full text with interval from antlr context"""
        token_source = ctx.start.getTokenSource()
        input_stream = token_source.inputStream
        start, stop = ctx.start.start, ctx.stop.stop
        return input_stream.getText(start, stop)

    def __get_node_id(self, node: ParserRuleContext) -> str:
        """get context node id"""
        return str(hash(node))

    def __get_query_id(self, node: ParserRuleContext) -> str | None:
        """get queryPrimary context node id of this node, or None if not found"""
        cur_node = node
        while True:
            parent_node = cur_node.parentCtx
            if parent_node is None:
                break
            if isinstance(parent_node, SqlBaseParser.QueryPrimaryContext):
                return self.__get_node_id(parent_node)
            cur_node = parent_node
        return None

    def __walk_tree(self, node, query_id) -> None:
        """walk through the syntax tree of the parsed sql recursively to get the dependency info"""
        go_deeper = self.__find_dependencies(node, query_id)
        if go_deeper:
            next_query_id = query_id
            if isinstance(node, SqlBaseParser.QueryPrimaryContext):
                next_query_id = self.__get_node_id(node)
            n = node.getChildCount()
            if n > 0:
                for i in range(n):
                    self.__walk_tree(node.getChild(i), next_query_id)

    def __post_process(self) -> None:
        """post process after sql parsing"""
        # restore braces of table names
        for table in self.dep_tables:
            table.table_name = self.__restore_braces(table.table_name)
        # set table_names for allColumns by queryId, tableAlias
        for column in self.dep_columns:
            tables = [t for t in self.dep_tables if t.table_name and t.query_id == column.query_id]
            if column.table_alias:
                tables = [t for t in tables if column.table_alias == t.alias]
            column.table_names = [t.table_name for t in tables]
        # remove tables of sub queries
        self.dep_tables = [t for t in self.dep_tables if t.table_name]
        # remove duplicate, and columns of sub queries
        self.dep_columns = list(dict.fromkeys(sorted(self.dep_columns, key=lambda d: ','.join(d.table_names))))

    def __find_one_xpath(self, node: ParserRuleContext, xpath: str) -> ParserRuleContext:
        """find context nodes with xpath string from current node, return first if multiple found"""
        first_found = None
        elements = XPath.findAll(node, xpath, self.__parser)
        if len(elements) > 1:
            logger.warning(f"more than 1 {xpath} found in node: {self.__get_full_text(node)}")
        if elements:
            first_found = elements[0]
        return first_found
