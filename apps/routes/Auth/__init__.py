from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask import current_app as app

import json, requests

auth = Blueprint(
    name='auth',
    import_name=__name__,
    url_prefix='/auth',
    template_folder="../../templates/pages/AuthPage"
)


@auth.before_request
def session_check():
    if (session.get('user') != None):
        if(session['user']['role']=='ADMIN'):
            return redirect(url_for('dashboard.admin'))
        else:
            return redirect(url_for('dashboard.index'))
        

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
    # mengambil data masukkan
    dataInput = request.form.to_dict()
    print(dataInput)

    # request permintaan register akun baru ke api
    if(is_admin):
        url = app.config['BE_URL'] + '/admin/signin'
    else:
        url = app.config['BE_URL'] + '/user/signin'

    print(url)
    payload = json.dumps(dataInput)
    print(payload)
    headers = {'Content-Type' : 'application/json'}
    response = requests.request (
        method='POST', 
        url=url,
        headers=headers,
        data=payload
    )
    print(response)
    # jika respon api tidak berhasil
    if(response.status_code == 499):
        flash (
            message=response.json().get('description'),
            category='danger'
        )
        return redirect(url_for('auth.sign_in'))

    if(response.status_code != 200):
        if(is_admin==False):
            return signin_process(is_admin=True)
        flash (
            message='Username atau Password salah',
            category='danger'
        )
        return redirect(url_for('auth.sign_in'))
    
    # jika berhasil, arahkan ke halaman dashboard
    else:
        session['user'] = response.json().get('data')
        return redirect(url_for('auth.sign_in'))
    # return redirect(url_for('dashboard.index'))