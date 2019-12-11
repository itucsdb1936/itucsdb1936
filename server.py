from flask import Flask

import os

import psycopg2 as dbapi2
        
import views
import views_h
import views_g

def create_app():
    app=Flask(__name__)
    #app.config["DEBUG"] = True
    
    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/login", view_func=views.login_page)
    
    app.add_url_rule("/meetings", view_func=views_g.meetings_page)
    app.add_url_rule("/meetings_add", methods=["GET", "POST"], view_func=views_g.meetings_add_page)
    app.add_url_rule("/meetings_remove_<int:id>", methods=["GET", "POST"], view_func=views_g.meetings_remove)
    app.add_url_rule("/meetings_remove", methods=["GET", "POST"], view_func=views_g.meetings_remove_page)
    app.add_url_rule("/meetings_update", methods=["GET", "POST"], view_func=views_g.meetings_update_find_page)
    app.add_url_rule("/meetings_update_<int:id>", methods=["GET", "POST"], view_func=views_g.meetings_update_change_page)
#    app.add_url_rule(, view_func=views_g.meetings_)
#    app.add_url_rule(, view_func=views_g.meetings_)
    
    return app
    
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
    app = create_app()
    app.run(port=5000)
