from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app as app

from ..utilities import *

import json, requests, base64


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
        template_name_or_list='detailGuest.html'
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
@guest.get('/copy')
def copy():
    data = dict()
    data['invitation'] = get_detail_invitation() # user_id
    data['list_invitation'] = get_invitation() # user_id
    
    return render_template(
        title="Creavitation",
        data=data,
        template_name_or_list='copyListGuest.html'
    )

# clear
@guest.post('/copy')
def copy_process():
    dataInput = request.form.to_dict()
    id = dataInput['invitation_id']
    code = dataInput['inv_code']
    dataInput = {
        "invitation_code" : dataInput['inv_code'],
        "reference_code": dataInput['ref_code']
    }

    # Set URL
    url = app.config['BE_URL'] + '/guest/duplicate'

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
        return redirect(url_for('guest.copy', id=id))
    else:
        flash(
            message=response.json().get('message'),
            category='success'
        )
        return redirect(url_for('management.invitation.detail', id=id, code=code))


# clear
@guest.get('/import')
def importExcel():
    data = dict()
    data['invitation'] = get_detail_invitation()
    data['list_invitation'] = get_invitation()
    
    return render_template(
        title="Creavitation",
        data=data,
        template_name_or_list='importExcelGuest.html'
    )


# clear
@guest.post('/import')
def importExcel_process():
    try:
        dataInput = request.form.to_dict()
        id = dataInput['invitation_id']
        code = dataInput['inv_code']
        excel = request.files.get('excel')
        
        if excel:
            excelFile = excel.read()
            excelMime = excel.mimetype
            excelFile = base64.b64encode(excelFile).decode('utf-8')
            excel_base64 = f"data:{excelMime};base64,{excelFile}"
        else:
            excel_base64 = ""

        dataInput = {
            "invitation_code" : dataInput['inv_code'],
            "file" : excelFile
        }

        # Set URL
        url = app.config['BE_URL'] + '/guest/import'

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
            return redirect(url_for('guest.importExcel', id=id))
        else:
            flash(
                message=response.json().get('message'),
                category='success'
            )
            return redirect(url_for('management.invitation.detail', id=id, code=code))
    except Exception as e:
        return make_response(jsonify({"statusCode":400, "message":str(e)}), 400)


# clear
@guest.get('/export')
def exportExcel():
    data = dict()
    data['invitation'] = get_detail_invitation()
    # data['list_invitation'] = get_invitation()
    data['export'] = export_guest()
    print("data => ", data)
    
    return render_template(
        title="Creavitation",
        data=data,
        template_name_or_list='exportExcelGuest.html'
    )


# clear
@guest.get('/export')
def exportExcel_process():
    try:
        id = request.args.get('id')
        code = request.args.get('code')
        dataInput = {
            "invitation_code": code
        }

        # Set URL
        url = app.config['BE_URL'] + '/guest/export'

        # Set Header
        headers = {
            'Authorization' : f'Bearer {session["user"]["access_token"]}',
            'Content-Type' : 'application/json'
        }

        # Payload
        payload = json.dumps(dataInput)
        response = requests.request (
            method='GET',
            url=url,
            headers=headers,
            params=code
        )
        print(response)
        
        data = response.json().get('data')
        print("data exp = ", data)

        if (response.status_code != 200):
            flash(
                message=response.json().get('message'),
                category='danger'
            )
            return redirect(url_for('management.invitation.detail', id=id, code=code))
        else:
            flash(
                message=response.json().get('message'),
                category='success'
            )
            return redirect(url_for('guest.exportExcel', data=data, id=id, code=code))
    except Exception as e:
        return make_response(jsonify({"statusCode":400, "message":str(e)}), 400)


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
    data['guest'] = get_guest_by_id() # gueId
    data['invitation'] = get_detail_invitation() # id
    
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
