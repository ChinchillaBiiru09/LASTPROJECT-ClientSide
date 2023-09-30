from flask import Blueprint, render_template, request, redirect, url_for, session, current_app as app
from ... import TITLE_DASHBD
from .utilities import get_templates, get_count_invitation, get_count_guest, get_count_greeting, decode_jwt

import requests


dashboard = Blueprint(
    name='dashboard',
    import_name=__name__,
    url_prefix='/dashboard',
    template_folder="../../templates/pages/DashboardPage"
)


# @dashboard.before_request
# def cek_session():
#     if session.get('user') == None:
#         return redirect(url_for('auth.sign_in'))
    
#     # decode = decode_jwt(session['user']['access_token'])
#     if session['user']['role']=='ADMIN':
#         return redirect(url_for('dashboard.admin'))
#     # elif session['user']['role']=='USER':
#     #     # return redirect(url_for('dashboard.index'))
#     #     pass
#     else:
#         # return redirect(url_for("logout", message="Sesi login anda telah habis silahkan login ulang"))
#         # Cek apakah token masih berlaku
#         response = requests.request (
#             method='GET',
#             url=app.config['BE_URL'] + '/auth/',
#             headers={"Authorization" : f"Bearer {session['user']['access_token']}"}
#         )
#         if response.status_code == 401:
#             return redirect(url_for("logout", message="Sesi login anda telah habis silahkan login ulang"))


@dashboard.get('/')
def index():
    data = dict()
    data['templates'] = get_templates()
    data['count_invit'] = get_count_invitation()
    data['count_guest'] = get_count_guest()
    data['count_greeting'] = get_count_greeting()
    return render_template(
        title=TITLE_DASHBD,
        data=data,
        template_name_or_list='dashboard.html',
        active='dashboard.index'
    )

