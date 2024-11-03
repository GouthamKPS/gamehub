This is a modern video game store made using the Python web framework Django.  
No external modules are used.

A `data.json` file is provided to import sample data. It can be committed using:

```bash
python manage.py loaddata data.json

#### Fixing errors while importing the data.json file
Run the following in order to properly import the data and avoid content type errors:
```bash
python manage.py migrate

Enter the python shell by running `py manage.py shell`. Then :
```bash
from django.contrib.contenttypes.models import ContentType
ContentType.objects.all()

```bash
ContentType.objects.all().delete()

You can exit the shell by running `exit()`.

