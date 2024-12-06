import requests
from scientiflow_cli.cli.auth_utils import getAuthToken

API_BASE = "https://www.backend.scientiflow.com/api"

def update_terminal_output(project_job_id: int, terminal_output: str):
    headers = { "Authorization": f"Bearer {getAuthToken()}"}
    body = {"project_job_id": project_job_id, "terminal_output": terminal_output}
    res = requests.post(f"{API_BASE}/agent-application/update-terminal-output", headers=headers, data=body)
    print("[+] Terminal output updated successfully.")