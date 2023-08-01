import base64
import os
import mimetypes
import json


class Utils:
    @staticmethod
    def file_to_base64(file_path):
        with open(file_path, 'rb') as file:
            base64_data = base64.b64encode(file.read()).decode('utf-8')
        return base64_data

    @staticmethod
    def construct_file_upload_request(file_path, destination_url):
        with open(file_path, 'rb') as file:
            file_content = base64.b64encode(file.read()).decode('utf-8')

        file_name = os.path.basename(file_path)
        file_type, _ = mimetypes.guess_type(file_name)

        request_data = {
            "file-content": file_content,
            "file-name": file_name,
            "destination-url": destination_url
        }

        if file_type:
            request_data["file-type"] = file_type

        return request_data

    @staticmethod
    def update_metadata(server_path, content_hash, version):
        metadata_path = os.path.join(server_path, 'metadata.json')
        metadata = {}
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)

        # file_metadata = metadata.get(file_name, {})
        metadata[content_hash] = version

        with open(metadata_path, 'w') as f:
            json.dump(metadata, f)

    @staticmethod
    def get_next_version(server_path):
        metadata_path = os.path.join(server_path, 'metadata.json')
        metadata = {}
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)

        max_version = max(metadata.values(), default=-1)
        next_version = max_version + 1
        return next_version


file_upload_request = Utils.construct_file_upload_request(
    '/Users/sohantandle/Documents/Personal/Jobs/DCU_LinkedIn_Tips.pdf',
    '/Users/sohantandle/Documents/Personal/Jobs/Companies/Propylon/Assignment/file_manager')
print(file_upload_request)
#%%
