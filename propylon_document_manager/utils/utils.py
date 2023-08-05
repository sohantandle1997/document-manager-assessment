import base64
import os
import mimetypes
import json
from datetime import datetime


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

    @staticmethod
    def list_files_and_folders_recursive(path):
        try:
            contents = os.listdir(path)
            # files = [item for item in contents if os.path.isfile(os.path.join(path, item))]
            folders = [item for item in contents if os.path.isdir(os.path.join(path, item))]

            # response = {"path": path, "files": files, "folders": folders}
            response = {}

            for folder in folders:
                folder_path = os.path.join(path, folder)
                response[folder] = Utils.list_files_and_folders_recursive(folder_path)
                if os.path.exists(os.path.join(folder_path, 'metadata.json')):
                    metadata = Utils.read_metadata(os.path.join(folder_path, 'metadata.json'))
                    for hash_content, version in metadata.items():
                        response[folder][f'version-{version}'] = \
                            Utils.get_last_modified(os.path.exists(os.path.join(folder_path, hash_content)))

            return response
        except FileNotFoundError:
            return None

    @staticmethod
    def read_metadata(path):
        """
        Method to read the metadata file
        :return:
        """
        metadata = {}
        if os.path.exists(path):
            with open(path, 'r') as f:
                metadata = json.load(f)
        return metadata

    @staticmethod
    def get_last_modified(file_path):
        try:
            print(file_path)
            # Get the last modification time in seconds since the epoch
            mtime = os.path.getmtime(file_path)

            # Convert the timestamp to a human-readable format
            last_modified = datetime.fromtimestamp(mtime)
            formatted_last_modified = last_modified.strftime("%m-%d-%Y %H:%M:%S")

            return formatted_last_modified
        except FileNotFoundError:
            return None

res = Utils.list_files_and_folders_recursive('/Users/sohantandle/Documents/Personal/Jobs/Companies/Propylon/Assignment/document-manager-assessment/propylon_document_manager/file_versions/user_repo')
print(res)



#%%

#%%
