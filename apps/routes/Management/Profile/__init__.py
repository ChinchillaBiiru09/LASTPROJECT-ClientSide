from flask import Blueprint, render_template, session, current_app as app
from .... import TITLE_DASHBD
from ...utilities import get_profile, get_log

import requests


mngprofile = Blueprint(
    name='profile',
    import_name=__name__,
    url_prefix='/user',
    template_folder="../../../templates/pages/ManagementPage/Profile"
)


@mngprofile.get('/profile')
def profile_view():
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


@mngprofile.get('/profile/edit')
def profile_edit():
    return render_template(
        title=TITLE_DASHBD,
        template_name_or_list='viewUser.html'
    )
