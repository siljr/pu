[![Coverage Status](https://coveralls.io/repos/github/siljr/pu/badge.svg?branch=master)](https://coveralls.io/github/siljr/pu?branch=master)
[![Build Status](https://travis-ci.org/siljr/pu.svg?branch=master)](https://travis-ci.org/siljr/pu)

TDT4140 - Programvareutvikling

2017 

Gruppe 34 
Eivind Keil, Håkon Molven, Long T. Thai, Silje Riseng 

qBot 

# Get started
0. Install pip https://pip.pypa.io/en/stable/installing/ 
1. Set up a virtual enviroment https://virtualenv.pypa.io/en/stable/
  * `virtualenv -p /usr/local/bin/python3.6 env`
2. Clone project 
  * `git clone https://github.com/siljr/pu.git`
3. Open virtual enviroment 
  cd to the virtual enviroment folder (probably named env or venv)
  * `source bin/activate`
4. Install requirements.txt 
  * `pip install -r requirements.txt`
5. Migrate server 
  * `python manage.py migrate`
6. Run server 
  * cd to the qBot folder 
  * `python manage.py runserver` 
7. Create superuser 
  * `python manage.py createsuperuser`
  * username: admin
  * email: (leave blank, just press enter)
  * password: admin123

## Look at the webapp 
1. Go to https://qbot-ntnu.herokuapp.com/

## Look at the login 
1. Go to https://qbot-ntnu.herokuapp.com/login/

## Look at the registration page 
1. click "register" on the navbar(https://qbot-ntnu.herokuapp.com/register)

# View about page
1. click "about" on the navbar(https://qbot-ntnu.herokuapp.com/about/)

# Logout
1. click "logout" on the navbar(https://qbot-ntnu.herokuapp.com/logout/)

# Sort questions
1. Click on "Newest" under the navbar(https://qbot-ntnu.herokuapp.com/questions/myquestions/n/)
2. Click on "Oldest" under the navbar(https://qbot-ntnu.herokuapp.com/questions/myquestions/o/)
3. Click on "Most votes" under the navbar(https://qbot-ntnu.herokuapp.com/questions/myquestions/mv/)

## Post a new question
1. Click "New question" button on the navbar(https://qbot-ntnu.herokuapp.com/questions/create_question)
2. Fill in form
3. Press "Submit"

## View your asked questions
1. Click "My questions" button the navbar(https://qbot-ntnu.herokuapp.com/questions/myquestions/)

## View scores(Admin access only!)
1. Click "scores" button on the navbar(https://qbot-ntnu.herokuapp.com/questions/scores/)

## View Profile page
1. Click "profile" button on the navbar(https://qbot-ntnu.herokuapp.com/profile/)
