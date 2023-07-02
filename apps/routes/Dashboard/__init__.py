from flask import Blueprint, render_template, request, redirect, url_for, session, current_app as app

dashboard = Blueprint(
    name='dashboard',
    import_name=__name__,
    url_prefix='/dashboard',
    template_folder="../../templates/pages/DashboardPage"
)


@dashboard.get('/')
def index():
    return render_template(
        title="Login Aplikasi Undangan Online",
        template_name_or_list='dashboard.html'
    )

