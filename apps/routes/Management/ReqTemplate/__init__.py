import base64
from flask import Blueprint, render_template, flash, request, redirect, url_for, session, current_app as app

from .... import TITLE_DASHBD
from ...utilities import *

import json, requests, base64, mimetypes

mngreqtemp = Blueprint(
    name='reqtemp',
    import_name=__name__,
    url_prefix='/request',
    template_folder="../../../templates/pages/ManagementPage/ReqTemplate"
)


@mngreqtemp.get('/')
def index():
    data = dict()
    data['list_category'] = get_category()
    data['template_request'] = get_request_template()
    print("data req - ", data['template_request'])
    data['selected'] = 0


    return render_template(
        title=TITLE_DASHBD,
        data=data,
        template_name_or_list='request.html'
    )
# @mngtemplate.get('/add')
# def add():
# @mngtemplate.post('/add')
# def add_proccess():
# @mngtemplate.get('/edit')
# def edit():
# @mngtemplate.post('/edit')
# def edit_proccess():
# # Clear
# @mngtemplate.get('/delete')
# def delete():
# # Clear
# @mngtemplate.get('/delete/id')
# def delete_proccess():
# @mngtemplate.get('/detail')
# def detail():


@mngreqtemp.get('/request')
def request_create():
    data = dict()
    data['list_category'] = get_category()

    return render_template(
        title=TITLE_DASHBD,
        data=data,
        template_name_or_list='addRequest.html'
    )


@mngreqtemp.post('/request')
def request_create_proccess():
    dataInput = request.form.to_dict()
    file = request.files.get('fileDesign')
    if file:
        filedesign = file.read()
        fileMimeType = file.mimetype
        filedesign = base64.b64encode(filedesign).decode('utf-8')
        base64_string = f"data:{fileMimeType};base64,{filedesign}"
    else:
        base64_string = ""
    
    dataInput = {
        "category_id" : dataInput["category"], 
        "template_design" : base64_string, 
        "description" : dataInput["description"], 
        "deadline" : dataInput["deadline"], 
        "type" : dataInput["selTypeTemp"]
        }
    
    url = app.config['BE_URL'] + '/template/request/'

    payload = json.dumps(dataInput)
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

    if (response.status_code != 200):
        flash(
            message=response.json().get('message'),
            category='danger'
        )
        return redirect(url_for('management.reqtemp.request_create'))
    else:
        flash(
            message=response.json().get('message'),
            category='success'
        )
        return redirect(url_for('management.reqtemp.index'))


@mngreqtemp.get('/request/edit')
def request_edit():
    data = dict()
    data['request'] = get_detail_request_template()

    return render_template(
        title=TITLE_DASHBD,
        data=data,
        template_name_or_list='detailTemplate.html'
    )


@mngreqtemp.post('/request/edit/')
def request_edit_proccess():
    dataInput = request.form.to_dict()
    file = request.files.get('fileDesign')
    if file:
        filedesign = file.read()
        fileMimeType = file.mimetype
        filedesign = base64.b64encode(filedesign).decode('utf-8')
        base64_string = f"data:{fileMimeType};base64,{filedesign}"
    else:
        filedesign = 0
    
    dataInput = {
        "req_id" : dataInput["req_id"],
        "category_id" : dataInput["category"], 
        "template_design" : base64_string, 
        "description" : dataInput["description"], 
        "deadline" : dataInput["deadline"], 
        "type" : dataInput["selTypeTemp"]
    }
    
    
    url = app.config['BE_URL'] + '/template/request'

    payload = json.dumps(dataInput)
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
            message=response.json().get('description'),
            category='danger'
        )
        return redirect(url_for('management.category.index'))
    else:
        flash(
            message=response.json().get('description'),
            category='success'
        )
        return redirect(url_for('management.category.index'))


# clear
@mngreqtemp.get('/request/delete')
def request_delete():
    data = dict()
    data['request'] = get_detail_request_template()
    
    return render_template(
        title=TITLE_DASHBD,
        data=data,
        template_name_or_list='deleteRequest.html'
    )

# clear
@mngreqtemp.get('/request/delete/')
def request_delete_proccess():
    reqId = request.args.get('reqId')
    
    dataInput = {
        "request_id" : reqId 
    }
    
    url = app.config['BE_URL'] + '/template/request'

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
        return redirect(url_for('management.reqtemp.request_delete', reqId=reqId))
    else:
        flash(
            message=response.json().get('message'),
            category='success'
        )
        return redirect(url_for('dashboard.index'))

# clear
@mngreqtemp.get('/request/detail')
def request_detail():
    data = dict()
    data['request'] = get_detail_request_template()

    return render_template(
        title=TITLE_DASHBD,
        data=data,
        template_name_or_list='detailRequest.html'
    )


@mngreqtemp.post('/request/update/status')
def update_reqstatus():
    dataInput = request.form.to_dict()
    reqId = dataInput['req_id']
    dataInput = {
        "req_id" : dataInput['req_id'],
        "status" : dataInput['status']
    }

    print(dataInput)
    payload = json.dumps(dataInput)
    url = app.config['BE_URL'] + '/template/request/status'

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
        return redirect(url_for('management.reqtemp.request_detail', reqId=reqId))
    else:
        flash(
            message=response.json().get('message'),
            category='success'
        )
        return redirect(url_for('management.reqtemp.request_detail', reqId=reqId))
