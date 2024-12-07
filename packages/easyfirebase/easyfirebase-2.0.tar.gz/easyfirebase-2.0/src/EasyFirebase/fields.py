from typing import Any
from django.db import models
from django.db.models.fields.files import FieldFile
from django.db.models.fields.files import ImageFieldFile
from django.core.files.storage import default_storage
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class _FirebaseFieldFile(FieldFile):

    @property
    def url(self):
        return self.storage.url(self.name)


class FirebaseFileField(models.FileField):
    """Free File Hosting base Class"""

    attr_class = _FirebaseFieldFile

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs["storage"] = kwargs.get("storage", default_storage)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        """
        Custom deconstruct method to ensure that the storage backend is not serialized in migrations.
        """
        name, path, args, kwargs = super().deconstruct()

        # Remove 'storage' from kwargs to avoid serialization issues
        if "storage" in kwargs:
            del kwargs["storage"]

        return name, path, args, kwargs

    def to_python(self, value):
        if value is not None:
            return value
        return super().to_python(value)

    def pre_save(self, model_instance, add):
        file_changed = False

        # Retrieve the current value from the database if it's not a new instance
        if not add and model_instance.pk:
            existing_instance = (
                model_instance.__class__.objects.filter(pk=model_instance.pk)
                .only(self.attname)
                .first()
            )

            if existing_instance:
                value_before_save = getattr(existing_instance, self.attname, None)
                value_after_save = getattr(model_instance, self.attname, None)
                file_changed = value_before_save != value_after_save and bool(
                    value_before_save
                )
                # print(file_changed)

                if file_changed:
                    # Delete the old file
                    field = existing_instance._meta.get_field(self.name)
                    field_file = getattr(existing_instance, self.name, None)
                    field.storage.delete(str(field_file))  # type: ignore
            else:
                raise ValueError(
                    "object not found. debug at fields.py in method pre_save"
                )
        else:
            pass
        return super().pre_save(model_instance, add)

    @receiver(pre_delete)
    def delete_image_on_model_delete(instance, **kwargs):
        for field in instance._meta.fields:  # type: ignore
            if isinstance(field, FirebaseFileField):
                firebase_image_field_file = getattr(instance, field.name, None)
                if (
                    firebase_image_field_file is not None
                    and firebase_image_field_file.name != ""
                ):
                    try:
                        field.storage.delete(str(firebase_image_field_file.name))
                    except Exception as e:
                        print(
                            f"[!!!] Warning! Can't delete the file in source. Exception: {e}\nobject:{instance}.fileld: {field}"
                        )


class FirebaseImageFieldFile(_FirebaseFieldFile, ImageFieldFile):
    pass


class FirebaseImageField(models.ImageField, FirebaseFileField):
    attr_class = FirebaseImageFieldFile
