# ntsw

a simple issues system , *just like github issue ,but not such powerful*

create a issue ,then system will email yourself and  techsupport .


settings.py should be configed , example is avail. 

## /issues/new will create a new issue


![pig2](https://user-images.githubusercontent.com/6398936/28869408-2c2a66e2-77af-11e7-98ee-d27329d45a7f.png)


## /issues/\<issues-id\>?token=\<token-id\> will see issue infos 


![pig1](https://user-images.githubusercontent.com/6398936/28869387-20cff88e-77af-11e7-94ef-7892384e9f4f.png)

token could be used for private view . without it , visitor could only see public infos.

## setups 

```
pip install django==1.11.4
pip install django-markdown_deux==1.0.5
cp ntsw/settings_example.py ntsw/settings.py
python manage.py makemigrations issues
python manage.py migrate
python manage.py createsuperuser
vi ntsw/settings.py
```

run :

```
python manage.py runserver 0.0.0.0:8000
```

## NEXT

if this resp is useful , more functions will be add later :

* issues list & online discuss
* tags
* user sign up and login .
* issues open and close 
* a call-board or/and blog system .

even more with hpc api :

* auto job info search
* issues auto reply . 
