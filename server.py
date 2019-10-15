#from flask import Flask
#
#
#app = Flask(__name__)
#
#
#@app.route("/")
#def home_page():
#    return "Hello, ITU!"
##This is going well
#
#if __name__ == "__main__":
#    app.run()

from flask import Flask

from flask import render_template

from datetime import datetime

#import views

app=Flask(__name__)

@app.route("/")
def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=day_name)
    
#def create_app():
#    app = Flask(__name__)
#    app.config.from_object("settings")
#
#    app.add_url_rule("/", view_func=views.home_page)
#
#    return app


if __name__ == "__main__":
    #app = create_app()
    #port = app.config.get("PORT", 8080)
    app.run()