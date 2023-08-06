import argparse
import os
import base64
import requests
import mimetypes
import json


def file_upload_call(token, source_path, target_path):
    _url = f'http://127.0.0.1:9000/file-manager/file-upload/'
    headers = {
        'Authorization': f'Token {token}',  # Replace with your actual token
        'Content-Type': 'application/json'
    }

    with open(source_path, 'rb') as file:
        file_content = base64.b64encode(file.read()).decode('utf-8')
    file_name = os.path.basename(source_path)
    file_type, _ = mimetypes.guess_type(file_name)

    body = {
        'file-content': file_content,
        'file-name': file_name,
        'file-type': file_type,
        'target-path': target_path
    }

    _response = requests.post(_url, json=body, headers=headers)
    response_data = _response.json()
    pretty_response = json.dumps(response_data, indent=4)

    print(pretty_response)


def main():
    parser = argparse.ArgumentParser(description='Upload a file on to the server using a REST API')
    parser.add_argument('--token', required=True, help='Authentication token')
    parser.add_argument('--source-path', required=True, help='Local path of the file to upload')
    parser.add_argument('--target-path', required=True, help='Server path to store the file')

    args = parser.parse_args()

    file_upload_call(args.token, args.source_path, args.target_path)


if __name__ == '__main__':
    main()
