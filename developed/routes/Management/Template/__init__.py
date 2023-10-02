from flask import Blueprint, render_template, request, redirect, url_for, session, current_app as app
from .... import TITLE_DASHBD


templatemng = Blueprint(
    name='template',
    import_name=__name__,
    url_prefix='/template',
    template_folder="../../../templates/pages/ManagementPage/TemplateMngPage"
)


@templatemng.get('/')
def index():
    return render_template(
        title=TITLE_DASHBD,
        template_name_or_list='template.html'
    )

