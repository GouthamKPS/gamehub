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
![home_3_11zon](https://github.com/user-attachments/assets/4f4d38d6-596e-4b1e-8d34-5f173be0f913)

----------
![publisher_2_11zon](https://github.com/user-attachments/assets/04658325-dbf8-4e0b-a795-19d356bebefc)

----------
![category_1_11zon](https://github.com/user-attachments/assets/c1a70b84-671a-4f12-897b-472a001ea07b)




