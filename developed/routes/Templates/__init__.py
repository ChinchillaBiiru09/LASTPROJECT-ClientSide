from flask import Blueprint, render_template, request, redirect, url_for, session, current_app as app

templates = Blueprint(
    name='templates',
    import_name=__name__,
    url_prefix='/templates',
    template_folder="../../templates/pages/TemplatesPage"
)


@templates.get('/')
def index():
    return render_template(
        title="Creavitation",
        template_name_or_list='templates.html'
    )

