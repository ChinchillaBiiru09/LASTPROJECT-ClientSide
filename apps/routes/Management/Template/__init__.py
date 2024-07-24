import base64
from flask import Blueprint, render_template, flash, request, redirect, url_for, session, current_app as app

from .... import TITLE_DASHBD
from ...utilities import *

import json, requests, base64, mimetypes

mngtemplate = Blueprint(
    name='template',
    import_name=__name__,
    url_prefix='/template',
    template_folder="../../../templates/pages/ManagementPage/Template"
)


@mngtemplate.get('/')
def index():
    data = dict()
    data['list_category'] = get_category()
    data['list_template'] = get_template()
    data['selected'] = 0


    return render_template(
        title=TITLE_DASHBD,
        data=data,
        template_name_or_list='template.html'
    )


@mngtemplate.get('/add')
def add():
    data = get_category()
    
    return render_template(
        title=TITLE_DASHBD,
        data=data,
        template_name_or_list='addTemplate.html'
    )


@mngtemplate.post('/add')
def add_proccess():
    dataInput = request.form.to_dict()
    thumbnail = request.files.get('thumbnail')
    css = request.files.get('css_file')
    js = request.files.get('js_file')
    wallpaper1 = request.files.get('Wallpaper1')
    wallpaper2 = request.files.get('Wallpaper2')
    if thumbnail:
        thumbnailFile = thumbnail.read()
        thumMime = thumbnail.mimetype
        thumbnailFile = base64.b64encode(thumbnailFile).decode('utf-8')
        thum_base64 = f"data:{thumMime};base64,{thumbnailFile}"
    else:
        thum_base64 = ""

    if css:
        cssFile = css.read()
        cssMime = css.mimetype
        cssFile = base64.b64encode(cssFile).decode('utf-8')
        css_base64 = f"data:{cssMime};base64,{cssFile}"
    else:
        css_base64 = ""

    if js:
        jsFile = js.read()
        jsMime = js.mimetype
        jsFile = base64.b64encode(jsFile).decode('utf-8')
        js_base64 = f"data:{jsMime};base64,{jsFile}"
    else:
        js_base64 = ""

    if wallpaper1:
        wallFile = wallpaper1.read()
        wallMime = wallpaper1.mimetype
        wallFile = base64.b64encode(wallFile).decode('utf-8')
        wall1_base64 = f"data:{wallMime};base64,{wallFile}"
    else:
        wall1_base64 = ""
    
    if wallpaper2:
        wallFile = wallpaper2.read()
        wallMime = wallpaper2.mimetype
        wallFile = base64.b64encode(wallFile).decode('utf-8')
        wall2_base64 = f"data:{wallMime};base64,{wallFile}"
    else:
        wall2_base64 = ""
    
    dataInput = {
        "category_id" : dataInput["category"], 
        "thumbnail" : thum_base64, 
        "css_file" : css_base64, 
        "js_file" : js_base64, 
        "wallpaper_1" : wall1_base64, 
        "wallpaper_2" : wall2_base64, 
        "title" : dataInput["title"]
        }
    
    url = app.config['BE_URL'] + '/template/'

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
        return redirect(url_for('management.template.add'))
    else:
        flash(
            message=response.json().get('message'),
            category='success'
        )
        return redirect(url_for('management.template.index'))


@mngtemplate.get('/edit')
def edit():
    data = dict()
    data['category'] = get_category()
    data['template'] = get_detail_template()

    return render_template(

        title=TITLE_DASHBD,
        data=data,
        template_name_or_list='editTemplate.html'
    )


@mngtemplate.post('/edit')
def edit_proccess():
    dataInput = request.form.to_dict()
    tempId = dataInput['template_id']
    thumbnail = request.files.get('thumbnail')
    css = request.files.get('css_file')
    js = request.files.get('js_file')
    wallpaper = request.files.get('Wallpaper')
    wallpaper2 = request.files.get('Wallpaper_2')

    if thumbnail:
        thumbnailFile = thumbnail.read()
        thumMime = thumbnail.mimetype
        thumbnailFile = base64.b64encode(thumbnailFile).decode('utf-8')
        thum_base64 = f"data:{thumMime};base64,{thumbnailFile}"
    else:
        thum_base64 = dataInput['thumbnail_old']

    if css:
        cssFile = css.read()
        cssMime = css.mimetype
        cssFile = base64.b64encode(cssFile).decode('utf-8')
        css_base64 = f"data:{cssMime};base64,{cssFile}"
    else:
        css_base64 = dataInput['css_old']

    if js:
        jsFile = js.read()
        jsMime = js.mimetype
        jsFile = base64.b64encode(jsFile).decode('utf-8')
        js_base64 = f"data:{jsMime};base64,{jsFile}"
    else:
        js_base64 = dataInput['js_old']

    if wallpaper:
        wallFile = wallpaper.read()
        wallMime = wallpaper.mimetype
        wallFile = base64.b64encode(wallFile).decode('utf-8')
        wall1_base64 = f"data:{wallMime};base64,{wallFile}"
    else:
        wall1_base64 = dataInput['wallpaper_old']
    
    if wallpaper2:
        wallFile = wallpaper.read()
        wallMime = wallpaper.mimetype
        wallFile = base64.b64encode(wallFile).decode('utf-8')
        wall2_base64 = f"data:{wallMime};base64,{wallFile}"
    else:
        wall2_base64 = dataInput['wallpaper_2_old']

    dataInput = {
        "template_id" : tempId,
        "category_id" : dataInput["category"],
        "thumbnail" : thum_base64, 
        "css_file" : css_base64, 
        "js_file" : js_base64, 
        "wallpaper_1" : wall1_base64, 
        "wallpaper_2" : wall2_base64, 
        "title" : dataInput["title"]
    }
    
    
    url = app.config['BE_URL'] + '/template/'

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
            message=response.json().get('message'),
            category='danger'
        )
        return redirect(url_for('management.template.edit', temId=tempId))
    else:
        flash(
            message=response.json().get('message'),
            category='success'
        )
        return redirect(url_for('management.template.index'))


# Clear
@mngtemplate.get('/delete')
def delete():
    data = dict()
    data['template'] = get_detail_template()

    return render_template(
        title=TITLE_DASHBD,
        data=data,
        template_name_or_list='deleteTemplate.html'
    )


# Clear
@mngtemplate.get('/delete/id')
def delete_proccess():
    id = request.args.get('id')
    dataInput = {
        "template_id" : id
    }          

    url = app.config['BE_URL'] + '/template/'
    headers = {
        'Authorization' : f'Bearer {session["user"]["access_token"]}',
        'Content-Type' : 'application/json'
    }
    print(dataInput)

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
        return redirect(url_for('management.template.delete', temId=id))
    else:
        flash(
            message=response.json().get('message'),
            category='success'
        )
        return redirect(url_for('management.template.index'))


# @mngtemplate.get('/detail')
# def detail():
#     data = dict()
#     data = get_detail_template()
#     return render_template(
#         title=TITLE_DASHBD,
#         data=data,
#         template_name_or_list='detailTemplate.html'
#     )


@mngtemplate.get('/request')
def request_create():
    data = dict()
    data['list_category'] = get_category()

    return render_template(
        title=TITLE_DASHBD,
        data=data,
        template_name_or_list='Request/addRequest.html'
    )


@mngtemplate.post('/request')
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
    
    
    url = app.config['BE_URL'] + '/template/request'

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
        return redirect(url_for('management.template.request_create'))
    else:
        flash(
            message=response.json().get('message'),
            category='success'
        )
        return redirect(url_for('management.template.index'))


@mngtemplate.get('/request/edit')
def request_edit():
    data = dict()
    data['request'] = get_detail_request_template()

    return render_template(
        title=TITLE_DASHBD,
        data=data,
        template_name_or_list='detailTemplate.html'
    )


@mngtemplate.post('/request/edit/')
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
@mngtemplate.get('/request/delete')
def request_delete():
    data = dict()
    data['request'] = get_detail_request_template()
    
    return render_template(
        title=TITLE_DASHBD,
        data=data,
        template_name_or_list='Request/deleteRequest.html'
    )


@mngtemplate.get('/request/delete/')
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
        return redirect(url_for('management.template.request_delete', reqId=reqId))
    else:
        flash(
            message=response.json().get('message'),
            category='success'
        )
        return redirect(url_for('dashboard.index'))


@mngtemplate.get('/request/detail')
def request_detail():
    data = dict()
    data['request'] = get_detail_request_template()

    return render_template(
        title=TITLE_DASHBD,
        data=data,
        template_name_or_list='Request/detailRequest.html'
    )


@mngtemplate.post('/request/update/status')
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
        return redirect(url_for('management.template.request_detail', reqId=reqId))
    else:
        flash(
            message=response.json().get('message'),
            category='success'
        )
        return redirect(url_for('management.template.request_detail', reqId=reqId))
