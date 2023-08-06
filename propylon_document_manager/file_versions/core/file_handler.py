import base64
import hashlib
import mimetypes
import os
import json
import datetime

BASE_SERVER_PATH = '/Users/sohantandle/Documents/Personal/Jobs/Companies/Propylon/Assignment/document-manager-assessment/propylon_document_manager/file_versions/user_repo'


class FileHandler:
    def __init__(self, user):
        """
        Base initialization for file handling
        :param user:
        """
        self.user = user
        self.user_repo_path = os.path.join(BASE_SERVER_PATH, self.user)

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
    def get_file_tyep_n_extension(cls, file_name):
        """
        Method to get the extension of a file based on its name
        :param file_name:
        :return:
        """
        file_type, _ = mimetypes.guess_type(file_name)
        extension = mimetypes.guess_extension(file_type)
        return file_type, extension


class FileUploadHandler(FileHandler):

    def __init__(self, user, file_content, file_name, file_type, target_path):
        """
        Initialize file upload variables
        :param user:
        :param file_content:
        :param file_name:
        :param file_type:
        :param target_path:
        """
        super().__init__(user)
        self.target_path = target_path.lstrip("/")
        self.file_name = file_name
        self.file_type = file_type
        self.file_content = file_content
        self.server_path = os.path.join(self.user_repo_path, self.target_path, self.file_name)
        self.metadata_path = os.path.join(self.server_path, 'metadata.json')
        self.metadata = self.read_metadata(self.metadata_path)
        self.file_version = 0

    def upload_file(self):
        """
        Method to upload file on to a given path
        :return:
        """
        try:
            os.makedirs(self.server_path, exist_ok=True)

            binary_data = base64.b64decode(self.file_content)
            content_hash = hashlib.sha256(binary_data).hexdigest()

            file_extension = mimetypes.guess_extension(self.file_type)
            hash_file_name = f"{content_hash}{file_extension}"

            self.generate_file_version(content_hash)

            file_path = os.path.join(self.server_path, hash_file_name)
            with open(file_path, 'wb') as f:
                f.write(binary_data)

            self.update_metadata(content_hash)

            return True

        except Exception as e:
            return False

    def generate_file_version(self, hash_content):
        """
        Method to generate next version number of the file
        :return:
        """
        max_version = max(self.metadata.values(), default=-1)
        # self.file_version = self.metadata.get(hash_content, default=max_version + 1)
        self.file_version = max_version + 1
        if hash_content in self.metadata:
            self.file_version = self.metadata[hash_content]

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
        """
        Initialize file retrieve variables
        :param user:
        :param file_path:
        :param file_version:
        """
        super().__init__(user)
        self.file_path = file_path.lstrip("/")
        self.file_version = file_version
        _metadata_path = os.path.join(self.user_repo_path, self.file_path, 'metadata.json')
        self.metadata = self.read_metadata(_metadata_path)
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

            self.file_name = os.path.basename(self.file_path)
            self.file_type, extension = self.get_file_tyep_n_extension(self.file_name)
            hash_file_name = f"{hash_content}{extension}"

            server_file_path = os.path.join(self.user_repo_path, self.file_path, hash_file_name)
            with open(server_file_path, 'rb') as file:
                self.file_content = base64.b64encode(file.read()).decode('utf-8')

            return True
        except FileNotFoundError:
            raise
        except Exception as e:
            return False

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
        """
        Initialize file structure variables
        :param user:
        """
        super().__init__(user)

    def retrieve_folder_structure(self, path):
        """
        Method to build the folder and file structure
        :param path:
        :return:
        """
        try:
            contents = os.listdir(path)
            # files = [item for item in contents if os.path.isfile(os.path.join(path, item))]
            folders = [item for item in contents if os.path.isdir(os.path.join(path, item))]

            # response = {"path": path, "files": files, "folders": folders}
            response = {}

            for folder in folders:
                folder_path = os.path.join(path, folder)
                response[folder] = self.retrieve_folder_structure(folder_path)

                # If the folder has metadata.json read all the hash files and its versions
                if os.path.exists(os.path.join(folder_path, 'metadata.json')):
                    metadata = self.read_metadata(os.path.join(folder_path, 'metadata.json'))

                    file_type, extension = self.get_file_tyep_n_extension(folder)

                    for hash_content, version in metadata.items():
                        response[folder][f'version-{version}'] = \
                            self.get_last_modified(os.path.join(folder_path, f'{hash_content}{extension}'))

            return response
        except FileNotFoundError:
            raise

    @classmethod
    def get_last_modified(cls, file_path):
        """
        Method to get the last modified data of a file
        :param file_path:
        :return:
        """
        try:
            mtime = os.path.getmtime(file_path)

            last_modified = datetime.datetime.fromtimestamp(mtime)
            formatted_last_modified = last_modified.strftime("%m-%d-%Y %H:%M:%S")

            return formatted_last_modified
        except FileNotFoundError:
            return None
