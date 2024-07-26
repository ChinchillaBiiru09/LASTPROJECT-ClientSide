from flask import Blueprint, render_template, session, request, redirect, flash, url_for, current_app as app
from .... import TITLE_DASHBD
from ...utilities import get_profile, get_invitation, get_guest, get_greeting
import requests, json


mnguser = Blueprint(
    name='user',
    import_name=__name__,
    url_prefix='/user',
    template_folder="../../../templates/pages/ManagementPage/User"
)


@mnguser.get('/')
def index():
    url = app.config['BE_URL'] + '/user/'
    headers = {
        'Authorization' : f'Bearer {session["user"]["access_token"]}',
        'Content-Type' : 'application/json'
    }

    response = requests.request(
        method='GET',
        url=url,
        headers=headers
    )
    
    data = response.json().get('data')
    return render_template(
        data=data,
        title=TITLE_DASHBD,
        template_name_or_list='user.html'
        
    )


@mnguser.get('/detail')
def detail():
    data = dict()
    is_param = True
    data['user'] = get_profile(is_param)
    data['invitation'] = get_invitation(is_param)
    data['guest'] = get_guest(is_param)
    data['greeting'] = get_greeting(is_param)

    return render_template(
        title=TITLE_DASHBD,
        data=data,
        template_name_or_list='detailUser.html'
    )


@mnguser.get('/delete')
def delete():
    data = get_profile(True)

    return render_template(
        title=TITLE_DASHBD,
        data=data,
        template_name_or_list='deleteUser.html'
    )


@mnguser.get('/delete/data')
def delete_proccess():
    id = request.args.get('id')
    dataInput = {
        "user_id" : id
    }
    
    print(dataInput)
    url = app.config['BE_URL'] + '/user/'

    headers = {
        'Authorization' : f'Bearer {session["user"]["access_token"]}',
        'Content-Type' : 'application/json'
    }

    response = requests.request (
        method='DELETE',
        url=url,
        headers=headers,
        params=dataInput
    )
    print(response)

    if (response.status_code != 200):
        flash(
            message=response.json().get('message'),
            category='danger'
        )
        return redirect(url_for('management.user.delete', id=id))
    else:
        flash(
            message=response.json().get('message'),
            category='success'
        )
        return redirect(url_for('management.user.index'))

