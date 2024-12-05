import secrets
from nicegui import ui
from schemon.env import loadenv_dev
from starlette.requests import Request

# Load environment variables
loadenv_dev()

# Import modules after loading environment
from report import report
from schemon import dao

# No need for session middleware anymore
secret_key = secrets.token_hex(32)


@ui.page("/")
def index():
    # Define the table columns
    columns = [
        {"name": "pr_id", "label": "PR ID", "field": "pr_id", "align": "left"},
        {"name": "status", "label": "Status", "field": "status", "align": "left"},
    ]

    # Fetch validation results, including result_id, repo_id, and pr_id
    results = dao.get_validation_results()

    # Process results to display in the table
    for r in results:
        r.status = r.status.report_status_text

    # Convert results to a list of dictionaries for the table rows
    rows = [d.to_dict() for d in results]

    # Display a label for user instruction
    ui.label("Click on PR ID to view the reports")

    # Create the table with columns and rows
    table = ui.table(columns=columns, rows=rows, row_key="pr_id")

    # Add a custom slot to handle the click on PR ID and pass the variables via URL
    table.add_slot(
        "body-cell-pr_id",
        """
        <q-td :props="props">
            <a style="color: blue;" :href="'/report/' + props.row.result_id + '?repo_id=' + props.row.repo_id + '&pr_id=' + props.row.pr_id">
                {{ props.value }}
            </a>
        </q-td>
        """,
    )


@ui.page("/report/{report_id}")
async def report_(request: Request, report_id: str):
    # Retrieve `repo_id` and `pr_id` from URL query parameters
    repo_id = request.query_params.get("repo_id")
    pr_id = request.query_params.get("pr_id")

    # Check if the query parameters exist, otherwise show an error
    if not repo_id or not pr_id:
        return ui.label("Error: Missing repo_id or pr_id in query parameters.")

    if repo_id == "null":
        repo_id = None

    # Pass the retrieved values to the report function
    return report(pr_id, repo_id)


# Start the web application
ui.run(title="schemon webapp", port=8020)
