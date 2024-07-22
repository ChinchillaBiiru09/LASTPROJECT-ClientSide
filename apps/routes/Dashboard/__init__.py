from flask import Blueprint, render_template, redirect, url_for, session, current_app as app

from ... import TITLE_DASHBD
from ..utilities import decode_jwt, get_count_category, get_count_template, get_count_user, get_count_invitation, get_count_guest, get_count_greeting, get_category_popular, get_recent_invitation, get_request_template


dashboard = Blueprint(
    name='dashboard',
    import_name=__name__,
    url_prefix='/dashboard',
    template_folder="../../templates/pages/DashboardPage"
)


@dashboard.before_request
def cek_session():  
    if session.get('user') is None:
        return redirect(url_for('auth.sign_in'))
    
    decode_token, error_message = decode_jwt(session['user']['access_token'])
    if decode_token:
        for data in decode_token:
            session['user'][data] = decode_token[data]
    else:
        return redirect(url_for('signout', message=error_message))


@dashboard.get('/')
def index(): # Clear
    data = dict()
    data['count_invitation'] = get_count_invitation()
    data['template_request'] = get_request_template()
    
    if session['user']['role'] == "ADMIN":
        data['count_category'] = get_count_category()
        data['count_template'] = get_count_template()
        data['count_user'] = get_count_user()

        return render_template(
            title=TITLE_DASHBD,
            data=data,
            template_name_or_list='dash_admin.html',
            active='dashboard.index'
        )
    elif session['user']['role'] == "USER":
        data['count_guest'] = get_count_guest()
        data['count_greeting'] = get_count_greeting()

        return render_template(
            title=TITLE_DASHBD,
            data=data,
            template_name_or_list='dash_user.html',
            active='dashboard.index'
        )
