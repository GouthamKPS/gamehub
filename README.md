This is a modern video game store made using the Python web framework Django.  
No external modules are used.

A `data.json` file is provided to import sample data. It can be imported using:

```bash
python manage.py loaddata data.json
```

### Fixing errors while importing the data.json file
Run the following in order to properly import the data and avoid content type errors:
```bash
python manage.py migrate
```

Enter the python shell by running `py manage.py shell`. Then :
```bash
from django.contrib.contenttypes.models import ContentType
ContentType.objects.all()
```

```bash
ContentType.objects.all().delete()
```

You can exit the shell by running `exit()`.

Now import the data by running
```bash
python manage.py loaddata data.json
```
###  Preview
![{67D5A0D4-DF86-4AFD-A216-CF9AFE7220B4}](https://github.com/user-attachments/assets/edbfcacd-010d-4d09-86e7-db63ec58cfeb)
----------
![{219F951A-732F-4702-ADD6-946A0D700F60}](https://github.com/user-attachments/assets/42cae678-9e78-4c0e-8283-df19d8b0ee0b)
----------
![{C1618B0F-36D3-4753-8426-F3D0D0090D19}](https://github.com/user-attachments/assets/314e2937-47bf-4dca-be60-7de6083057f4)



