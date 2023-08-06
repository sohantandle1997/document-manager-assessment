import pytest
import os
import builtins
import mimetypes
import typing
import base64
from propylon_document_manager.file_versions.core.file_handler import FileUploadHandler, FileRetrieveHandler, FileStructHandler


@pytest.fixture(scope="function")
def mock_open(mocker):
    return mocker.patch.object(builtins, 'open')


@pytest.fixture(scope="function")
def mock_open_exception(mocker):
    return mocker.patch.object(builtins, 'open', side_effect=Exception("error"))


@pytest.fixture(scope="function")
def mock_open_exception_fnf(mocker):
    return mocker.patch.object(builtins, 'open', side_effect=FileNotFoundError)


@pytest.fixture(scope="function")
def mock_write(mocker):
    return mocker.patch.object(typing, 'write')


@pytest.fixture(scope="function")
def mock_makedirs(mocker):
    return mocker.patch.object(os, 'makedirs')


@pytest.fixture(scope="function")
def mock_guess_extension(mocker):
    return mocker.patch.object(mimetypes, 'guess_extension')


@pytest.fixture(scope="function")
def mock_guess_type(mocker):
    return mocker.patch.object(mimetypes, 'guess_type', return_value=('', ''))


@pytest.fixture(scope="function")
def mock_b64encode(mocker):
    return mocker.patch.object(base64, 'b64encode')


@pytest.fixture(scope="function")
def mock_isdir(mocker):
    return mocker.patch.object(os.path, 'isdir', return_value=True)


@pytest.fixture(scope="function")
def mock_listdir(mocker):
    return mocker.patch.object(os, 'listdir', return_value=['abc', 'xyz'])
# @pytest.fixture(scope="function")
# def mock_read(mocker):
#     return mocker.patch.object(typing, 'read')


@pytest.fixture(scope="class")
def file_upload_handler(request):
    file_name = "example.txt"
    file_type = "text/plain"
    file_content = "Base64EncodedFileContentHere"
    target_path = "/uploads/"

    user = "test_user"
    handler = FileUploadHandler(
        user=user,
        file_content=file_content,
        file_name=file_name,
        file_type=file_type,
        target_path=target_path
    )

    return handler


@pytest.mark.usefixtures("file_upload_handler")
class TestFileUploadHandler:
    # @pytest.mark.parametrize("test_input_params, expected_output", [
    #     ()
    # ])
    @pytest.mark.usefixtures("mock_makedirs", "mock_guess_extension", "mock_open")
    def test_upload_file_success(self, file_upload_handler):
        is_successful = file_upload_handler.upload_file()
        assert is_successful == True

    @pytest.mark.usefixtures("mock_makedirs", "mock_guess_extension", "mock_open_exception")
    def test_upload_file_failure(self, file_upload_handler):
        is_successful = file_upload_handler.upload_file()
        assert is_successful == False


@pytest.fixture(scope="class")
def file_retrieve_handler():
    file_path = "/uploads/"
    file_version = 0
    user = "test_user"

    handler = FileRetrieveHandler(
        user=user,
        file_path=file_path,
        file_version=file_version
    )
    return handler


@pytest.mark.usefixtures("file_retrieve_handler")
class TestFileRetrieveHandler:
    @pytest.mark.usefixtures("mock_makedirs", "mock_guess_extension", "mock_guess_type", "mock_b64encode", "mock_open")
    def test_retrieve_file_success(self, file_retrieve_handler):
        is_successful = file_retrieve_handler.retrieve_file()
        assert is_successful == True

    @pytest.mark.usefixtures("mock_makedirs", "mock_guess_extension", "mock_guess_type", "mock_b64encode",
                             "mock_open_exception")
    def test_upload_file_failure(self, file_retrieve_handler):
        is_successful = file_retrieve_handler.retrieve_file()
        assert is_successful == False

    @pytest.mark.usefixtures("mock_makedirs", "mock_guess_extension", "mock_guess_type", "mock_open_exception_fnf")
    def test_upload_file_fnf(self, file_retrieve_handler):
        try:
            is_successful = file_retrieve_handler.retrieve_file()
        except:
         pass


@pytest.fixture(scope="class")
def file_struct_handler():
    user = "test_user"

    handler = FileStructHandler(
        user=user
    )
    return handler


# @pytest.mark.usefixtures("file_struct_handler")
# class TestFileStructHandler:
#     @pytest.mark.usefixtures("mock_open", "mock_listdir", "mock_isdir")
#     def test_retrieve_folder_structure(self, file_struct_handler):
#         response = file_struct_handler.retrieve_folder_structure('/uploads/')
#         # assert is_successful == True



#%%
