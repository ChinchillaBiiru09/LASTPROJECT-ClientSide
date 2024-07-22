from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app as app

from ..utilities import *

import json, requests


guest = Blueprint(
    name='guest',
    import_name=__name__,
    url_prefix='/guest',
    template_folder="../../templates/pages/GuestPage"
)


@guest.before_request
def cek_session():
    if session.get('user') is None:
        return redirect(url_for('auth.sign_in'))
    
    decode_token, error_message = decode_jwt(session['user']['access_token'])
    if decode_token:
        for data in decode_token:
            session['user'][data] = decode_token[data]
    else:
        return redirect(url_for('signout', message=error_message))


# clear
@guest.get('/')
def index():
    data = dict()
    data['guest'] = get_guest()
    
    return render_template(
        title="Creavitation",
        data=data,
        template_name_or_list='guest.html'
    )


# clear
@guest.get('/detail')
def guest_detail():
    data = dict()
    data['guest'] = get_detail_guest()

    return render_template(
        title="Creavitation",
        data=data,
        template_name_or_list='detailguest.html'
    )


# clear
@guest.get('/add')
def add():
    data = dict()
    data['invitation'] = get_detail_invitation()
    
    return render_template(
        title="Creavitation",
        data=data,
        template_name_or_list='addGuest.html'
    )


# clear
@guest.post('/add')
def add_proccess():

    dataInput = request.form.to_dict()
    id = dataInput['invitation_id']
    code = dataInput['inv_code']
    dataInput = {
        "invitation_code" : dataInput['inv_code'],
        "name" : dataInput['name'],
        "address" : dataInput['address'],
        "phone" : dataInput['phone']
    }

    # Set URL
    url = app.config['BE_URL'] + '/guest/'

    # Set Header
    headers = {
        'Authorization' : f'Bearer {session["user"]["access_token"]}',
        'Content-Type' : 'application/json'
    }

    # Payload
    payload = json.dumps(dataInput)

    response = requests.request (
        method='POST',
        url=url,
        headers=headers,
        data=payload
    )

    if (response.status_code != 200):
        flash(
            message=response.json().get('message'),
            category='danger'
        )
        return redirect(url_for('guest.add', id=id))
    else:
        flash(
            message=response.json().get('message'),
            category='success'
        )
        return redirect(url_for('management.invitation.detail', id=id, code=code))


# clear
@guest.get('/edit')
def edit():
    data = dict()
    data['invitation'] = get_detail_invitation()
    data['guest'] = get_guest_by_id()
    
    return render_template(
        title="Creavitation",
        data=data,
        template_name_or_list='editGuest.html'
    )


# clear
@guest.post('/edit')
def edit_proccess():
    dataInput = request.form.to_dict()
    gueId = dataInput['guest_id']
    id = dataInput['invitation_id']
    code = dataInput['inv_code']
    dataInput = {
        "guest_id" : dataInput['guest_id'],
        "invitation_code" : dataInput['inv_code'],
        "name" : dataInput['name'],
        "address" : dataInput['address'],
        "phone" : dataInput['phone']
    }

    # Set URL
    url = app.config['BE_URL'] + '/guest/'

    # Set Header
    headers = {
        'Authorization' : f'Bearer {session["user"]["access_token"]}',
        'Content-Type' : 'application/json'
    }

    # Payload
    payload = json.dumps(dataInput)

    response = requests.request (
        method='PUT',
        url=url,
        headers=headers,
        data=payload
    )

    if (response.status_code != 200):
        flash(
            message=response.json().get('message'),
            category='danger'
        )
        return redirect(url_for('guest.edit', gueId=gueId, id=id))
    else:
        flash(
            message=response.json().get('message'),
            category='success'
        )
        return redirect(url_for('management.invitation.detail', id=id, code=code))


# Clear
@guest.get('/delete')
def delete():
    data = dict()
    data['guest'] = get_guest_by_id()
    data['invitation'] = get_detail_invitation()
    
    return render_template(
        title="Creavitation",
        data=data,
        template_name_or_list='deleteGuest.html'
    )


# Clear
@guest.get('/delete/data')
def delete_proccess():
    gueId = request.args.get('gueId')
    id = request.args.get('id')
    code = request.args.get('code')
    dataInput = {
        "guest_id" : gueId
    }

    url = app.config['BE_URL'] + '/guest/'
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

    if (response.status_code != 200):
        flash(
            message=response.json().get('message'),
            category='danger'
        )
        return redirect(url_for('guest.delete', gueId=gueId, id=id))
    else:
        flash(
            message=response.json().get('message'),
            category='success'
        )
        return redirect(url_for('management.invitation.detail', id=id, code=code))
