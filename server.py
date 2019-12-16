from flask import Flask

import os

import psycopg2 as dbapi2
        
import views
import views_h
import views_g

app=Flask(__name__)
app.config["DEBUG"] = True
    
app.add_url_rule("/", methods=["GET", "POST"], view_func=views.home_page)
app.add_url_rule("/login", view_func=views.login_page)

app.add_url_rule("/meetings", view_func=views_g.meetings_page)
app.add_url_rule("/meetings_add", methods=["GET", "POST"], view_func=views_g.meetings_add_page)
app.add_url_rule("/meetings_remove", methods=["GET", "POST"], view_func=views_g.meetings_remove_page)
app.add_url_rule("/meetings_remove_<int:id>", methods=["GET", "POST"], view_func=views_g.meetings_remove)
app.add_url_rule("/meetings_update", methods=["GET", "POST"], view_func=views_g.meetings_update_find_page)
app.add_url_rule("/meetings_update_<int:id>", methods=["GET", "POST"], view_func=views_g.meetings_update_change_page)

app.add_url_rule("/tech", view_func=views_g.tech_page)
app.add_url_rule("/tech_add", methods=["GET", "POST"], view_func=views_g.tech_add_page)
app.add_url_rule("/tech_remove", methods=["GET", "POST"], view_func=views_g.tech_remove_page)
app.add_url_rule("/tech_remove_<string:name>", methods=["GET", "POST"], view_func=views_g.tech_remove)
app.add_url_rule("/tech_update", methods=["GET", "POST"], view_func=views_g.tech_update_find_page)
app.add_url_rule("/tech_update_<string:name>", methods=["GET", "POST"], view_func=views_g.tech_update_change_page)
app.add_url_rule("/tech_upload", view_func=views_g.tech_upload_page)
app.add_url_rule("/tech_upload_success", methods=["POST"], view_func=views_g.tech_upload_success_page)
app.add_url_rule("/tech_download", view_func=views_g.tech_download_page)

app.add_url_rule("/departments", view_func=views_g.departments_page)
app.add_url_rule("/departments_add", methods=["GET", "POST"], view_func=views_g.departments_add_page)
app.add_url_rule("/departments_remove", methods=["GET", "POST"], view_func=views_g.departments_remove_page)
app.add_url_rule("/departments_remove_<string:department_name>", methods=["GET", "POST"], view_func=views_g.departments_remove)
app.add_url_rule("/departments_update", methods=["GET", "POST"], view_func=views_g.departments_update_find_page)
app.add_url_rule("/departments_update_<string:department_name>", methods=["GET", "POST"], view_func=views_g.departments_update_change_page)

app.add_url_rule("/personnel", view_func=views_h.personnel_page)
app.add_url_rule("/personnel_add", methods=["GET", "POST"], view_func=views_h.personnel_add_page)
app.add_url_rule("/personnel_update", methods=["GET", "POST"], view_func=views_h.personnel_update_find_page)
app.add_url_rule("/personnel_update_<int:id>", methods=["GET", "POST"], view_func=views_h.personnel_update_change_page)
app.add_url_rule("/personnel_remove_<int:id>", methods=["GET", "POST"], view_func=views_h.personnel_remove)

app.add_url_rule("/participants", view_func=views_h.participants_page)
app.add_url_rule("/participants_remove_<int:Meeting_ID>_<int:Person_ID>", methods=["GET", "POST"], view_func=views_h.participants_remove)

app.add_url_rule("/places", view_func=views_h.places_page)
app.add_url_rule("/places_add", methods=["GET", "POST"], view_func=views_h.places_add_page)
app.add_url_rule("/places_update", methods=["GET", "POST"], view_func=views_h.places_update_find_page)
app.add_url_rule("/places_update_<int:id>", methods=["GET", "POST"], view_func=views_h.places_update_change_page)
app.add_url_rule("/places_remove_<int:id>", methods=["GET", "POST"], view_func=views_h.places_remove)

#app.add_url_rule(, view_func=views_g.tech_)

#def create_app():
#    app=Flask(__name__)
#    #app.config["DEBUG"] = True
#    
#    app.add_url_rule("/", view_func=views.home_page)
#    app.add_url_rule("/login", view_func=views.login_page)
#    
#    app.add_url_rule("/meetings", view_func=views_g.meetings_page)
#    app.add_url_rule("/meetings_add", methods=["GET", "POST"], view_func=views_g.meetings_add_page)
#    app.add_url_rule("/meetings_remove_<int:id>", methods=["GET", "POST"], view_func=views_g.meetings_remove)
#    app.add_url_rule("/meetings_remove", methods=["GET", "POST"], view_func=views_g.meetings_remove_page)
#    app.add_url_rule("/meetings_update", methods=["GET", "POST"], view_func=views_g.meetings_update_find_page)
#    app.add_url_rule("/meetings_update_<int:id>", methods=["GET", "POST"], view_func=views_g.meetings_update_change_page)
##    app.add_url_rule(, view_func=views_g.meetings_)
##    app.add_url_rule(, view_func=views_g.meetings_)
#    
#    return app
    
#def write_blob(table_name, attribute, path_to_file, file_extension):
#    file = open(path_to_file, 'rb').read()
#    url= DATABASE_URL
#    with dbapi2.connect(url) as connection:
#        cursor = connection.cursor()
#        cursor.execute("""INSERT INTO %s(%s) 
#                            VALUES (%s);""" % (table_name, attribute, dbapi2.Binary(file)))
#        cursor.close()

#def read_blob(table_name, attribute, path_to_dir):
#    url= DATABASE_URL
#    with dbapi2.connect(url) as connection:
#        cursor = connection.cursor()
#        cursor.execute(""" SELECT %s FROM %s
#                       """)
#        cursor.close()

if __name__ == "__main__":
#    app = create_app()
    app.run()
