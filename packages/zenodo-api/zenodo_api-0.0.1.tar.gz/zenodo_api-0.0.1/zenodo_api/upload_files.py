import requests
import os
import json


def call_depositions():
    ACCESS_TOKEN = load_access_token()
    empty_upload = requests.get(
        # /api/deposit/depositions/:id/files/:file_id
        "https://sandbox.zenodo.org/api/deposit/depositions",
        [("access_token", ACCESS_TOKEN), ("size", 200), ("all_versions", "true")],
    )
    return empty_upload


def load_access_token():
    return os.environ.get("ACCESS_TOKEN")


def create_empty_upload():
    headers = {"Content-Type": "application/json"}
    params = {"access_token": load_access_token()}
    r = requests.post(
        "https://sandbox.zenodo.org/api/deposit/depositions",
        params=params,
        json={},
        headers=headers,
    )
    return r


def upload_new_file(file_path):
    params = {"access_token": load_access_token()}
    empty_upload = create_empty_upload()

    bucket_url = empty_upload.json()["links"]["bucket"]
    filename = "tests_file.txt"
    path = f"tests/data/{filename}"

    response_upload = upload_file(params, bucket_url, filename, path)
    return response_upload


def upload_file(params, bucket_url, filename, path):
    with open(path, "rb") as file_content:
        response_upload = requests.put(
            f"{bucket_url}/{filename}",
            data=file_content,
            params=params,
        )

    return response_upload


def upload_metadata(data_dict):
    empty_upload = create_empty_upload()
    deposition_id = empty_upload.json()["id"]
    headers = {"Content-Type": "application/json"}
    r = requests.put(
        f"https://sandbox.zenodo.org/api/deposit/depositions/{deposition_id}",
        params={"access_token": load_access_token()},
        data=json.dumps(data_dict),
        headers=headers,
    )
    return r
