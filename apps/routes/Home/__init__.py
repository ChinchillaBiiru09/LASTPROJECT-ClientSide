from flask import Blueprint, render_template, redirect, url_for, current_app as app
from ... import TITLE_HOME
import json, requests

# Block Blueprint ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
home = Blueprint(
    name='home',
    import_name=__name__,
    url_prefix='/home',
    template_folder='../../templates/pages/HomePage'
)
# End Block Blueprint ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ROUTE SERVICE ============================================================ Begin
# POST https://127.0.0.1:5000/home/service
@home.get('/service')
def service():
    return render_template(
        title=TITLE_HOME,
        template_name_or_list="service.html"
    )
# BLOCK FIRST/BASE ============================================================ End


# ROUTE ABOUT ============================================================ Begin
# POST https://127.0.0.1:5000/home/about
@home.get('/about')
def about():
    return render_template(
        title=TITLE_HOME,
        template_name_or_list="about.html"
    )
# BLOCK FIRST/BASE ============================================================ End