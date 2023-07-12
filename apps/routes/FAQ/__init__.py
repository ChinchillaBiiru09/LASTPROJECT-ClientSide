from flask import Blueprint, render_template, request, redirect, url_for, session, current_app as app

faq = Blueprint(
    name='faq',
    import_name=__name__,
    url_prefix='/faq',
    template_folder="../../templates/pages/FAQPage"
)

@faq.before_request
def cek_session():
    if session.get('user') == None:
        return redirect(url_for('auth.sign_in'))
    
    # decode = decode_jwt(session['user']['access_token'])
    if session['user']['role']=='ADMIN':
        return redirect(url_for('dashboard.admin'))
    # elif session['user']['role']=='USER':
    #     # return redirect(url_for('dashboard.index'))
    #     pass
    else:
        # return redirect(url_for("logout", message="Sesi login anda telah habis silahkan login ulang"))
        # Cek apakah token masih berlaku
        response = requests.request (
            method='GET',
            url=app.config['BE_URL'] + '/auth/',
            headers={"Authorization" : f"Bearer {session['user']['access_token']}"}
        )
        if response.status_code == 401:
            return redirect(url_for("logout", message="Sesi login anda telah habis silahkan login ulang"))


@faq.get('/')
def index():
    return render_template(
        title="Creavitation",
        template_name_or_list='faq.html'
    )

