import base64
import hashlib
import mimetypes
import os
import json

BASE_SERVER_PATH = '/Users/sohantandle/Documents/Personal/Jobs/Companies/Propylon/Assignment/document-manager-assessment/propylon_document_manager/file_versions/my_file_manager'


class FileHandler:
    def __init__(self):
        pass


class FileUploadHandler(FileHandler):

    def __init__(self, file_content, file_name, file_type, target_path):
        super().__init__()
        self.target_path = target_path
        self.file_name = file_name
        self.file_type = file_type
        self.file_content = file_content
        self.server_path = os.path.join(BASE_SERVER_PATH, self.target_path, self.file_name)
        self.metadata_path = os.path.join(self.server_path, 'metadata.json')
        self.metadata = {}
        self.read_metadata()
        self.file_version = 0
        self.generate_file_version()

    def upload_file(self):
        try:
            # Decode base64 file content to binary
            binary_data = base64.b64decode(self.file_content)

            # Calculate the content hash (unique identifier) for the file's content
            content_hash = hashlib.sha256(binary_data).hexdigest()

            # Get the file extension from the provided file type
            file_extension = mimetypes.guess_extension(self.file_type)

            if not os.path.exists(BASE_SERVER_PATH):
                os.mkdir(BASE_SERVER_PATH)

            # Create the server path for the destination URL using the content hash
            server_path = os.path.join(BASE_SERVER_PATH, self.target_path, self.file_name)

            # Create the nested folder structure (and any missing intermediate directories)
            os.makedirs(server_path, exist_ok=True)

            # Get the latest version number for the file from the metadata
            self.generate_file_version()

            # Construct the file name using the content hash
            hash_file_name = f"{content_hash}{file_extension}"

            # Save the file to the server's storage
            file_path = os.path.join(server_path, hash_file_name)
            with open(file_path, 'wb') as f:
                f.write(binary_data)

            # Update the metadata with the new version number
            self.update_metadata(content_hash)

            return True

        except Exception as e:
            return False

    def generate_file_version(self):
        """
        Method to generate next version of the file
        :return:
        """
        max_version = max(self.metadata.values(), default=-1)
        self.file_version = max_version + 1

    def read_metadata(self):
        """
        Method to read the metadata file
        :return:
        """
        if os.path.exists(self.metadata_path):
            with open(self.metadata_path, 'r') as f:
                self.metadata = json.load(f)

    def update_metadata(self, content_hash):
        """
        Method to update metadata file mapping the version and the hash
        :param content_hash:
        :return:
        """
        self.metadata[content_hash] = self.file_version

        with open(self.metadata_path, 'w') as f:
            json.dump(self.metadata, f)

