# EasyFirebase

An easy implementation of Firebase in django application.
If you do not want to upload your static files (ex: Image, pdf etc.) to the server then you can use easyfirebase to upload all of your static files to Firebase and easyfirebase will do the rest. Updating your file on updating models, deletions of file while you delete your model object or changes the file etc.

## Usage

```python
  from easyfirebase.fields import FirebaseImageField
  from easyfirebase.storage import FirebaseStorage

  class MyModel(models.Model):
    name = models.CharField(max_length=100)
    #...
    photo = models.FirebaseImageField(storage=FirebaseStorage, ... )
```

If you do not provide any parameter for storage, then easyfirebase will use Default Django storage, which will store your image/pdf files in the local/server root dir or upload dir provided by STATIC_ROOT.

## Installation

```python
  pip install easyfirebase
```

Or,

Download the tar file and run the following command in django environment.

```python
  pip install ./easyfirebase.tar.gz
```

add the app name in the `settings.py` of project.

```python
  INSTALLED_APPS = [
    ...
    'easyfirebase',
    ...
    ]
```

## Configure Settings.py

Get your firebase json config file and info from firebase console. Write the following code in your projects `settings.py` file:

```python

  FIREBASE_CONFIG = {
      "apiKey": "your api key",
      "authDomain": "your domain name",
      "databaseURL": "your databaseURL",
      "projectId": "your projectID",
      "storageBucket": "your storageBucket",
      "messagingSenderId": "your messagingSenderId",
      "appId": "your app id",
      "measurementId": "your measurementId",
  }

  FIREBASE_CREDENTIALS_FILE = (
      BASE_DIR / "path/to/your/firebase/config/file.json"
  )
```

[optional: `settings.py`]

```python
FIREBASE_DEFAULT_UPLOAD_DIR = "test_dir"
```

This will set the default upload directory for all FirebaseImageField instances in the Firebase Storage. If not provided, easyfirebase will first try to set the `Project_name` as the default upload dir in the Firebase Storage.
or if the above also fails, `FreeDjangoFirebase/` will be the default upload dir.

Note: You must put your FIREBASE_CONFIG in `settings.py` and put your firebase sdk json file in the `BASE_DIR` of the project. ie, in the directory where `settings.py` resides.
