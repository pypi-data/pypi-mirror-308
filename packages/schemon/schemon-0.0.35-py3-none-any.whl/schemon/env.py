import os
from dotenv import load_dotenv

# Define a global variable for storing the environment value
env = None


def detect_ci_environment():
    """
    Detects which CI/CD environment the script is running in.
    Returns a string representing the CI/CD platform or 'local' if none is detected.
    """
    if os.getenv("SYSTEM_TEAMPROJECT"):  # Azure Pipelines
        return "azure_pipelines"
    elif os.getenv("GITHUB_ACTIONS"):  # GitHub Actions
        return "github_actions"
    elif os.getenv("CI") == "true" and os.getenv("GITLAB_CI"):  # GitLab CI
        return "gitlab_ci"
    elif os.getenv("JENKINS_URL"):  # Jenkins
        return "jenkins"
    elif os.getenv("CIRCLECI") == "true":  # CircleCI
        return "circleci"
    elif os.getenv("TRAVIS") == "true":  # Travis CI
        return "travis_ci"
    else:
        return "local"  # Default to local if no CI environment is detected


def loadenv(selected_env: str = None):
    """
    Load the environment variables based on the selected environment.

    Args:
        selected_env (str): The environment to load (e.g., 'local', 'dev', 'prod').

    Raises:
        FileNotFoundError: If the .env file for the specified environment does not exist.
    """
    ci_environment = detect_ci_environment()

    if ci_environment == "local":
        global env

        # Handle the logic for when global env and selected_env are None
        if env is None and selected_env is None:
            raise ValueError(
                "No environment specified. Both global 'env' and 'selected_env' are None."
            )

        # Assign selected_env to global env if global env is None and selected_env is provided
        if env is None and selected_env is not None:
            env = selected_env

        # Construct the path to the environment-specific .env file
        env_file = f".env.{env}"

        # if not os.path.exists(env_file):
        #     raise FileNotFoundError(f"Environment file '{env_file}' does not exist.")

        # Load environment variables from the environment-specific .env file
        load_dotenv(env_file)


def loadenv_dev():
    global env
    env = "dev"

    env_file = f".env.{env}"

    # if not os.path.exists(env_file):
    #     raise FileNotFoundError(f"Environment file '{env_file}' does not exist.")

    # Load environment variables from the environment-specific .env file
    load_dotenv(env_file)
