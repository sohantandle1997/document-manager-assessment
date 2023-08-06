import argparse
import requests
import json


def file_structure_call(token):
    _url = f'http://127.0.0.1:9000/file-manager/file-structure/'
    headers = {
        'Authorization': f'Token {token}',  # Replace with your actual token
        'Content-Type': 'application/json'
    }

    _response = requests.get(_url, headers=headers)

    response_data = _response.json()
    pretty_response = json.dumps(response_data, indent=4)

    print(pretty_response)


def main():
    parser = argparse.ArgumentParser(description='View the folders and files on the server using a REST API')
    parser.add_argument('--token', required=True, help='Authentication token')

    args = parser.parse_args()

    file_structure_call(args.token)


if __name__ == '__main__':
    main()
