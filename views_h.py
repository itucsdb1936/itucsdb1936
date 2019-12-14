from flask import render_template
from flask import request, redirect, url_for

import psycopg2 as dbapi2

import os

#DATABASE_URL = os.environ['DATABASE_URL']
DATABASE_URL= "postgres://gvoybackrspqkf:339af7eacd4af135d7f93ef0df5dd3e25623e2a68da06335f5dc75855628fe95@ec2-54-247-171-30.eu-west-1.compute.amazonaws.com:5432/d7iva2beg4i1l0"

def query(url, table_name):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM %s" % (table_name))
        rows = cursor.fetchall()
        
        cursor.close()
        return rows

### PERSONNEL

def personnel_page():
    rows = query(DATABASE_URL, "PERSONNEL")
    return render_template("personnel.html", rows=sorted(rows), len=len(rows))

def personnel_add_page():
    if request.method == "GET":
        return render_template(
            "personnel_add.html"
        )
    else:
        form_Name = request.form["Name"]
        form_Surname = request.form["Surname"]
        form_Department = request.form["Department"]
        form_Professional_Title = request.form["Professional_Title"]
        form_Phone_Number = request.form["Phone_Number"]
        form_Email_Address = request.form["Email_Address"]
        
        STATEMENTS = [ '''
                      INSERT INTO PERSONNEL VALUES
                          (DEFAULT, '%s', '%s', '%s', '%s', '%s', '%s'); ''' % (form_Name, form_Surname, form_Department, form_Professional_Title, form_Phone_Number, form_Email_Address)  ]
        
        url= DATABASE_URL
        with dbapi2.connect(url) as connection:
           cursor = connection.cursor()
           for statement in STATEMENTS:
               cursor.execute(statement)
        
           cursor.close()
        
        return redirect(url_for("personnel_page"))
        
def personnel_update_find_page():
    if request.method == "GET":
        values = {"id":""}
        return render_template(
            "personnel_update_find.html", values=values
        )
    else:
        valid = validate_meetings_form(request.form)
        if not valid:
            return render_template("personnel_update_find.html", values=request.form)
        
        form_id = request.form["id"]
        
        return redirect(url_for("personnel_update_change_page", id=form_id))
        
def personnel_update_change_page(id):
    if request.method == "GET":
        STATEMENTS = [ '''
                      SELECT * FROM PERSONNEL
                          WHERE (ID=%s); ''' % (id)  ]
            
        url= DATABASE_URL
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            for statement in STATEMENTS:
                cursor.execute(statement)
                values = {"id":""}
            row = cursor.fetchone()
        return render_template(
            "personnel_update_change.html", row=row, values=values
        )
    else:
    
        form_ID = request.form["id"]
        form_Name = request.form["Name"]
        form_Surname = request.form["Surname"]
        form_Department = request.form["Department"]
        form_Professional_Title = request.form["Professional_Title"]
        form_Phone_Number = request.form["Phone_Number"]
        form_Email_Address = request.form["Email_Address"]
        
        STATEMENTS = [ '''
                      UPDATE PERSONNEL
                          SET Name='%s', Surname='%s', Department='%s', Professional_Title='%s', Phone_Number='%s', Email_Address='%s'
                          WHERE ID=%s; ''' % (form_Name, form_Surname, form_Department, form_Professional_Title, form_Phone_Number, form_Email_Address, form_ID)  ]
        
        url= DATABASE_URL
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            for statement in STATEMENTS:
                cursor.execute(statement)
        
            cursor.close()
        
        return redirect(url_for("personnel_page"))
        
def personnel_remove(id):
        STATEMENTS = ['''
                              DELETE FROM PERSONNEL
                                  WHERE (ID=%s); ''' % (id)]

        url= DATABASE_URL
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            for statement in STATEMENTS:
                cursor.execute(statement)

            cursor.close()

        return redirect(url_for("personnel_page"))
        
### PARTICIPANTS

def participants_page():
    rows = query(DATABASE_URL, "PARTICIPANTS")
    return render_template("participants.html", rows=sorted(rows), len=len(rows))
    
def participants_remove(meeting):
        STATEMENTS = ['''
                              DELETE FROM PARTICIPANTS
                                  WHERE (Meeting_ID=%s AND Person_ID=%s); ''' % (Meeting_ID,Person_ID)]

        url= DATABASE_URL
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            for statement in STATEMENTS:
                cursor.execute(statement)

            cursor.close()

        return redirect(url_for("participants_page"))
    
### PLACES

def places_page():
    rows = query(DATABASE_URL, "PLACES")
    return render_template("places.html", rows=sorted(rows), len=len(rows))

def places_add_page():
    if request.method == "GET":
        return render_template(
            "place_add.html"
        )
    else:
        form_Type = request.form["Type"]
        form_Department = request.form["Department"]
        form_Location = request.form["Location"]
        form_Capacity = request.form["Capacity"]
        
        STATEMENTS = [ '''
                      INSERT INTO PLACES VALUES
                          (DEFAULT, '%s', '%s', '%s', %s); ''' % (form_Type, form_Department, form_Location, form_Capacity)  ]
        
        url= DATABASE_URL
        with dbapi2.connect(url) as connection:
           cursor = connection.cursor()
           for statement in STATEMENTS:
               cursor.execute(statement)
        
           cursor.close()
        
        return redirect(url_for("places_page"))
        
def places_update_find_page():
    if request.method == "GET":
        values = {"id":""}
        return render_template(
            "place_update_find.html", values=values
        )
    else:
        valid = validate_meetings_form(request.form)
        if not valid:
            return render_template("places_update_find.html", values=request.form)
        
        form_id = request.form["id"]
        
        return redirect(url_for("places_update_change_page", id=form_id))        
        
def places_update_change_page(id):
    if request.method == "GET":
        STATEMENTS = [ '''
                      SELECT * FROM PLACES
                          WHERE (ID=%s); ''' % (id)  ]
            
        url= DATABASE_URL
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            for statement in STATEMENTS:
                cursor.execute(statement)
                
            row = cursor.fetchone()
        return render_template(
            "place_update_change.html", row=row
        )
    else:
        form_ID = request.form["id"]
        form_Type = request.form["Type"]
        form_Department = request.form["Department"]
        form_Location = request.form["Location"]
        form_Capacity = request.form["Capacity"]
        
        STATEMENTS = [ '''
                      UPDATE PERSONNEL
                          SET Type='%s', Department='%s', Location='%s', Capacity=%s
                          WHERE ID=%s; ''' % (form_Type, form_Department, form_Location, form_ID)  ]
        
        url= DATABASE_URL
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            for statement in STATEMENTS:
                cursor.execute(statement)
        
            cursor.close()
        
        return redirect(url_for("places_page"))
        
def places_remove(id):
        STATEMENTS = ['''
                              DELETE FROM PLACES
                                  WHERE (ID=%s); ''' % (id)]

        url= DATABASE_URL
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            for statement in STATEMENTS:
                cursor.execute(statement)

            cursor.close()

        return redirect(url_for("places_page"))
        