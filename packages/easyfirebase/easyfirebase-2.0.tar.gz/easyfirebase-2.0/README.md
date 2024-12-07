# EasyFirebase

a easy implementation of Firebase in django application.
If you do not want to upload your static files (ex: Image, pdf etc.) to the server then you can use EasyFirebase to upload all of your static files to Firebase and Easyfirebase will do the rest. Updating your file on updating models, deletions of file while you delete your model object or changes the file etc.

## Usage

```python
  from EasyFirebase.fields import FirebaseImageField
  from EasyFirebase.storage import FirebaseStorage

  class MyModel(models.Model):
    name = models.CharField(max_length=100)
    #...
    photo = models.FirebaseImageField(storage=FirebaseStorage, ... )
```

## Installation

```python
  pip install easyfirebase
```

Or,

Download the tar file and run the following command in django environment.

```python
  pip install ./EasyFirebase.tar.gz
```

## Settings.py

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

# Note: You must put your FIREBASE_CONFIG in `settings.py` and put your firebase sdk json file in the `BASE_DIR` of the project. ie, in the directory where `settings.py` resides.
