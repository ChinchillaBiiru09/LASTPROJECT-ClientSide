from flask import Flask, render_template, url_for, redirect, flash, session, request
from dotenv import load_dotenv
import os

load_dotenv()  # read env file
app = Flask(__name__)

# CONFIGURATION APP ============================================================ Begin
### Set Config ======================================== 
app.config['BASE_URL'] = os.getenv('BASE_URL')
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['BE_URL'] = os.getenv('BE_URL')
app.config['SESSION_TYPE'] = 'mamecached'

### Set Title App ========================================
TITLE_HOME = os.getenv('TITLE_HOME')
TITLE_DASHBD = os.getenv('TITLE_DASHBD')
### Import Navigation ======================================== 
# from apps.routes.Dashboard import Navigation

### Register Setting Navigation ======================================== 
# app.config['navigation'] = Navigation
# CONFIGURATION APP ============================================================ End


# BLUEPRINT ============================================================ Begin
## Import Blueprint ---------------------------------------- Start
from apps.routes.Home import home
from apps.routes.Auth import auth
from apps.routes.Dashboard import dashboard
## Import Blueprint ---------------------------------------- Finish

## Register Blueprint ---------------------------------------- Start
app.register_blueprint(home)
app.register_blueprint(auth)
app.register_blueprint(dashboard)
## Register Blueprint ---------------------------------------- Finish
# BLUEPRINT ============================================================ End


# ROUTING ============================================================ Begin
## Route Home ---------------------------------------- Start
@app.route('/')
def home():
    return render_template (
        title=TITLE_HOME,
        template_name_or_list='pages/index.html'
    )
## Route Home ---------------------------------------- Finish

## Route LogOut ---------------------------------------- Start
@app.route('/logout')
def logout():
    if (session.get('user') != None):
        session.pop('user')
        session.clear()
        if request.args.get("message") != None:
            flash(
                message=request.args.get("message"),
                category='danger'
            )
    return redirect(url_for('Auth.login'))
## Route LogOut ---------------------------------------- Finish

## Route Not Found ---------------------------------------- Start
@app.errorhandler(404)
def page_not_found(e):
    return render_template("layout/page_not_found.html")
## Route Not Found ---------------------------------------- Finish
# ROUTING ============================================================ End
