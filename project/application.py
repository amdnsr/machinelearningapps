import datetime
import os
import secrets
from tempfile import mkdtemp

import pytz
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from helpers import apology, clearFolderContents, createFolder, login_required
from send_mail import send_mail
from website_data import website




from PIL import Image
import argparse
import os
import mimetypes
from utils.transforms import get_no_aug_transform
import torch
from models.generator import Generator
import numpy as np
import torchvision.transforms.functional as TF
import torch.nn.functional as F
from torchvision import transforms
import cv2
from torchvision import utils as vutils
import subprocess
import tempfile
import re
from tqdm import tqdm
import time
import predict

app = Flask(__name__)


# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 3600
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db = SQL("sqlite:///data.db")


# Ensure templates are auto reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/change", methods=["GET", "POST"])
def change():
    if request.method == "GET":
        return render_template("change_password.html")
    elif request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        old = request.form.get("old")
        new_password = request.form.get("new_password")
        new_confirm = request.form.get("new_confirm")

        # Sanity Checks
        rows = db.execute(
            "SELECT * FROM users WHERE username = :username;", username=username)

        if not rows:
            return apology("Sorry an error has occured")
            # return render_template("apology.html", message="Sorry an error has occured")

        if not len(rows) == 1 or not check_password_hash(rows[0]["hash"], old):
            return apology("Sorry, Error in Password")
            # return render_template("apology.html", message="Sorry, Error in Password")

        rows = db.execute("UPDATE users SET hash = :hash WHERE username = :username;",
                          hash=generate_password_hash(new_password), username=username)

        if not rows:
            return apology("Unable to Change Password")
            # return render_template("apology.html", message="Unable to Change Password")

        # send email to the user"
        message = "Password has been changed!"
        return render_template("success.html", message=message)


@app.route("/confirm_registration/<reg_link>", methods=["GET", "POST"])
def confirm_reg(reg_link):
    reg_link = website + "confirm_registration/" + reg_link
    if request.method == "GET":
        file = open("tmp_users", "r")
        l = list(file)
        file.close()

        user_found = False

        for i in range(len(l)):
            l[i] = l[i].split(",")
            if l[i][0] == reg_link:
                username = l[i][1]
                email = l[i][2]
                hashed_password = l[i][3]
                time = l[i][4]
                fname = l[i][5]
                lname = l[i][6]
                user_found = True
                break

        if user_found:
            status = db.execute("INSERT INTO users (username, email, hash, time) VALUES (:username, :email, :hash, :time);",
                                username=username, email=email, hash=hashed_password, time=time)
            print(status)
            if not status:
                return "Username or Email is already registered!"

            rows = db.execute(
                "SELECT * FROM users where username = :username;", username=username)

            id = rows[0]["id"]

            status2 = db.execute(
                "INSERT INTO profile (id, fname, lname) VALUES (:id, :fname, :lname);", id=id, fname=fname, lname=lname)

            home_dir = "./users/" + username
            createFolder(home_dir)

            jobs_dir = home_dir + "/jobs"
            createFolder(jobs_dir)

            tmp_dir = home_dir + "/tmp"
            createFolder(tmp_dir)

            print(rows)

            if not len(rows) == 1:
                return "Invalid username and/or password"

            session["user_id"] = rows[0]["id"]
            return render_template("success.html", message="You are successfully registered!")
        else:
            return apology("User Not Found!")
            # return render_template("apology.html", message="User Not Found!")


@app.route("/contact", methods=["GET"])
def contact():
    return render_template("contact.html")


@app.route("/jobs", methods=["GET", "POST"])
@login_required
def jobs():
    if request.method == "GET":
        id = session["user_id"]
        rows = db.execute(
            "SELECT * FROM jobs WHERE user_id = :user_id", user_id=id)
        return render_template("jobs.html", myjobs=rows)

    elif request.method == "POST":

        id = session["user_id"]

        rows = db.execute("SELECT * FROM users where id = :id;", id=id)

        file_count = int(request.form.get("file_count"))
        print(file_count)
        # Store the files in the username/tmp folder
        # then check if the files arer of coorect type and not malicious
        # then assign a job id

        file_names = ["file_{}".format(i) for i in range(file_count)]
        print(file_names)

        username = rows[0]["username"]

        UPLOAD_FOLDER = './users/' + username + "/tmp"
        print(UPLOAD_FOLDER)
        ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

        def allowed_file(filename):
            return '.' in filename and \
                   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

        # check if the post request has the file part
        for file_name in file_names:
            if file_name not in request.files:
                flash('No file part')
                return redirect("/")

        for file_name in file_names:
            print(file_name)
            file = request.files[file_name]
            actual_file_name = file.filename
            print(actual_file_name)
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect("/about")
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        time = datetime.datetime.now(pytz.timezone(
            'Asia/Calcutta')).strftime('%Y-%m-%d %H:%M:%S')
        status = db.execute("INSERT INTO jobs (user_id, file_count, time) VALUES (:user_id, :file_count, :time);",
                            user_id=id, file_count=file_count, time=time)
        if not status:
            return apology("Can't create a job!")
            # return render_template("apology.html", message="Can't create a job!")

        rows = db.execute(
            "SELECT * FROM jobs WHERE user_id = :user_id AND time = :time;", user_id=id, time=time)

        job_id = rows[0]["job_id"]

        home_dir = "./users/" + username

        jobs_id_dir = home_dir + "/jobs/" + str(job_id) + "/"
        jobs_id_input_dir = home_dir + "/jobs/" + str(job_id) + "/" "input" + "/"
        jobs_id_output_dir = home_dir + "/jobs/" + str(job_id) + "/" "output" + "/"
        createFolder(jobs_id_dir)
        createFolder(jobs_id_input_dir)
        createFolder(jobs_id_output_dir)

        UPLOAD_FOLDER = jobs_id_input_dir
        print(UPLOAD_FOLDER)

        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

        print("I am here!")
        for file_name in file_names:
            print(file_name)
            file = request.files[file_name]
            actual_file_name = file.filename
            print(actual_file_name)
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect("/about")
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.stream.seek(0)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        tmp_directory = './users/' + username + "/tmp"
        clearFolderContents(tmp_directory)

        path, dirs, files = next(os.walk(UPLOAD_FOLDER))
        print(files)
        # cartoonize(files[0])
        
        return render_template("success.html", message="The job has been create and the JOBID is {}".format(job_id))

def cartoonize(input_path, output_path, user_stated_device="cpu", batch_size=4):

    # input_path, output_path, user_stated_device, batch_size = vars(parser.parse_args()).values()
    device = torch.device(user_stated_device)
    pretrained_dir = "./checkpoints/trained_netG.pth"
    netG = Generator().to(device)
    netG.eval()

    netG.load_state_dict(torch.load(pretrained_dir, map_location=torch.device('cpu')))
    predict.predict_file(input_path, output_path)

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return apology("Must Provide Username")
            # return render_template("apology.html", message="Must Provide Username")
        elif not password:
            return apology("Must Provide Password")
            # return render_template("apology.html", message="Must Provide Password")

        rows = db.execute(
            "SELECT * FROM users WHERE username = :username", username=username)

        if not rows:
            return apology("Invalid Username")
            # return render_template("apology.html", message="Invalid Username")
        # Put same error message at both places to maintain anonymity
        if (not len(rows) == 1) or not check_password_hash(rows[0]["hash"], password):
            return apology("Incorrect Password")
            # return render_template("apology.html", message="Incorrect Password")

        session["user_id"] = rows[0]["id"]

        return redirect("/")


@app.route("/logout")
def logout():
    session.clear()

    return redirect("/")


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    id = session["user_id"]
    if request.method == "GET":
        rows = db.execute("SELECT * FROM users WHERE id = :id;", id=id)
        rows2 = db.execute("SELECT * FROM profile WHERE id = :id;", id=id)

        fname = rows2[0]["fname"]
        lname = rows2[0]["lname"]

        username = rows[0]["username"]
        email = rows[0]["email"]

        return render_template("profile.html", fname=fname, lname=lname, username=username, email=email)


@app.route("/queue", methods=["GET"])
def queue():
    rows = db.execute("SELECT job_id, file_count, time FROM jobs;")
    return render_template("queue.html", jobs=rows)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        session.clear()
        return render_template("register.html")
    else:
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        if not username:
            return "username not entered"
        elif not email:
            return "email not entered"
        elif not password:
            return "password not entered"
        elif not confirm:
            return "confirm password not entered"
        elif password != confirm:
            return "passwrod and confirm passwrod are not same"
        elif not fname:
            return "first name not entered."
        elif not lname:
            return "last name not entered."

        hashed_password = generate_password_hash(password)

        time = datetime.datetime.now(pytz.timezone(
            'Asia/Calcutta')).strftime('%Y-%m-%d %H:%M:%S')

        secret_key = secrets.token_hex(nbytes=32)
        verif_link = website + "confirm_registration/" + secret_key

        file = open("tmp_users", "a")
        file.write(str(verif_link) + "," + str(username) + "," + str(email) + "," + str(
            hashed_password) + "," + str(time) + "," + str(fname) + "," + str(lname) + "," + "\n")
        file.close()
        send_mail(fname, email, verif_link, "new_user")

        return render_template("success.html", message="Please check your email to confirm registeration.")

        # status = db.execute("INSERT INTO users (username, email, hash, time) VALUES (:username, :email, :hash, :time);", username=username, email=email, hash=hashed_password, time=time)
        # print(status)
        # if not status:
        #     return "Username or Email is already registered!"
        #
        # rows = db.execute("SELECT * FROM users where username = :username;", username=username)
        #
        # home_dir = "./users/" + username
        # createFolder(home_dir)
        #
        # jobs_dir = home_dir + "/jobs"
        # createFolder(jobs_dir)
        #
        # tmp_dir = home_dir + "/tmp"
        # createFolder(tmp_dir)
        #
        # print(rows)
        #
        # if not len(rows) == 1:
        #     return "Invalid username and/or password"
        #
        # session["user_id"] = rows[0]["id"]
        # return redirect("/")


@app.route("/reset", methods=["GET", "POST"])
def reset():
    if request.method == "GET":
        return render_template("reset.html")
    elif request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
# Check if username and email are in datababse
        rows = db.execute(
            "SELECT * FROM users WHERE username = :username", username=username)

        if not rows:
            return apology("Invalid Username")
            # return render_template("apology.html", message="Invalid Username")
        # Put same error message at both places to maintain anonymity
        if (not len(rows) == 1):
            return apology("Unknown Error!")
            # return render_template("apology.html", message="Unknown Error!")

        if not email == rows[0]["email"]:
            return apology("Incorrect Email")
            # return render_template("apology.html", message="Incorrect Email")

        user_id = rows[0]["id"]

        rows2 = db.execute("SELECT * FROM profile WHERE id = :id", id=user_id)

        fname = rows2[0]["fname"]

        secret_key = secrets.token_hex(nbytes=32)
        time = datetime.datetime.now(pytz.timezone('Asia/Calcutta'))
        # print(str(secret_key))

        file = open("./reset/tokens", "a")
        file.write(secret_key+","+str(time)+","+str(user_id)+"\n")
        file.close()

        # import sys
        # sys.path.insert(0, '/mailing')
        # sys.path.append('../')

        token_link = website + "reset_link/" + secret_key
        send_mail(fname, email, token_link, "forgot")
        return render_template("success.html", message="An Email has been sent to the email ID provided.")


@app.route("/reset_link/<token>", methods=["GET", "POST"])
def reset_links(token):
    if request.method == "GET":
        file = open("./reset/tokens", "r")
        l = list(file)
        file.close()

        for i in range(len(l)):
            l[i] = l[i].split(",")
            if token in l[i][0]:
                print(token)
                return render_template("reset2.html", token=token)

        return apology("Sorry, please try again to reset the password.")
        # return render_template("apology.html", message="Sorry, please try again to reset the password.")

    elif request.method == "POST":
        new_password = request.form.get("password")
        new_confirm = request.form.get("confirm")

        if new_password != new_confirm:
            return apology("Passwords do not match.")
            # return render_template("apology.html", message="Passwords don not match.")

        file = open("./reset/tokens", "r")
        l = list(file)
        file.close()

        sent_time = ""
        user_id = ""

        for i in range(len(l)):
            l[i] = l[i].split(",")
            if token in l[i][0]:
                sent_time = l[i][1]
                user_id = l[i][2]

                # if time is less than 30 minutes, then continue

        # email = rows[0]["email"]
        # username = request.form.get("username")
        # old = request.form.get("old")
        # new_password = request.form.get("new_password")
        # new_confirm = request.form.get("new_confirm")

        # Sanity Checks
        rows = db.execute("SELECT * FROM users WHERE id = :id;", id=user_id)

        if not rows:
            return apology("Sorry an error has occured")
            # return render_template("apology.html", message="Sorry an error has occured")

        rows = db.execute("UPDATE users SET hash = :hash WHERE id = :id;",
                          hash=generate_password_hash(new_password), id=user_id)

        if not rows:
            return apology("Unable to Change Password")
            return render_template("apology.html", message="Unable to Change Password")

        # send email to the user"
        message = "Password has been changed!"
        session["user_id"] = user_id
        return render_template("success.html", message=message)


@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "GET":
        return redirect("/jobs")
    elif request.method == "POST":
        # Error checking
        file_count = request.form.get("file_count")
        file_count = int(file_count)
        if not file_count:
            return render_template("apology.html", message="Invalid Input")

        return render_template("upload.html", file_count=file_count)
