
<h1 align="center">
  <br>
  <a href="http://35.198.36.42/"><img src="devTeamTaskLogo.png" alt="DevTeamTask" width="200" style="border-radius: 2px"></a>
  <br>
  DevTeamTask
  <br>
</h1>

<h4 align="center">A task management software for development team built on top of <a href="https://www.django-rest-framework.org/" target="_blank">Django Rest Framework</a>.</h4>


<p align="center">
  <a href="https://github.com/cookiecutter/cookiecutter-django/">
    <img src="https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter"
         alt="Logo Cookiecutter">
  </a>
  <a href="https://github.com/ambv/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

</p>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#credits">Credits</a> •
  <a href="#license">License</a> •
  <a href="#contact">Contact</a>
</p>

![screenshot](devteamtaskgif.gif)

## Key Features

* User control
  - With support for sending an email if the user wants to reset the password outside the application
* Socal authentication
  - Supports: Google and Github
* Project management  
* Project status management
* Project tag management
* Project sprint management
* Project task management
* Event note management
* App routes secured with `JWT` authorization
* Encryption for sensitive information

## How To Use

To clone and run this application, you'll need [Git](https://git-scm.com), [Python 3.10.6](https://www.python.org/download/) and [Postgres 15.3](https://www.postgresql.org/download/). From your command line:

```bash
# Clone this repository
$ git clone https://github.com/Talismar/devteamtask-back

# Go into the repository
$ cd devteamtask-back

# Create enviroment virtual
$ python3 -m venv venv

# Active enviroment virtual
$ source venv/bin/activate

# Install dependencies
$ pip install -r requirements/production.txt

# export global variable
$ export DJANGO_READ_DOT_ENV_FILE=True

# run the project
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py load_db_v1
$ python manage.py runserver
```

> **Note**
> If you're using Linux Bash for Windows, [see this guide]().

## Credits

This software uses the following open source packages:

- [Django](https://www.djangoproject.com/)
- [Django Rest Framework](https://github.com/encode/django-rest-framework)
- [Django Filters](https://django-filter.readthedocs.io/en/stable/)
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
- [Django Cors Headers](https://github.com/adamchainz/django-cors-headers)
- [DRF Spectacular](https://github.com/tfranzel/drf-spectacular)
- [DRF Flex Fields](https://github.com/rsinger86/drf-flex-fields)


## You may also like...

- [DevTeamTask-CLI](https://github.com/amitmerchant1990/pomolectron) - A task management software for development team
- [DevTeamTask-Frontend](https://github.com/amitmerchant1990/correo) - A task management software for development team
- [DevTeamTask-Figma](https://www.figma.com/file/93HpbAt9qbG8F41DQERB37/DevTeamTask-%7C-PI-02?type=design&mode=design&t=DoRfhoPhuCJtCq7Q-1) - A task management software for development team

## License

MIT

---

## Contact 

> GitHub [Talismar](https://github.com/Talismar)
> Facebook [Tali Fer Costa](https://www.facebook.com/tali.fercosta)
> Gmail [talismar788.una@gmail.com]()
