from typing import Any

import requests


def get_api_output_in_standard_format(
    data: Any = None,
    message: str = None,
    log: Any = None,
):
    return {"data": data, "message": message, "log": log}


def make_request_json_output(
    method,
    base_url,
    endpoint,
    data=None,
    params=None,
    headers=None,
):
    try:
        url = f"{base_url}/{endpoint}"
        if headers:
            headers = {key.replace("_", "-"): value for key, value in headers.items()}
        response = requests.request(
            method,
            url,
            json=data,
            params=params,
            headers=headers,
        )
        response.raise_for_status()
        return response.json()
    except Exception:
        raise
