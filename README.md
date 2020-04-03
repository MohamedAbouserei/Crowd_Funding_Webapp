# Crowd-Funding Web app
[![PyPi Version](https://img.shields.io/pypi/v/yt2mp3.svg)](https://pypi.python.org/pypi/yt2mp3/)
[![PyPi Version Alt](https://badge.fury.io/py/yt2mp3.svg)](https://pypi.python.org/pypi/yt2mp3/)  
[![PyPi Python Versions](https://img.shields.io/pypi/pyversions/yt2mp3.svg)](https://pypi.python.org/pypi/yt2mp3/)
[![PyPi Downloads](http://pepy.tech/badge/yt2mp3)](http://pepy.tech/project/yt2mp3)
[![Python Versions](https://img.shields.io/pypi/pyversions/yt2mp3.svg)](https://pypi.python.org/pypi/yt2mp3/)

> Crowdfunding is the practice of funding a project or venture by raising small
amounts of money from a large number of people, typically via the Internet.
Crowdfunding is a form of crowdsourcing and alternative finance. In 2015,
over US$34 billion was raised worldwide by crowdfunding.


## Aim of the project
Create a web platform for starting fundraise
projects in Egypt.

## Features of the project
1- User :
##### Authentication System​ :
- Registration:
- Activation Email after registration
- Once the user register he should receive an email with the activation link. The user shouldn’t be able to login without
activation. The activation link should expire after 24 hours.
- Login
- The user should be able to login after activation using his email
and password

####  profile :
- user can view his profile
- user can view his projects
- user can view his donations
- user can edit all his data except for the email
- user can have extra optional info other than the info he added
while registration (Birthdate, facebook profile, country)
- User can delete his account (Note that there must be a
confirmation message before deleting)

2- project 
- The user can create a project fund raise campaign 
- Users can view any project and donate to the total target

- Users can add comments on the projects

- Users can report inappropriate projects

- Users can report inappropriate comments
- Users can rate the projects
- Project creator can cancel the project if the donations are less than
25% of the target

3- Homepage

## Installation

```sh
OS centos
```
```sh
program VScode
```
## Development setup
install virtualenv  then activate it and install all dependences which in requirements.txt


```sh
pip3 install virtualenv
```

```sh
pip3 install django
```
```sh
pip3 install bootstrap4
```
```sh
sudo pip install pillow
```
```sh
sudo pip install ajaxuploader
```

# steps :

1- clone repository

2- activate virtualenv :
```
source fund/bin/activate
```
2- run localhost server:
```
python3 manage.py runserver
``` 
3- in browser write localhost:8000 , 

4- you can sign up to see all projects and donate to them 











