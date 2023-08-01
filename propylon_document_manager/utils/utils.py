import base64
import os
import mimetypes


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


file_upload_request = Utils.construct_file_upload_request(
    '/Users/sohantandle/Documents/Personal/Jobs/DCU_LinkedIn_Tips.pdf',
    '/Users/sohantandle/Documents/Personal/Jobs/Companies/Propylon/Assignment/file_manager')
print(file_upload_request)
#%%
