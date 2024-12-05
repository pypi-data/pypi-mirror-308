import sys
import os
import requests
import json
import urllib.parse
from requests.auth import HTTPBasicAuth
from schemon.common import ReturnWithMessage


class ADOApiConfig:
    __slots__ = ["url_base", "auth", "headers"]


def init_ado_api_config(org=None, project=None, pat=None) -> ADOApiConfig:
    """prepare common config for ADO API"""
    org = os.getenv("ADO_ORG", org)
    project = os.getenv("ADO_PROJECT", project)
    pat = os.getenv("ADO_PAT", pat)
    encoded_organization = urllib.parse.quote(org)
    encoded_project = urllib.parse.quote(project)
    url_base = f"https://dev.azure.com/{encoded_organization}/{encoded_project}/_apis"
    ado_api_config = ADOApiConfig()
    ado_api_config.url_base = url_base
    ado_api_config.auth = HTTPBasicAuth("", pat)
    ado_api_config.headers = {"Content-Type": "application/json"}
    return ado_api_config


def create_pr_thread_ado(
        repository_id,
        pull_request_id,
        content,
        comment_type="text",
        status="active",
):
    """
    Creates a thread in a pull request on Azure DevOps.

    Args:
        repository_id (str): The ID of the repository.
        pull_request_id (int): The ID of the pull request.
        content (str): The content of the comment.
        comment_type (str): The type of the comment. Defaults to 'text'.
        status (str): The status of the comment thread. Defaults to 'active'.

    Returns:
        dict: The response from the Azure DevOps API.
    """
    ado_api_config = init_ado_api_config()
    url = f"{ado_api_config.url_base}/git/repositories/{repository_id}/pullRequests/{pull_request_id}/threads?api-version=7.1-preview.1"
    data = {
        "comments": [{"content": content, "commentType": comment_type}],
        "status": status,
    }
    response = requests.post(url, headers=ado_api_config.headers, data=json.dumps(data), auth=ado_api_config.auth)

    if response.status_code == 200:
        print("Thread created successfully.")
    else:
        print(f"Failed to create thread. Status code: {response.status_code}")
        sys.exit(1)

    return response.json()


def requeue_pr_pipeline_ado(pr_id) -> ReturnWithMessage:
    api_return = ReturnWithMessage()
    try:
        ado_api_config = init_ado_api_config()
        pr_url = f"{ado_api_config.url_base}/git/pullrequests/{pr_id}?api-version=7.1-preview.1"
        response = requests.get(pr_url, headers=ado_api_config.headers, auth=ado_api_config.auth)
        if response.status_code != 200:
            raise Exception(f"Failed to get PR details, status code: {response.status_code}, response: {response.text}")

        try:
            project_id = response.json()["repository"]["project"]["id"]
        except ValueError as json_error:
            raise Exception(f"Failed to parse JSON: {json_error}. Response content: {response.text}")

        artifact_id = f"vstfs:///CodeReview/CodeReviewId/{project_id}/{pr_id}"
        policy_evaluation_url = f"{ado_api_config.url_base}/policy/evaluations?artifactId={artifact_id}&api-version=7.0-preview.1"
        response = requests.get(policy_evaluation_url, headers=ado_api_config.headers, auth=ado_api_config.auth)
        evaluation = response.json()['value'][0]
        requeue_url = f"{ado_api_config.url_base}/policy/evaluations/{evaluation['evaluationId']}?api-version=7.0-preview.1"
        response = requests.patch(requeue_url, headers=ado_api_config.headers, auth=ado_api_config.auth)
        if response.status_code == 200:
            api_return.success = True
            api_return.message = f"Pipeline requeued successfully for PR #{pr_id}."
        else:
            raise Exception(f"Requeue response code: {response.status_code}")
    except Exception as e:
        api_return.success = False
        api_return.message = f"Failed to requeue pipeline for PR #{pr_id}: {e}"
    return api_return
