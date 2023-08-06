import requests
import argparse
import base64
import os
import json


def file_retrieve_call(token, source_path, version, target_path):
    _source_path = source_path.replace('/', '%2F')
    _url = f'http://127.0.0.1:9000/file-manager/file-retrieve/?source-path={_source_path}&version={version}'
    headers = {
        'Authorization': f'Token {token}',  # Replace with your actual token
        'Content-Type': 'application/json'
    }

    _response = requests.get(_url, headers=headers)

    response_data = _response.json()
    pretty_response = json.dumps(response_data, indent=4)
    file_content = response_data.get('file-content', '')
    file_name = response_data.get('file-name', '')
    binary_data = base64.b64decode(file_content)
    file_path = os.path.join(target_path, file_name)

    with open(file_path, 'wb') as f:
        f.write(binary_data)

    print(pretty_response)


def main():
    parser = argparse.ArgumentParser(description='Retrieve a file from the server using a REST API')
    parser.add_argument('--token', required=True, help='Authentication token')
    parser.add_argument('--source-path', required=True, help='Path of the file on the server')
    parser.add_argument('--version', required=True, type=int, help='Version of the file')
    parser.add_argument('--target-path', required=True, help='Local path to store the file')

    args = parser.parse_args()

    file_retrieve_call(args.token, args.source_path, args.version, args.target_path)


if __name__ == '__main__':
    main()
