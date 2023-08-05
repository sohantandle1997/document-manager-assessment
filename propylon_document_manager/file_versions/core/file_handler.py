import base64
import hashlib
import mimetypes
import os
import json
import datetime

BASE_SERVER_PATH = '/Users/sohantandle/Documents/Personal/Jobs/Companies/Propylon/Assignment/document-manager-assessment/propylon_document_manager/file_versions/user_repo'


class FileHandler:
    def __init__(self, user):
        self.user = user
        self.user_repo_path = os.path.join(BASE_SERVER_PATH, self.user)


class FileUploadHandler(FileHandler):

    def __init__(self, user, file_content, file_name, file_type, target_path):
        super().__init__(user)
        self.target_path = target_path
        self.file_name = file_name
        self.file_type = file_type
        self.file_content = file_content
        self.server_path = os.path.join(self.user_repo_path, self.target_path, self.file_name)
        self.metadata_path = os.path.join(self.server_path, 'metadata.json')
        self.metadata = {}
        self.read_metadata()
        self.file_version = 0

    def upload_file(self):
        try:
            # Decode base64 file content to binary
            binary_data = base64.b64decode(self.file_content)

            # Calculate the content hash (unique identifier) for the file's content
            content_hash = hashlib.sha256(binary_data).hexdigest()

            # Get the file extension from the provided file type
            file_extension = mimetypes.guess_extension(self.file_type)

            # Create the server path for the destination URL using the content hash
            # server_path = os.path.join(self.server_path, self.file_name)

            # Create the nested folder structure (and any missing intermediate directories)
            os.makedirs(self.server_path, exist_ok=True)

            # Get the latest version number for the file from the metadata
            self.generate_file_version(content_hash)

            # Construct the file name using the content hash
            hash_file_name = f"{content_hash}{file_extension}"

            # Save the file to the server's storage
            file_path = os.path.join(self.server_path, hash_file_name)
            with open(file_path, 'wb') as f:
                f.write(binary_data)

            # Update the metadata with the new version number
            self.update_metadata(content_hash)

            return True

        except Exception as e:
            return False

    def generate_file_version(self, hash_content):
        """
        Method to generate next version of the file
        :return:
        """
        max_version = max(self.metadata.values(), default=-1)
        # self.file_version = self.metadata.get(hash_content, default=max_version + 1)
        self.file_version = max_version + 1
        if hash_content in self.metadata:
            self.file_version = self.metadata[hash_content]

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


class FileRetrieveHandler(FileHandler):
    def __init__(self, user, file_path, file_version):
        super().__init__(user)
        self.file_path = file_path
        self.file_version = file_version
        self.metadata_path = os.path.join(self.user_repo_path, self.file_path, 'metadata.json')
        self.metadata = {}
        self.read_metadata()
        self.file_type = None
        self.file_name = None
        self.file_content = None

    def retrieve_file(self):
        """
        Method to retrieve a file form the server given the file path and version
        :return:
        """
        try:
            hash_content = self.find_hash_by_version()

            print(f'METAAA{self.metadata_path}')

            self.file_name = os.path.basename(self.file_path)

            self.file_type, _ = mimetypes.guess_type(self.file_name)

            extension = mimetypes.guess_extension(self.file_type)

            hash_file_name = f"{hash_content}{extension}"

            server_file_path = os.path.join(self.user_repo_path, self.file_path, hash_file_name)

            with open(server_file_path, 'rb') as file:
                self.file_content = base64.b64encode(file.read()).decode('utf-8')

            return True
        except FileNotFoundError:
            raise
        except Exception as e:
            print(e)
            return False

    def read_metadata(self):
        """
        Method to read the metadata file
        :return:
        """
        if os.path.exists(self.metadata_path):
            with open(self.metadata_path, 'r') as f:
                self.metadata = json.load(f)

    def find_hash_by_version(self):
        """
        Method to find the hash based on the given doc version
        :return:
        """
        for content_hash, hash_version in self.metadata.items():
            if int(hash_version) == self.file_version:
                return content_hash
        return None


class FileStructHandler(FileHandler):
    def __init__(self, user):
        super().__init__(user)

    def retrieve_folder_structure(self, path):
        try:
            contents = os.listdir(path)
            # files = [item for item in contents if os.path.isfile(os.path.join(path, item))]
            folders = [item for item in contents if os.path.isdir(os.path.join(path, item))]

            # response = {"path": path, "files": files, "folders": folders}
            response = {}

            for folder in folders:
                folder_path = os.path.join(path, folder)
                response[folder] = self.retrieve_folder_structure(folder_path)
                if os.path.exists(os.path.join(folder_path, 'metadata.json')):
                    metadata = self.read_metadata(os.path.join(folder_path, 'metadata.json'))
                    file_type, _ = mimetypes.guess_type(folder)
                    extension = mimetypes.guess_extension(file_type)
                    for hash_content, version in metadata.items():
                        response[folder][f'version-{version}'] = \
                            self.get_last_modified(os.path.join(folder_path, f'{hash_content}{extension}'))

            return response
        except FileNotFoundError:
            return None

    @classmethod
    def read_metadata(cls, path):
        """
        Method to read the metadata file
        :return:
        """
        metadata = {}
        if os.path.exists(path):
            with open(path, 'r') as f:
                metadata = json.load(f)
        return metadata

    @classmethod
    def get_last_modified(cls, file_path):
        try:
            print(f'HASHHH PATHHH{file_path}')
            mtime = os.path.getmtime(file_path)

            last_modified = datetime.datetime.fromtimestamp(mtime)
            formatted_last_modified = last_modified.strftime("%m-%d-%Y %H:%M:%S")

            return formatted_last_modified
        except FileNotFoundError:
            return None
