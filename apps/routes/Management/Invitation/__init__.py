from flask import Blueprint, render_template, request, redirect, url_for, session, make_response, flash, current_app as app

from .... import TITLE_DASHBD
from ...utilities import *

import requests, json, base64


mnginvitation = Blueprint(
    name='invitation',
    import_name=__name__,
    url_prefix='/invitation',
    template_folder="../../../templates/pages/ManagementPage/Invitation"
)


@mnginvitation.before_request
def cek_session():
    if session.get('user') is None:
        return redirect(url_for('auth.sign_in'))
    
    decode_token, error_message = decode_jwt(session['user']['access_token'])
    if decode_token:
        for data in decode_token:
            session['user'][data] = decode_token[data]
    else:
        return redirect(url_for('signout', message=error_message))


@mnginvitation.get('/')
def index():
    data = dict()
    data['list_invitation'] = get_invitation()
    # data['category'] = get_category()

    return render_template(
        title="Creavitation",
        data = data,
        template_name_or_list='invitation.html'
    )


@mnginvitation.get('/select/template')
def select_template():
    data = dict()
    data['list_category'] = get_category()
    data['list_template'] = get_template()
    data['selected'] = 1

    return render_template(
        title="Creavitation",
        data = data,
        template_name_or_list='template.html'
    )


@mnginvitation.get('/add')
def add():
    data = dict()
    data['template'] = get_detail_template()

    return render_template(
        title="Creavitation",
        data = data,
        template_name_or_list='addInvitation.html'
    )


@mnginvitation.post('/add')
def add_proccess():
    dataInput = request.form.to_dict()
    temId = dataInput['template_id']
    category = dataInput['category']

    if category.upper() == "PERNIKAHAN":
        womans_photo = request.files.get('womans_photo')
        mans_photo = request.files.get('mans_photo')
        # galeri_photo = request.files.get('galeri-1')
        if womans_photo:
            photoFile = womans_photo.read()
            photoMime = womans_photo.mimetype
            photoFile = base64.b64encode(photoFile).decode('utf-8')
            wpf_base64 = f"data:{photoMime};base64,{photoFile}" # wpf = womans photo file
        else:
            wpf_base64 = ""

        if mans_photo:
            photoFile = mans_photo.read()
            photoMime = mans_photo.mimetype
            photoFile = base64.b64encode(photoFile).decode('utf-8')
            mpf_base64 = f"data:{photoMime};base64,{photoFile}" # mpf = mans photo file
        else:
            mpf_base64 = ""

        # if galeri_photo:
        #     photoFile = galeri_photo.read()
        #     photoMime = galeri_photo.mimetype
        #     photoFile = base64.b64encode(photoFile).decode('utf-8')
        #     gpf_base64 = f"data:{photoMime};base64,{photoFile}" # mpf = mans photo file
        # else:
        #     gpf_base64 = ""

        print(dataInput)
        dataInput = {
            "category_id" : dataInput['category_id'],
            "template_id" : dataInput['template_id'],
            "title" : dataInput['title'],
            "personal_data" : {
                # man info
                "man_fullname": dataInput['man_fullname'],
                "man_name": dataInput['man_name'],
                "mans_photo": mpf_base64,
                "man_address": dataInput['man_address'],
                "son_no": dataInput['son_no'],
                "man_dad_status": dataInput['man_dad_status'],
                "man_mom_status": dataInput['man_mom_status'],
                "mans_dad": dataInput['mans_dad'],
                "mans_mom": dataInput['mans_mom'],

                # woman info
                "woman_fullname": dataInput['woman_fullname'],
                "woman_name": dataInput['woman_name'],
                "womans_photo": wpf_base64,
                "woman_address": dataInput['woman_address'],
                "daughter_no": dataInput['daughter_no'],
                "woman_dad_status": dataInput['woman_dad_status'],
                "woman_mom_status": dataInput['woman_mom_status'],
                "womans_dad": dataInput['womans_dad'],
                "womans_mom": dataInput['womans_mom'],
            #     "galeri_photo": gpf_base64,
            },
            "detail_info" : {
                "marriage_date": dataInput['marriage_date'],
                "marriage_start": dataInput['marriage_start'],
                "marriage_end": dataInput['marriage_end'],
                "reception_date": dataInput['reception_date'],
                "reception_start": dataInput['reception_start'],
                "reception_end": dataInput['reception_end'],
                "location": dataInput['location'],
                "maps": dataInput['maps'],
            },
            "inv_setting" : {}
        }
    elif category.upper() == "ULANG TAHUN":
        myphoto = request.files.get('myphoto')
        if myphoto:
            photoFile = myphoto.read()
            photoMime = myphoto.mimetype
            photoFile = base64.b64encode(photoFile).decode('utf-8')
            photo_base64 = f"data:{photoMime};base64,{photoFile}" # wpf = womans photo file
        else:
            photo_base64 = ""

        dataInput = {
            "category_id" : dataInput['category_id'],
            "template_id" : dataInput['template_id'],
            "title" : dataInput['title'],
            "personal_data" : {
                # My info
                "fullname": dataInput['fullname'],
                "callname": dataInput['callname'],
                "myphoto": photo_base64,
                "birthday": dataInput['birthday']
            },
            "detail_info" : {
                "date": dataInput['bd_date'],
                "start": dataInput['bd_start'],
                "end": dataInput['bd_end'],
                "dresscode": dataInput['dresscode'],
                "location": dataInput['location'],
                "maps": dataInput['maps'],
            },
            "inv_setting" : {}
        }
    

    # Payload 
    payload = json.dumps(dataInput)

    # Set URL
    url = app.config['BE_URL'] + '/invitation/'

    # Set Header
    headers = {
        'Authorization' : f'Bearer {session["user"]["access_token"]}',
        'Content-Type' : 'application/json'
    }
    response = requests.request (
        method='POST',
        url=url,
        headers=headers,
        data=payload
    )
    data = response.json().get('data')
    
    if (response.status_code != 200):
        flash(
            message=response.json().get('message'),
            category='danger'
        )
        return redirect(url_for('management.invitation.add', temId=temId))
    else:
        flash(
            message=response.json().get('message'),
            category='success'
        )
        id = data["inv_id"]
        code = data["inv_code"]
        return redirect(url_for('management.invitation.detail', id=id, code=code))
        # return redirect(url_for('management.invitation.add', temId=temId))


@mnginvitation.get('/edit')
def edit():
    data = dict()
    data['invitation'] = get_detail_invitation()

    return render_template(
        title="Creavitation",
        data = data,
        template_name_or_list='editInvitation.html'
    )


@mnginvitation.post('/edit')
def edit_proccess():
    dataInput = request.form.to_dict()
    id = dataInput['invitation_id']
    code = dataInput['invitation_code']
    category = dataInput['category']

    if category.upper() == "PERNIKAHAN":
        womans_photo = request.files.get('womans_photo')
        mans_photo = request.files.get('mans_photo')
        if womans_photo:
            photoFile = womans_photo.read()
            photoMime = womans_photo.mimetype
            photoFile = base64.b64encode(photoFile).decode('utf-8')
            wpf_base64 = f"data:{photoMime};base64,{photoFile}" # wpf = womans photo file
        else:
            wpf_base64 = dataInput['womans_photo_old']

        if mans_photo:
            photoFile = mans_photo.read()
            photoMime = mans_photo.mimetype
            photoFile = base64.b64encode(photoFile).decode('utf-8')
            mpf_base64 = f"data:{photoMime};base64,{photoFile}" # mpf = mans photo file
        else:
            mpf_base64 = dataInput['mans_photo_old']
        dataInput = {
            "invitation_id" : dataInput['invitation_id'],
            "category_id" : dataInput['category_id'],
            "template_id" : dataInput['template_id'],
            "title" : dataInput['title'],
            "personal_data" : {
                # man info
                "man_fullname": dataInput['man_fullname'],
                "man_name": dataInput['man_name'],
                "mans_photo": mpf_base64,
                "man_address": dataInput['man_address'],
                "son_no": dataInput['son_no'],
                "man_dad_status": dataInput['man_dad_status'],
                "man_mom_status": dataInput['man_mom_status'],
                "mans_dad": dataInput['mans_dad'],
                "mans_mom": dataInput['mans_mom'],

                # woman info
                "woman_fullname": dataInput['woman_fullname'],
                "woman_name": dataInput['woman_name'],
                "womans_photo": wpf_base64,
                "woman_address": dataInput['woman_address'],
                "daughter_no": dataInput['daughter_no'],
                "woman_dad_status": dataInput['woman_dad_status'],
                "woman_mom_status": dataInput['woman_mom_status'],
                "womans_dad": dataInput['womans_dad'],
                "womans_mom": dataInput['womans_mom'],
            #     "galeri_photo": gpf_base64,
            },
            "detail_info" : {
                "marriage_date": dataInput['marriage_date'],
                "marriage_start": dataInput['marriage_start'],
                "marriage_end": dataInput['marriage_end'],
                "reception_date": dataInput['reception_date'],
                "reception_start": dataInput['reception_start'],
                "reception_end": dataInput['reception_end'],
                "location": dataInput['location'],
                "maps": dataInput['maps'],
            },
            "inv_setting" : {}
        }
    
    elif category.upper() == "ULANG TAHUN":
        myphoto = request.files.get('myphoto')
        if myphoto:
            photoFile = myphoto.read()
            photoMime = myphoto.mimetype
            photoFile = base64.b64encode(photoFile).decode('utf-8')
            photo_base64 = f"data:{photoMime};base64,{photoFile}" # wpf = womans photo file
        else:
            photo_base64 = dataInput['myphoto_old']

        print(dataInput)
        dataInput = {
            "invitation_id" : dataInput['invitation_id'],
            "category_id" : dataInput['category_id'],
            "template_id" : dataInput['template_id'],
            "title" : dataInput['title'],
            "personal_data" : {
                # man info
                "fullname": dataInput['fullname'],
                "callname": dataInput['callname'],
                "myphoto": photo_base64,
                "birthday": dataInput['birthday']
            },
            "detail_info" : {
                "date": dataInput['bd_date'],
                "start": dataInput['bd_start'],
                "end": dataInput['bd_end'],
                "dresscode": dataInput['dresscode'],
                "location": dataInput['location'],
                "maps": dataInput['maps'],
            },
            "inv_setting" : {}
        }
    
    # Payload 
    payload = json.dumps(dataInput)

    # Set URL
    url = app.config['BE_URL'] + '/invitation/'

    # Set Header
    headers = {
        'Authorization' : f'Bearer {session["user"]["access_token"]}',
        'Content-Type' : 'application/json'
    }
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
        return redirect(url_for('management.invitation.edit', id=id))
    else:
        flash(
            message=response.json().get('message'),
            category='success'
        )
        return redirect(url_for('management.invitation.detail', id=id, code=code))
    # return redirect(url_for('management.invitation.edit', id=id))


# clear
@mnginvitation.get('/delete')
def delete():
    data = dict()
    data['invitation'] = get_detail_invitation()

    return render_template(
        title="Creavitation",
        data = data,
        template_name_or_list='deleteInvitation.html'
    )


# clear
@mnginvitation.get('/delete/id')
def delete_proccess(): 
    id = request.args.get('id')
    dataInput = {
        "invitation_id" : id
    }          

    url = app.config['BE_URL'] + '/invitation/'
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

    # response.status_code = 300
    
    if (response.status_code != 200):
        flash(
            message=response.json().get('message'),
            category='danger'
        )
        return redirect(url_for('management.invitation.delete', id=id))
    else:
        flash(
            message=response.json().get('message'),
            category='success'
        )
        return redirect(url_for('management.invitation.index'))


@mnginvitation.get('/detail')
def detail():
    data = dict()
    data['invitation'] = get_detail_invitation() # id
    data['guest'] = get_detail_guest() # code
    data['greeting'] = get_detail_greeting() # code
    print(data)
    data['message'] = set_message("","")
    if data['invitation'] != None:
        data['message'] = set_message(data['invitation']['invitation_code'], data['invitation']['invitation_title'])

    return render_template(
        title="Creavitation",
        data = data,
        template_name_or_list='detailInvitation.html'
    )

