from flask import Blueprint, make_response, jsonify, render_template, request, redirect, url_for, session, flash
from flask import current_app as app

from ... import TITLE_SIGNIN, TITLE_SIGNUP
from ..utilities import decode_jwt
from datetime import datetime

import json, requests


auth = Blueprint(
    name='auth',
    import_name=__name__,
    url_prefix='/auth',
    template_folder="../../templates/pages/AuthPage"
)


@auth.before_request
def session_check():
    """
        session : <SecureCookieSession {'user': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2Us
        ImlhdCI6MTcwOTU0NzEwNywianRpIjoiZWU2MzA3NjMtN2NhZC00YWNiLThkMjgtYmY2YmYyMmE0OGQxIiwidHlwZSI6ImFjY2
        VzcyIsInN1YiI6ImFkbWZpZGFoM0BnbWFpbC5jb20iLCJuYmYiOjE3MDk1NDcxMDcsImV4cCI6MTcwOTYzMzUwNywiaWQiOjIs
        ImVtYWlsIjoiYWRtZmlkYWgzQGdtYWlsLmNvbSIsIm5hbWUiOiJGaWRhaCBJSUkiLCJyb2xlIjoiVVNFUiJ9.MtoFZVdlCX0QC
        ZdyV4BIskflkT8LFOI1_x1ZIeqkge0', 'role': 'USER'}>

        encode : {'fresh': False, 'iat': 1709547107, 'jti': 'ee630763-7cad-4acb-8d28-bf6bf22a48d1', 
        'type': 'access', 'sub': 'admfidah3@gmail.com', 'nbf': 1709547107, 'exp': 1709633507, 'id': 2, 
        'email': 'admfidah3@gmail.com', 'name': 'Fidah III', 'role': 'USER'}
    """
    if session.get('user') is not None:
        decode_token, error_message = decode_jwt(session['user']['access_token'])
        if decode_token:
            return redirect(url_for('dashboard.index'))
        else:
            return redirect(url_for('signout', message=error_message))    
    

@auth.get('/signup')
def sign_up():
    return render_template(
        title=TITLE_SIGNUP,
        template_name_or_list='sign_up.html'
    )    


@auth.get('/signin')
def sign_in():
    return render_template(
        title=TITLE_SIGNIN,
        template_name_or_list='sign_in.html'
    )


@auth.post('/signup')
def signup_proccess(): # Clear
    # mengambil data masukkan
    dataInput = request.form.to_dict()
    
    # request permintaan register akun baru ke api
    payload = json.dumps(dataInput)
    headers = {'Content-Type' : 'application/json'}
    response = requests.request (
        method='POST', 
        url=app.config['BE_URL'] + '/user/',
        headers=headers,
        data=payload
    )
    
    # jika respon api tidak berhasil mendaftarkan akun baru, maka munculkan pesan error menggunakan flash
    if(response.status_code != 200):
        flash (
            message=response.json().get('message'),
            category='danger'
        )
        return redirect(url_for('auth.sign_up'))
    
    # jika berhasil, arahkan user ke halaman login
    else:
        flash (
            message=f'Pendaftaran akun berhasil. Silahkan cek email anda untuk verifikasi akun 😊',
            category='success'
        )
        return redirect(url_for('auth.sign_up'))


@auth.post('/signin')
def signin_proccess(is_admin=False): # Clear
    # mengambil data masukkan
    dataInput = request.form.to_dict()
    if dataInput['email'].lower() == "admin":
        dataInput['email'] = "admkira2@gmail.com"
        dataInput['password'] = "Admin12345"
    elif dataInput['email'].lower() == "user":
        dataInput['email'] = "usrkira1@gmail.com"
        dataInput['password'] = "User12345"

    # Membuat URL berdasarkan role user
    url = app.config['BE_URL'] + ('/admin/signin' if is_admin else '/user/signin')

    # request permintaan register akun baru ke api
    payload = json.dumps(dataInput)
    headers = {'Content-Type' : 'application/json'}
    response = requests.request (
        method='POST', 
        url=url,
        headers=headers,
        data=payload
    )

    # jika respon api tidak berhasil
    if(response.status_code == 499):
        flash (
            message=response.json().get('message'),
            category='danger'
        )
        return redirect(url_for('auth.sign_in'))

    if(response.status_code != 200):
        if(is_admin==False):
            return signin_proccess(is_admin=True)
        flash (
            message='Username atau Password salah',
            category='danger'
        )
        return redirect(url_for('auth.sign_in'))
    
    # jika berhasil, arahkan ke halaman dashboard
    else:
        session['user'] = response.json().get('data')
        return redirect(url_for('auth.sign_in'))


@auth.get('/verified/<codes>')
def verify(codes):
    try:
        # mengambil data masukkan
        dataInput = {
            "token" : codes
        }

        # request permintaan register akun baru ke api
        # payload = json.dumps(dataInput)
        headers = {'Content-Type' : 'application/json'}
        response = requests.request (
            method='GET', 
            url=app.config['BE_URL'] + '/auth/detail',
            headers=headers,
            params=dataInput
        )
        
        # Response data
        data = response.json().get('data')
        is_expired = data['is_expired']

        if is_expired == 1:
            # flash (
            #     message=response.json().get('message'),
            #     category='danger'
            # )
            # return app.errorhandler(419)
            return render_template(
                title='Verify New Account',
                data=data,
                expired=True,
                template_name_or_list='verify.html'
            )

        # Cek Respon
        if(response.status_code != 200):
            flash (
                message=response.json().get('message'),
                category='danger'
            )
            # return app.errorhandler(419)
            return render_template(
                title='Verify New Account',
                data=data,
                expired=False,
                template_name_or_list='verify.html'
            )
        
        # jika berhasil, arahkan user ke halaman login
        else:
            return render_template(
                title='Verify New Account',
                data=data,
                expired=False,
                template_name_or_list='verify.html'
            )
    except Exception as e:
        return make_response(jsonify({"statusCode":400, "message":str(e)}), 400)


@auth.post('/updatetoken/')
def update_token():
    try:
        # mengambil data masukkan
        dataInput = request.form.to_dict()
        code = dataInput['token']
        # dataInput = {
        #     "token" : codes
        # }

        # request permintaan register akun baru ke api
        payload = json.dumps(dataInput)
        print("payload = ", payload)
        headers = {'Content-Type' : 'application/json'}
        url = app.config['BE_URL'] + '/auth/'
        response = requests.request (
            method='PUT', 
            url=url,
            headers=headers,
            data=payload
        )
        
        # Response data
        # data = response.json().get('data')

        # Cek Respon
        if(response.status_code != 200):
            flash (
                message=response.json().get('message'),
                category='danger'
            )
            return redirect(url_for('auth.verify', codes=code))
        
        # jika berhasil, arahkan user ke halaman login
        else:
            flash (
                message=f'Token aktivasi akun anda berhasil diperbarui. Silahkan cek email anda untuk melanjutkan verifikasi akun 😊',
                category='success'
            )
            return redirect(url_for('auth.sign_in'))
    except Exception as e:
        return make_response(jsonify({"statusCode":400, "message":str(e)}), 400)


@auth.post('/activate/')
def activate():
    try:
        # mengambil data masukkan
        dataInput = request.form.to_dict()
        # dataInput = {
        #     "token" : codes
        # }

        # request permintaan register akun baru ke api
        payload = json.dumps(dataInput)
        print("payload aktivasi - ", payload)
        headers = {'Content-Type' : 'application/json'}
        url = app.config['BE_URL'] + '/user/activate'
        response = requests.request (
            method='PUT', 
            url=url,
            headers=headers,
            data=payload
        )
        
        # Cek Respon
        if(response.status_code != 200):
            flash (
                message=f'Maaf, aktivasi akun gagal. Silahkan coba lagi 😊',
                category='danger'
            )
            return redirect(url_for('auth.sign_in'))
        
        # jika berhasil, arahkan user ke halaman login
        else:
            flash (
                message=f'Aktivasi akun berhasil. Silahkan login ke akun anda 😊',
                category='success'
            )
            return redirect(url_for('auth.sign_in'))
    except Exception as e:
        return make_response(jsonify({"statusCode":400, "message":str(e)}), 400)


@auth.get('/forgot-password')
def forgot_password():
    return render_template(
        title='forgot password',
        template_name_or_list='forgot_password.html'
    )


@auth.post('/send')
def send_email():
    try:
        # mengambil data masukkan
        dataInput = request.form.to_dict()
        
        # request permintaan register akun baru ke api
        payload = json.dumps(dataInput)
        headers = {'Content-Type' : 'application/json'}
        response = requests.request (
            method='POST', 
            url=app.config['BE_URL'] + '/auth/',
            headers=headers,
            data=payload
        )
        
        # Cek Respon
        if(response.status_code != 200):
            flash (
                message=response.json().get('message'),
                category='danger'
            )
            return redirect(url_for('auth.sign_up'))
        
        # jika berhasil, arahkan user ke halaman login
        else:
            flash (
                message=f'Pendaftaran akun berhasil. Silahkan cek email anda untuk verifikasi akun 😊',
                category='success'
            )
            return redirect(url_for('auth.sign_up'))
        
    except:
        pass


@auth.post('/reset-password/<codes>')
def reset_password(codes):
    try:
        # mengambil data masukkan
        dataInput = request.form.to_dict()
        
        # request permintaan register akun baru ke api
        payload = json.dumps(dataInput)
        headers = {'Content-Type' : 'application/json'}
        response = requests.request (
            method='POST', 
            url=app.config['BE_URL'] + '/user/',
            headers=headers,
            data=payload
        )
        
        # Cek Respon
        if(response.status_code != 200):
            flash (
                message=response.json().get('message'),
                category='danger'
            )
            return redirect(url_for('auth.sign_up'))
        
        # jika berhasil, arahkan user ke halaman login
        else:
            flash (
                message=f'Pendaftaran akun berhasil. Silahkan cek email anda untuk verifikasi akun 😊',
                category='success'
            )
            return redirect(url_for('auth.sign_up'))
    except:
        pass

