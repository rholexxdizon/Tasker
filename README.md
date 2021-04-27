# Tasker

## installation instructions

### step1:

install python

### step2:

clone this repository

```powershell
git clone https://github.com/RJGJ/Tasker.git
cd Tasker
```


### step3: (optional)

create a virtual enviroment

install virtualenv first

```powershell
python -m pip install virtualenv
```

start virtual environment

```powershell
python -m pip virtualenv <your environment name>
```

activate

```powershell
call <environment name>\Scripts\activate
  ```
  
### step4:

install requirements

```powershell
pip install -r requirements.txt
```

### step5: 

perform migrations

```powershell
python manage.py makemigrations
python manage.py migrate
# create admin user
python manage.py createsuperuser
# enter your preferred credentials
```

### step6:

start development server

```powershell
python manage.py runserver
```

go to localhost:8000 on web browser
