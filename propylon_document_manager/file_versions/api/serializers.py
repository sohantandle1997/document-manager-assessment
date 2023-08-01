from rest_framework import serializers

from file_versions.models import FileVersion


class FileVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileVersion
        fields = "__all__"


class FileUploadSerializer(serializers.Serializer):
    file_url = serializers.CharField()

