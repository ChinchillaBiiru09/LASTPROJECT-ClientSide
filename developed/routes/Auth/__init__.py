from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask import current_app as app

import json, requests

auth = Blueprint(
    name='auth',
    import_name=__name__,
    url_prefix='/auth',
    template_folder="../../templates/pages/AuthPage"
)


# @auth.before_request
# def session_check():
#     if (session.get('user') != None):
#         if(session['user']['role']=='ADMIN'):
#             return redirect(url_for('dashboard.admin'))
#         else:
#             return redirect(url_for('dashboard.index'))
#     else:
#         return True
        

@auth.get('/')
@auth.get('/signin')
def sign_in():
    return render_template(
        title="Sign In - Aplikasi Undangan Online",
        template_name_or_list='sign_in.html'
    )

@auth.get('/signup')
def sign_up():
    return render_template(
        title="Sign Up - Aplikasi Undangan Online",
        template_name_or_list='sign_up.html'
    )

@auth.post('/signin')
def signin_process(is_admin=False):
    return redirect(url_for('dashboard.index'))