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
import requests
import base64
import os
import mimetypes


class FileVersionViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    authentication_classes = []
    permission_classes = []
    serializer_class = FileVersionSerializer
    queryset = FileVersion.objects.all()
    lookup_field = "id"


def say_hello(requests):
    return HttpResponse('Hello World')


# class FileUploadView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = FileUploadSerializer(data=request.data)
#         if serializer.is_valid():
#             file_path = serializer.validated_data['file-url']
#             try:
#                 # Get the file name from the file path and create the server path
#                 file_name = os.path.basename(file_path)
#                 server_path = os.path.join(
#                     '/Users/sohantandle/Documents/Personal/Jobs/Companies/Propylon/Assignment/file_manager', file_name)
#
#                 # Save the file on the server
#                 with open(file_path, 'rb') as src_file, open(server_path, 'wb') as dest_file:
#                     dest_file.write(src_file.read())
#
#                 return Response({'message': 'File uploaded successfully.'}, status=status.HTTP_201_CREATED)
#
#             except FileNotFoundError:
#                 return Response({'error': 'File not found.'}, status=status.HTTP_404_NOT_FOUND)
#
#             except Exception as e:
#                 return Response({'error': 'Failed to upload the file.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class FileUploadView(APIView):
#     parser_classes = [FileUploadParser]
#
#     def post(self, request, *args, **kwargs):
#         file_obj = request.FILES.get('file')
#         if file_obj:
#             # Save the file to the server's storage
#             with open('file_manager/' + file_obj.name, 'wb') as f:
#                 for chunk in file_obj.chunks():
#                     f.write(chunk)
#             return Response({'message': 'File uploaded successfully.'}, status=status.HTTP_201_CREATED)
#
#         return Response({'error': 'No file provided.'}, status=status.HTTP_400_BAD_REQUEST)


class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        file_content = request.data.get('file-content')
        file_name = request.data.get('file-name')
        file_type = request.data.get('file-type', 'application/octet-stream')
        destination_url = request.data.get('destination-url', '')

        if file_content and file_name and file_type:
            try:
                # Decode base64 file content to binary
                binary_data = base64.b64decode(file_content)

                # Create the server path for the destination URL
                base_server_path = '/Users/sohantandle/Documents/Personal/Jobs/Companies/Propylon/Assignment/document-manager-assessment/propylon_document_manager/file_versions/my_file_manager'
                if not os.path.exists(base_server_path):
                    os.mkdir(base_server_path)

                server_path = os.path.join(base_server_path, destination_url)
                print(server_path)
                os.makedirs(server_path, exist_ok=True)

                file_path = os.path.join(server_path, file_name)

                # Save the file to the server's storage
                with open(file_path, 'wb') as f:
                    f.write(binary_data)

                # Determine the file extension from the provided file type
                file_extension = mimetypes.guess_extension(file_type)
                if file_extension:
                    # Rename the file with the correct file extension
                    new_file_path = f"{file_path}{file_extension}"
                    os.rename(file_path, new_file_path)

                return Response({'message': 'File uploaded successfully.'}, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({'error': 'Failed to upload the file.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'error': 'Invalid request data.'}, status=status.HTTP_400_BAD_REQUEST)