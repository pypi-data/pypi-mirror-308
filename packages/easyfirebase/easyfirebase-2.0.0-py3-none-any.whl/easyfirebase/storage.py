import os
from django.core.files.storage import Storage
from django.core.files.storage import Storage
from django.conf import settings

import firebase_admin
from firebase_admin import credentials, storage

# Initialize Firebase only once

if not firebase_admin._apps:
    cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_FILE)
    firebase_admin.initialize_app(
        cred, {"storageBucket": settings.FIREBASE_CONFIG["storageBucket"]}
    )


class FirebaseStorage(Storage):

    def _get_bucket(self):
        """Helper method to get Firebase storage bucket."""
        return storage.bucket()

    def _save(self, name, content):
        """Upload a file to Firebase and return its name."""
        default_folder = getattr(settings, "FIREBASE_DEFAULT_UPLOAD_DIR", None)
        if default_folder:
            name = os.path.join(default_folder, name)
        else:
            # adding project name as default dir.
            project_dir = getattr(settings, "BASE_DIR", None)
            if project_dir:
                project_name = os.path.basename(project_dir)
            else:
                project_name = "FreeDjangoFirebase"
            name = os.path.join(project_name, name)
        bucket = self._get_bucket()
        blob = bucket.blob(name)
        blob.upload_from_file(content, content_type=content.content_type)
        blob.make_public()  # Make the file publicly accessible
        return name

    def url(self, name):
        """Return the public URL of the file."""
        bucket = self._get_bucket()
        blob = bucket.blob(name)
        return blob.public_url if blob.exists() else None

    def exists(self, name):
        """Check if the file exists in Firebase storage."""
        bucket = self._get_bucket()
        blob = bucket.blob(name)
        return blob.exists()

    def delete(self, name):
        """Delete a file from Firebase storage."""
        bucket = self._get_bucket()
        blob = bucket.blob(name)
        blob.delete()

    def open(self, name, mode="rb"):
        """Open the file; Firebase does not support direct file retrieval, so raise an error."""
        raise NotImplementedError(
            "Direct file opening is not supported by FirebaseStorage.Instead use the 'url' method to get download link of the file."
        )

    def get_available_name(self, name, max_length=None):
        """Return the name of the file, ensuring it’s unique."""
        return (
            name  # Firebase automatically overwrites existing files with the same name
        )
