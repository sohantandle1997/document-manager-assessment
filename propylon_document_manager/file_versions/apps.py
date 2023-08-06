from django.apps import AppConfig


class FileVersionsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "file_versions"
    verbose_name = "File Versions"
    base_server_path = ""