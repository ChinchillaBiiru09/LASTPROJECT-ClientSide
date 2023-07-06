from flask import Blueprint, render_template, request, redirect, url_for, session, current_app as app

guest = Blueprint(
    name='guest',
    import_name=__name__,
    url_prefix='/guest',
    template_folder="../../templates/pages/GuestPage"
)


@guest.get('/')
def index():
    return render_template(
        title="Creavitation",
        template_name_or_list='guest.html'
    )

