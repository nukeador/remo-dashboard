remo-dashboard
==============

Test dashboard for Mozilla Reps

### Install

Clone this repo

    $ git clone git@github.com:nukeador/remo-dashboard.git
    
You should be using a ``virtualenv`` for this project.

    $ sudo aptitude install pip
    $ sudo pip install virtualenv

Create and enable the ``virtualenv``

    $ virtualenv remo-dashboard
    $ cd remo-dashboard
    $ source bin/activate

You'll need to install python packages used in this project. These are in ``requirements.txt``.

The best way to install these packages is using ``pip``:

    $ pip install -r requirements.txt

Run the testserver

    $ python manage.py runserver