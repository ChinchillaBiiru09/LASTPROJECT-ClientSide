from flask import Blueprint, render_template, session, request, flash, redirect, url_for, current_app as app
from .... import TITLE_DASHBD
from ...utilities import get_profile, get_log

import requests, json


mngprofile = Blueprint(
    name='profile',
    import_name=__name__,
    url_prefix='/user/profile',
    template_folder="../../../templates/pages/ManagementPage/Profile"
)


@mngprofile.get('/')
def index():
    try:
        data = dict()
        data['profile'] = get_profile()
        data['log'] = get_log()

        return render_template(
            data=data,
            title=TITLE_DASHBD,
            template_name_or_list='profile.html'
        )
    
    except Exception as e:
        return str(e)


@mngprofile.post('/edit')
def edit_process():
    try:
        dataInput = request.form.to_dict()
        dataInput = {
            "first_name" : dataInput['f_name'],
            "middle_name" : dataInput['m_name'],
            "last_name" : dataInput['l_name'],
            "phone" : dataInput['phone'],
        }

        # Create URL
        url = app.config['BE_URL'] + '/profile/'

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
            return redirect(url_for('management.profile.index'))
        else:
            flash(
                message=response.json().get('message'),
                category='success'
            )
            return redirect(url_for('management.profile.index'))


    except Exception as e:
        return str(e)