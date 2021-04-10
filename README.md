
## Executing Web API

Follow the below steps to execute in your local

1. `pip install -r requirements.txt`
2. `python manage.py migrate`
3. `python manage.py runserver`

Load Fixtures 

`python manage.py loaddata fixtures/*`

Executing tests
1. `pytest` or `python manage.py test --settings=matrimony.settings_test`

To get Code Coverage details in detail
1. `coverage erase`
2. `coverage run manage.py test --settings-matrimony.settings_test`
3. `coverage report`
4. `coverage html`


python manage.py test api.tests --settings=matrimony.settings_test


TokenAuth is used to authenticate the User with its username and password to obtain the JSON Web token.

VerifyToken to confirm that the token is valid, passing it as an argument.

RefreshToken to obtain a new token within the renewed expiration time for non-expired tokens, if they are enabled to expire. Using it is outside the scope of this tutorial.

# Tello 

https://trello.com/b/tDx86YUE/matrimony

# POSTMAN COLLECTION

https://www.getpostman.com/collections/8bc9ca5ee135ada1cf46

# CHAT WebSocket Connection

ws://127.0.0.1:8000/ws/chat/5b33d4fe-93b8-4953-8130-8851cc6f8dd2/

ws://127.0.0.1:8000/ws/chat/<room-id>/

Operations 
	
	- fetch_messages
		{ "command":  "fetch_messages"}
	- new_message
		{ "command":  "new_message", "content": "ppppppp aaaadsat"}

