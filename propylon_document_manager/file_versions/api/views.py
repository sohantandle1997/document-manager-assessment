from django.shortcuts import render

from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from file_versions.models import FileVersion
from .serializers import FileVersionSerializer

from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileUploadSerializer
from propylon_document_manager.file_versions.core.file_handler import FileUploadHandler, FileRetrieveHandler, \
    FileStructHandler
from propylon_document_manager.file_versions.core.metadata import ResponseMsgs, ReqResFields


class FileVersionViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    authentication_classes = []
    permission_classes = []
    serializer_class = FileVersionSerializer
    queryset = FileVersion.objects.all()
    lookup_field = "id"


class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        """
        A POST method API to upload a file on to the server
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        user = str(request.user)
        file_content = request.data.get(ReqResFields.FILE_CONTENT)
        file_type = request.data.get(ReqResFields.FILE_TYPE, 'application/octet-stream')
        target_path = request.data.get(ReqResFields.TARGET_PATH, '')
        file_name = request.data.get(ReqResFields.FILE_NAME)

        if file_content and file_name and file_type and target_path:
            file_handler = FileUploadHandler(user, file_content, file_name, file_type, target_path)
            is_successful = file_handler.upload_file()
            if is_successful:
                return Response({ReqResFields.MESSAGE: ResponseMsgs.UPLOAD_SUCCESSFUL,
                                 ReqResFields.VERSION: file_handler.file_version}, status=status.HTTP_201_CREATED)
            return Response({ReqResFields.ERROR: ResponseMsgs.FAILED_TO_UPLOAD}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({ReqResFields.ERROR: ResponseMsgs.INVALID_REQUEST}, status=status.HTTP_400_BAD_REQUEST)


class FileRetrieveView(APIView):
    def get(self, request, *args, **kwargs):
        """
        A GET method API to retrieve a file from the server
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        user = str(request.user)
        source_path = request.GET.get(ReqResFields.SOURCE_PATH)
        file_version = int(request.GET.get(ReqResFields.VERSION, 0))

        if source_path and file_version is not None:

            try:
                file_handler = FileRetrieveHandler(user, source_path, file_version)
                is_successful = file_handler.retrieve_file()
            except FileNotFoundError:
                return Response({ReqResFields.ERROR: ResponseMsgs.FILE_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)

            if is_successful:
                response = {
                    ReqResFields.VERSION: file_handler.file_version,
                    ReqResFields.FILE_CONTENT: file_handler.file_content,
                    ReqResFields.FILE_TYPE: file_handler.file_type,
                    ReqResFields.FILE_NAME: file_handler.file_name,
                    ReqResFields.MESSAGE: ResponseMsgs.RETRIEVE_SUCCESSFUL
                }
                return Response(response, status=status.HTTP_200_OK)

            return Response({ReqResFields.ERROR: ResponseMsgs.FAILED_TO_RETRIEVE_FILE},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({ReqResFields.ERROR: ResponseMsgs.INVALID_REQUEST}, status=status.HTTP_400_BAD_REQUEST)


class FileStructView(APIView):
    def get(self, request, *args, **kwargs):
        """
        A GET method API to view the folders and files structure on the server
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # folder_path = request.data.get('url', '')
        user = str(request.user)

        try:
            file_handler = FileStructHandler(user)
            file_structure = file_handler.retrieve_folder_structure(file_handler.user_repo_path)
            if not file_structure:
                return Response({ReqResFields.MESSAGE: ResponseMsgs.EMPTY_REPO},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(file_structure, status=status.HTTP_200_OK)
        except:
            return Response({ReqResFields.ERROR: ResponseMsgs.FAILED_TO_RETRIEVE_STRUCT},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

