class ReqResFields:
    FILE_CONTENT = 'file-content'
    FILE_TYPE = 'file-type'
    TARGET_PATH = 'target-path'
    FILE_NAME = 'file-name'
    SOURCE_PATH = 'source-path'
    VERSION = 'version'
    MESSAGE = 'message'
    ERROR = 'error'


class ResponseMsgs:
    INVALID_REQUEST = 'Invalid request data'
    FAILED_TO_RETRIEVE_FILE = 'Failed to retrieve the file'
    FAILED_TO_RETRIEVE_STRUCT = 'Failed to retrieve the file structure'
    FAILED_TO_UPLOAD = 'Failed to upload the file'
    EMPTY_REPO = 'Repository is empty'
    RETRIEVE_SUCCESSFUL = 'File retrieved successfully'
    UPLOAD_SUCCESSFUL = 'File uploaded successfully'
    FILE_NOT_FOUND = 'File not found. Please provide valid path'
