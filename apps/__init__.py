from flask import Flask, render_template, url_for, redirect, flash, session, request
from dotenv import load_dotenv
from flask_cors import CORS
import os

load_dotenv()  # read env file
app = Flask(__name__)
CORS(app)  # Mengizinkan semua asal secara default

# CONFIGURATION APP ============================================================ Begin
### Set Config ======================================== 
# app.config['BASE_URL'] = os.getenv('BASE_URL')
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['BE_URL'] = os.getenv('BE_URL')
app.config['FE_URL'] = os.getenv('FE_URL')
app.config['SESSION_TYPE'] = 'mamecached'

### Set Title App ========================================
TITLE_HOME = os.getenv('TITLE_HOME')
TITLE_DASHBD = os.getenv('TITLE_DASHBD')
TITLE_SIGNIN = os.getenv('TITLE_SIGNIN')
TITLE_SIGNUP = os.getenv('TITLE_SIGNUP')

### Import Navigation ======================================== 
# from apps.routes.Dashboard import Navigation

### Register Setting Navigation ======================================== 
# app.config['navigation'] = Navigation
# CONFIGURATION APP ============================================================ End


# BLUEPRINT ============================================================ Begin
## Import Blueprint ---------------------------------------- Start
from apps.routes.Auth import auth
from apps.routes.Dashboard import dashboard
from apps.routes.Management import management
from apps.routes.Show import show
from apps.routes.Guest import guest
from apps.routes.RSVP import greeting
## Import Blueprint ---------------------------------------- Finish

## Register Blueprint ---------------------------------------- Start
app.register_blueprint(auth)
app.register_blueprint(dashboard)
app.register_blueprint(management)
app.register_blueprint(show)
app.register_blueprint(guest)
app.register_blueprint(greeting)
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
@app.route('/signout')
def signout():
    if (session.get('user') is not None):
        session.pop('user')
        session.clear()
        if request.args.get("message") is not None:
            flash(
                message=request.args.get("message"),
                category='danger'
            )
        return redirect(url_for('auth.sign_in'))
## Route LogOut ---------------------------------------- Finish

## Route Unauthorization ---------------------------------------- Start
@app.errorhandler(403)
def unauthorization(e):
    return render_template("pages/ErrorPage/403.html")
## Route Unauthorization ---------------------------------------- Finish

## Route Not Found ---------------------------------------- Start
@app.errorhandler(404)
def page_not_found(e):
    return render_template("pages/ErrorPage/404.html")
## Route Not Found ---------------------------------------- Finish

# ## Route Authorization Timeout ---------------------------------------- Start
# @app.errorhandler(419)
# def authorization_timeout(e):
#     return render_template("pages/ErrorPage/419.html")
# ## Route Authorization Timeout ---------------------------------------- Finish

# ROUTING ============================================================ End
