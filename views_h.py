from flask import render_template
from flask import request, redirect, url_for

import psycopg2 as dbapi2

import os

DATABASE_URL = os.environ['DATABASE_URL']

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

def validate_personnel_form(form):
    form.data = {}
    form.errors = {}
    
    form_topic = form.get("Phone_Number", "").strip()
    if len(form_topic) != 13:
        form.errors["Phone_Number"] = "Phone Number must be 13 characters long."
    else:
        form.data["Phone_Number"] = form_topic

    return len(form.errors) == 0

def personnel_add_page():
    departments_row= query(DATABASE_URL, "DEPARTMENTS")
    departments_ids =[]
    length_departments=len(departments_row)
    
    for department in range(0, length_departments):
        departments_ids.append(departments_row[department][0])
        
    if request.method == "GET":
        values = {"Phone_Number":""}
        return render_template(
            "personnel_add.html" , values=values, length_departments=length_departments, departments_ids=departments_ids
        )
    else:
        valid = validate_personnel_form(request.form)
        if not valid:
            return render_template("personnel_add.html", values=request.form, length_departments=length_departments, departments_ids=departments_ids
            )
        
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

    departments_row= query(DATABASE_URL, "DEPARTMENTS")
    departments_ids =[]
    length_departments=len(departments_row)
    
    for department in range(0, length_departments):
        departments_ids.append(departments_row[department][0])

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
            "personnel_update_change.html", row=row, values=values ,  length_departments=length_departments, departments_ids=departments_ids
        )
    else:
    
        form_ID = id
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
        STATEMENTS = ['''   DELETE FROM PARTICIPANTS
                                  WHERE (Person_ID=%s);
                              DELETE FROM PERSONNEL
                                  WHERE (ID=%s); ''' % (id,id)]

        url= DATABASE_URL
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            for statement in STATEMENTS:
                cursor.execute(statement)

            cursor.close()

        return redirect(url_for("personnel_page"))
        
def personnel_remove_page():
    
    personnel_row = query(DATABASE_URL, "PERSONNEL")        
    personnel_list =[]
    personnel_ids=[]
    length=len(personnel_row)
    
    for personnel in range(0, length):
        personnel_list.append(personnel_row[personnel][1]+' '+personnel_row[personnel][2])
        personnel_ids.append(personnel_row[personnel][0])
        
    
    if request.method == "GET":
        return render_template(
            "personnel_remove.html", personnel_list=personnel_list, personnel_ids=personnel_ids, length=length,                              
        )
    else:
        form_personnel = request.form.getlist("personnellist")        
        
        remove_personnel(form_personnel)
        
        return redirect(url_for("personnel_page"))

def remove_personnel(personnellist):
    STATEMENTS=[]
    for personel in personnellist:
        print(personel)
        STATEMENTS.append("DELETE FROM PARTICIPANTS WHERE (Person_ID=%s);DELETE FROM PERSONNEL WHERE (ID=%s);" % (int(personel),int(personel)) )
    url= DATABASE_URL
    with dbapi2.connect(url) as connection:
       cursor = connection.cursor()
       for statement in STATEMENTS:
           cursor.execute(statement)
    
       cursor.close()
       
def personnel_upload_page(name):
    return render_template("personnel_upload.html", name=name)

def personnel_upload_success_page(name):  
    if request.method == 'POST':  
        form_file = request.files['file']  
        form_file.save(form_file.filename)
        file = open(form_file.filename, 'rb').read()
        
        url= DATABASE_URL
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute('''
                      UPDATE PERSONNEL
                          SET Pictures=%s
                          WHERE name='%s'; ''' % (dbapi2.Binary(file), name) )
            cursor.close()
      
        return redirect(url_for("personnel_page")) 

def personnel_download_page(name):
    url= DATABASE_URL
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(''' SELECT Pictures FROM PERSONNEL 
                       WHERE NAME='%s';''' % (name) )
        
    blob = cursor.fetchone()
    open('./static/downloaded_file_'+name+'.jpeg', 'wb').write(blob[0])

    return render_template("personnel_download.html", name=name)
       
### PARTICIPANTS

def participants_page():
    rows = query(DATABASE_URL, "PARTICIPANTS")
    return render_template("participants.html", rows=sorted(rows), len=len(rows))
    
def participants_remove(Meeting_ID,Person_ID):
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
        
def participants_update_change_page(Meeting_ID,Person_ID):

    if request.method == "GET":
        STATEMENTS = [ '''
                      SELECT * FROM PARTICIPANTS
                          WHERE (Meeting_ID=%s AND Person_ID=%s); ''' % (Meeting_ID,Person_ID)  ]
            
        url= DATABASE_URL
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            for statement in STATEMENTS:
                cursor.execute(statement)
                values = {"id":""}
            row = cursor.fetchone()
        return render_template(
            "participants_update_change.html", row=row, values=values
        )
    else:
    
        form_Meeting_ID = Meeting_ID
        form_Person_ID = Person_ID
        form_Role = request.form["Role"]
        form_Attendance = request.form["Attendance"]
        form_Performance = request.form["Performance"]
        
        STATEMENTS = [ '''
                      UPDATE PARTICIPANTS
                          SET Role='%s', Attendance='%s', Performance='%s'
                          WHERE (Meeting_ID=%s AND Person_ID=%s); ''' % (form_Role, form_Attendance, form_Performance, form_Meeting_ID, form_Person_ID)  ]
        
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
    departments_row= query(DATABASE_URL, "DEPARTMENTS")
    departments_ids =[]
    length_departments=len(departments_row)
    
    for department in range(0, length_departments):
        departments_ids.append(departments_row[department][0])
        
    if request.method == "GET":
        return render_template(
            "place_add.html" ,  length_departments=length_departments, departments_ids=departments_ids
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
    departments_row= query(DATABASE_URL, "DEPARTMENTS")
    departments_ids =[]
    length_departments=len(departments_row)
    
    for department in range(0, length_departments):
        departments_ids.append(departments_row[department][0])


    if request.method == "GET":
        STATEMENTS = [ '''
                      SELECT * FROM PLACES
                          WHERE (ID=%s); ''' % (id)  ]
            
        url= DATABASE_URL
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            for statement in STATEMENTS:
                cursor.execute(statement)
            values = {"id":""}
            row = cursor.fetchone()
        return render_template(
            "place_update_change.html", row=row, values=values,  length_departments=length_departments, departments_ids=departments_ids
        )
    else:
        form_ID = id
        form_Type = request.form["Type"]
        form_Department = request.form["Department"]
        form_Location = request.form["Location"]
        form_Capacity = request.form["Capacity"]
        
        STATEMENTS = [ '''
                      UPDATE PLACES
                          SET Type='%s', Department='%s', Location='%s', Capacity=%s
                          WHERE ID=%s; ''' % (form_Type, form_Department, form_Location, form_Capacity, form_ID)  ]
        
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
        