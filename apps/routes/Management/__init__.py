from flask import Blueprint, redirect, url_for, session

from ..utilities import decode_jwt


management = Blueprint (
    name='management', 
    import_name=__name__,
    url_prefix='/manage',
    template_folder='../../templates/pages/ManagementPage'
)


@management.before_request
def cek_session():
    if session.get('user') is None:
        return redirect(url_for('auth.sign_in'))
    
    decode_token, error_message = decode_jwt(session['user']['access_token'])
    if decode_token:
        for data in decode_token:
            session['user'][data] = decode_token[data]
    else:
        return redirect(url_for('signout', message=error_message))


from .Category import mngcategory
from .Invitation import mnginvitation
from .Template import mngtemplate
from .User import mnguser
from .Profile import mngprofile

management.register_blueprint(mngcategory)
management.register_blueprint(mnginvitation)
management.register_blueprint( mngtemplate)
management.register_blueprint(mnguser)
management.register_blueprint(mngprofile)