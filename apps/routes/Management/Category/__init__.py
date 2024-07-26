from turtle import title
from flask import Blueprint, render_template, make_response, request, redirect, url_for, session, flash, current_app as app

from .... import TITLE_DASHBD
from ...utilities import get_category, get_detail_category

import json, requests

mngcategory = Blueprint(
    name='category',
    import_name=__name__,
    url_prefix='/category',
    template_folder="../../../templates/pages/ManagementPage/Category"
)


@mngcategory.get('/')
def index():
    if session['user']['role'] == "USER":
        return app.errorhandler(403)
    
    data = get_category()
    return render_template(
        title=TITLE_DASHBD,
        template_name_or_list='category.html',
        data=data
    )


@mngcategory.get('/add')
def add():
    data = get_category()
    return render_template(
        title=TITLE_DASHBD,
        template_name_or_list='addCategory.html',
        data=data
    )


@mngcategory.post('/add')
def add_proccess():
    dataInput = request.form.to_dict()

    dumps1 = []
    dumps2 = []
    for key in dataInput:
        if key == "category":
            continue
        if key[:-1] == "format-data-":
            dumps1.append(key)
        if key[:-1] == "mandatory-":
            dumps2.append(key)
    
    if len(dumps1) != len(dumps2):
        for i in dumps1:
            s = "mandatory-"+i[-1]
            if s not in dumps2:
                dumps2.append(s)
    
    for d2 in dumps2:
        print(d2)
        if d2 in dataInput:
            dataInput[d2] = "required"
        else:
            dataInput[d2] = "optional"

    dumps3 = []
    for d1 in dumps1:
        data = {
            dataInput[d1] : ""
        }
        dumps3.append(data)

    for di in dataInput:
        if di in dumps2:
            for d1 in dumps1:
                if di[-1] == d1[-1]:
                    for d3 in dumps3:
                        if dataInput[d1] in d3:
                            d = dataInput[d1]
                            d3[d] = dataInput[di]
                        
    dumps4 = {}
    for d3 in dumps3:
        for d in d3:
            dumps4[d] = d3[d]

    dataInput = {
        "category" : dataInput["category"],
        "format_data" : dumps4
    }

    url = app.config['BE_URL'] + '/category/'

    payload = json.dumps(dataInput)
    headers = {
        'Authorization' : f'Bearer {session["user"]["access_token"]}',
        'Content-Type' : 'application/json'
    }
    # return redirect(url_for('management.category.index'))
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
        return redirect(url_for('management.category.add'))
    else:
        flash(
            message=response.json().get('message'),
            category='success'
        )
        return redirect(url_for('management.category.index'))


@mngcategory.get('/edit')
def edit():
    data = get_detail_category()
    return render_template(
        title=TITLE_DASHBD,
        template_name_or_list='editCategory.html',
        data=data
    )


@mngcategory.post('/edit')
def edit_proccess():
    dataInput = request.form.to_dict()
    data = {}
    i = 1
    dumps1 = []
    dumps2 = []
    for key in dataInput:
        if key == "category":
            continue
        if key[:-1] == "format-data-":
            dumps1.append(key)
        if key[:-1] == "mandatory-":
            dumps2.append(key)

    if len(dumps1) != len(dumps2):
        for i in dumps1:
            s = "mandatory-"+i[-1]
            if s not in dumps2:
                dumps2.append(s)
    
    for d2 in dumps2:
        if d2 in dataInput:
            dataInput[d2] = "required"
        else:
            dataInput[d2] = "optional"

    dumps3 = []
    for d1 in dumps1:
        data = {
            dataInput[d1] : ""
        }
        dumps3.append(data)

    for di in dataInput:
        if di in dumps2:
            for d1 in dumps1:
                if di[-1] == d1[-1]:
                    for d3 in dumps3:
                        if dataInput[d1] in d3:
                            d = dataInput[d1]
                            d3[d] = dataInput[di]
                        
    dumps4 = {}
    for d3 in dumps3:
        for d in d3:
            dumps4[d] = d3[d]
    
    dataInput = {
        "category_id" : dataInput["category-id"],
        "category" : dataInput["category"],
        "format_data" : dumps4
    }
    id = dataInput['category_id']

    url = app.config['BE_URL'] + '/category/'

    # Set headers url
    headers = {
        'Authorization' : f'Bearer {session["user"]["access_token"]}',
        'Content-Type' : 'application/json'
    }
    
    # request response ke BE api
    payload = json.dumps(dataInput)
    response = requests.request(
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
        return redirect(url_for('management.category.edit', id=id))
    else:
        flash(
            message=response.json().get('message'),
            category='success'
        )
        return redirect(url_for('management.category.index'))


@mngcategory.get('/delete')
def delete():
    data = get_detail_category()
    print(data)

    return render_template(
        title=TITLE_DASHBD,
        data=data,
        template_name_or_list='deleteCategory.html'
    )


@mngcategory.get('/delete/data')
def delete_proccess():
    id = request.args.get('id')
    dataInput = {
        "category_id" : id
    }  

    url = app.config['BE_URL'] + '/category/'
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
        return redirect(url_for('management.category.delete'))
    else:
        flash(
            message=response.json().get('message'),
            category='success'
        )
        return redirect(url_for('management.category.index'))

