from datetime import datetime
from flask import render_template
from flask import request, redirect, url_for

import os

import psycopg2 as dbapi2

#DATABASE_URL = os.environ['DATABASE_URL']
DATABASE_URL= "postgres://gvoybackrspqkf:339af7eacd4af135d7f93ef0df5dd3e25623e2a68da06335f5dc75855628fe95@ec2-54-247-171-30.eu-west-1.compute.amazonaws.com:5432/d7iva2beg4i1l0"

def query(url, table_name):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM %s" % (table_name))
        rows = cursor.fetchall()
        
        cursor.close()
        return rows

def validate_comments_form(form):
    form.data = {}
    form.errors = {}

    form_name = form.get("name", "").strip()
    form_name.replace("\n"," ")
    form_name.replace("\'","")
    if len(form_name) == 0:
        form.errors["name"] = "Name can not be blank."
    else:
        form.data["name"] = form_name
        
    form_comment = form.get("comment", "").strip()
    form_comment.replace("'","")
    if len(form_comment) == 0:
        form.errors["comment"] = "Comment can not be blank."
    else:
        form.data["comment"] = form_name
        
    form_score = form.get("score")
    if not form_score:
        form.data["score"] = None
    elif not form_score.isdigit():
        form.errors["score"] = "Score can not be blank!."
    else:
        score = int(form_score)
        if (score < 0) or (score > 5):
            form.errors["score"] = "Score not in valid range."
        else:
            form.data["score"] = score

    return len(form.errors) == 0

def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    rows = query(DATABASE_URL, "COMMENTS")
    
    if request.method == "GET":
        values = {"commentid":"","name":"","comment":"","score":""}
        return render_template("home.html", day=day_name, rows=sorted(rows), len=len(rows), values=values)
    else:
        valid = validate_comments_form(request.form)
        if not valid:
            return render_template("home.html", day=day_name, rows=sorted(rows), len=len(rows), values=request.form)
        
        form_name = request.form["name"]
        form_comment = request.form["comment"]
        form_comment=form_comment.replace("\'","")
        #form_comment=form_comment.decode('UTF-8','strict')
        form_score = request.form["score"]
        
        STATEMENTS = [ '''
                      INSERT INTO COMMENTS VALUES
                          (DEFAULT, '%s', '%s', %s); ''' % (form_name, form_comment, form_score)  ]
        
        url= DATABASE_URL
        with dbapi2.connect(url) as connection:
           cursor = connection.cursor()
           for statement in STATEMENTS:
               cursor.execute(statement)
        
           cursor.close()
           
    values = {"commentid":"","name":"","comment":"","score":""}
    return redirect(url_for("home_page"))

def login_page():
    return render_template("login.html")






























