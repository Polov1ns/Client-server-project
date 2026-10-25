import os
import uuid
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile


class InvalidFileUploadException(Exception):
    """Виняток для некоректних файлів завантаження (повертає 400 Bad Request)"""
    pass


class CoverImageService:
    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png'}
    ALLOWED_MIME_TYPES = {'image/jpeg', 'image/png'}
    MAX_FILE_SIZE = 5 * 1024 * 1024 

    @staticmethod
    def get_upload_directory():
        # Зберігаємо у папку wwwroot/uploads
        return os.path.join(settings.BASE_DIR, 'wwwroot', 'uploads')

    @classmethod
    def validate_and_save(cls, resource, file_obj: UploadedFile):
        if not file_obj or file_obj.size == 0:
            raise InvalidFileUploadException("Select a non-empty JPEG or PNG file.")
        
        if file_obj.size > cls.MAX_FILE_SIZE:
            raise InvalidFileUploadException("The cover image must not exceed 5 MB.")

        if file_obj.content_type not in cls.ALLOWED_MIME_TYPES:
            raise InvalidFileUploadException("Only JPEG and PNG cover images are supported.")

        ext = os.path.splitext(file_obj.name)[1].lower()
        if ext not in cls.ALLOWED_EXTENSIONS:
            raise InvalidFileUploadException("The file extension does not match the declared image type.")

        # Генерація безпечного випадкового імені файла
        filename = f"{uuid.uuid4().hex}{ext}"
        upload_dir = cls.get_upload_directory()
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, filename)

        # Запис файлу на диск
        try:
            with open(file_path, 'wb+') as destination:
                for chunk in file_obj.chunks():
                    destination.write(chunk)
        except Exception:
            raise InvalidFileUploadException("Failed to save the file on the server.")

        # Зберігаємо старе ім'я для подальшого видалення
        old_cover = resource.cover_image
        resource.cover_image = filename
        resource.save()


        if old_cover:
            cls.delete_file_by_name(old_cover)

        return filename

    @classmethod
    def delete_file_by_name(cls, filename):
        if not filename:
            return
        file_path = os.path.join(cls.get_upload_directory(), filename)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass

    @classmethod
    def get_file_path(cls, filename):
        if not filename:
            return None
        file_path = os.path.join(cls.get_upload_directory(), filename)
        if os.path.exists(file_path):
            return file_path
        return None