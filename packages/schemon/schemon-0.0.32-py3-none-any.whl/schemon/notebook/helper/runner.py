import os
import yaml
from schemon_python_client.spark.helper.fs import list_folders_in_directory
from pyspark.sql import SparkSession


def parse_spark_notebook_config(spark: SparkSession, cwd: str, job: str, stage: str, config_type: str = "yaml"):
    """Parse a YAML file to retrieve the spark_notebook_config."""
    if config_type == "yaml":        
        file_path = f"{cwd}/{job}/{stage}/spark_notebook_config.yaml"
        with open(file_path, "r") as file:
            config = yaml.safe_load(file)
            return config.get("spark_notebook_config", {})
    elif config_type == "db":
        notebook_config_df = spark.sql(f"SELECT value FROM demo.spark_notebook_config WHERE job = '{job}' AND stage = '{stage}'").collect()
        config_value = notebook_config_df[0]["value"]
        config = yaml.safe_load(config_value)
        return config.get("spark_notebook_config", {})
    return {}



def build_dependency_graph(spark: SparkSession, stages: list, job: str, cwd: str, config_type: str = "yaml"):
    """Build a dependency graph for sorting stages based on spark_notebook_config."""
    dependency_map = {}
    stage_to_name_map = {}

    for stage in stages:
        config = parse_spark_notebook_config(spark, cwd, job, stage, config_type)
        name = config.get("name")
        dependent_on = config.get("dependent_on") or []
        if isinstance(dependent_on, str):
            dependent_on = [dependent_on]  # Ensure dependent_on is always a list
        if name:
            dependency_map[name] = dependent_on
            stage_to_name_map[name] = (
                stage  # Map the notebook config name to the stage (folder)
            )

    return dependency_map, stage_to_name_map


def topological_sort(dependency_map):
    """Sort stages based on dependencies using topological sorting."""
    sorted_names = []
    visited = set()
    temp_marked = set()

    def visit(stage_name):
        if stage_name in visited:
            return
        if stage_name in temp_marked:
            raise ValueError(f"Circular dependency detected for stage: {stage_name}")
        temp_marked.add(stage_name)

        # Visit all dependencies first
        for dep in dependency_map.get(stage_name, []):
            if dep not in visited:
                visit(dep)

        temp_marked.remove(stage_name)
        visited.add(stage_name)
        sorted_names.append(stage_name)

    # Visit stages in topological order
    for stage_name in dependency_map.keys():
        if stage_name not in visited:
            visit(stage_name)

    return sorted_names


def sort_stages_by_dependency(spark: SparkSession, job: str, cwd: str, config_type: str = "yaml"):
    """Sort stages based on the 'dependent_on' field of spark_notebook_config."""
    if config_type == "yaml":
        dir_path = f"{cwd}/{job}"
        stages = list_folders_in_directory(dir_path)
    elif config_type == "db":
        #TODO: move it to the schemon_repo
        stage_df = spark.sql(f"SELECT DISTINCT stage FROM demo.spark_config").collect()
        stages = [row.stage for row in stage_df]        
    else:
        raise ValueError(f"Invalid config_type: {config_type}")
    dependency_map, stage_to_name_map = build_dependency_graph(spark, stages, job, cwd, config_type)

    sorted_names = topological_sort(dependency_map)

    # Return the stages (folder names) based on the sorted notebook names
    sorted_stages = [stage_to_name_map[name] for name in sorted_names]

    return sorted_stages


def get_config_from_widget(input_dict):
    import re

    result = {}

    for key, value in input_dict.items():
        # Split the key by dots
        parts = key.split(".")

        # Handle 'spark_config'
        if parts[0] == "spark_config":
            if len(parts) >= 3:
                nested_key = parts[1]
                remaining_key = ".".join(parts[2:])
                if "spark_config" not in result:
                    result["spark_config"] = {}
                if nested_key not in result["spark_config"]:
                    result["spark_config"][nested_key] = {}
                result["spark_config"][nested_key][remaining_key] = value

        # Handle 'spark_notebook_config'
        elif parts[0] == "spark_notebook_config":
            if len(parts) >= 2:
                final_key = parts[1]
                if "spark_notebook_config" not in result:
                    result["spark_notebook_config"] = {}
                result["spark_notebook_config"][final_key] = value

        # Handle 'spark_section_configs'
        elif parts[0].startswith("spark_section_configs"):
            # Extract the index from the first part like 'spark_section_configs[0]'
            section_match = re.match(r"spark_section_configs\[(\d+)\]", parts[0])
            if section_match:
                section_index = int(section_match.group(1))

                # Ensure the structure for 'spark_section_configs' is a list
                if "spark_section_configs" not in result:
                    result["spark_section_configs"] = []

                # Ensure the list has enough items up to the current index
                while len(result["spark_section_configs"]) <= section_index:
                    result["spark_section_configs"].append({})

                # Handle the rest of the key
                if len(parts) >= 3:
                    # Second token becomes nested key (e.g., 'source')
                    nested_key = parts[1]
                    remaining_key = ".".join(parts[2:])

                    # Ensure nested structure exists
                    if nested_key not in result["spark_section_configs"][section_index]:
                        result["spark_section_configs"][section_index][nested_key] = {}

                    # Assign the value to the final key
                    result["spark_section_configs"][section_index][nested_key][
                        remaining_key
                    ] = value

    return result


if __name__ == "__main__":
    cwd = f"{os.getcwd()}/src/schemon/runner/spark_runner_config"
    sorted_stages = sort_stages_by_dependency(cwd)
    print(sorted_stages)
