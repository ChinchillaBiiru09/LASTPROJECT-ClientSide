from flask import Blueprint, render_template, request, redirect, url_for, session, current_app as app

auth = Blueprint(
    name='auth',
    import_name=__name__,
    url_prefix='/auth',
    template_folder="../../templates/pages/AuthPage"
)


@auth.before_request
def session_check():
    if (session.get('user') != None):
        return redirect(url_for('Dashboard.index'))

@auth.get('/')
@auth.get('/login')
def login():
    return render_template(
        title="Login Aplikasi Undangan Online",
        template_name_or_list='login.html'
    )