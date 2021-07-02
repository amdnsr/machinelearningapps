# Lab Website

## Requirements

To install the requirements, create a virtual environment and run:

```setup
pip install -r requirements.txt
```

## Usage

The code can either take input via a file which is passed as a command line argument, or the input can be entered manually

```usage
export FLASK_APP=application.py
export FLASK_DEBUG=1
export EMAIL_ADDRESS=""
export PASSWORD=""
flask run
```
* `EMAIL_ADDRESS` should be the actual gmail address from where the email will be sent and `PASSWORD` will be the password of the corresponding email

* By default the home address is the [localhost](http://127.0.0.1:5000/) If we are using an online webserver, then we'd have to replace the [localhost](http://127.0.0.1:5000/)  with the corresponding home address in the website_data.py file

* To use the email sender code, we need to allow [DisplayUnlockCaptcha](https://accounts.google.com/DisplayUnlockCaptcha) and [less secure apps](https://myaccount.google.com/lesssecureapps)


