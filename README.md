TDT4140 - Programvareutvikling

2017 

Gruppe 34 
Eivind Keil, Håkon Molven, Long T. Thai, Silje Riseng 

qBot 

# Get started
0. Install pip https://pip.pypa.io/en/stable/installing/ 
1. Set up a virtual enviroment https://virtualenv.pypa.io/en/stable/ 
2. Clone project 
  * `git clone https://github.com/siljr/pu.git`
3. Open virtual enviroment 
  * `source bin/activate`
4. Install requirements.txt 
  * `pip install -r requirements.txt`
5. Migrate server 
  * `python manage.py migrate`
6. Run server 
  * `python manage.py runserver` 

## login as admin 
1. Run server 
2. Go to http://127.0.0.1:8000/admin 
3. Input username and password
  * username: admin
	* password: admin123

## look at the app 
1. Run server
2. Go to http://127.0.0.1:8000/questions/
