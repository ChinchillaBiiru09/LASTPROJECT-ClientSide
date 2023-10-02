from flask import Blueprint, render_template, request, redirect, url_for, session, current_app as app
from .... import TITLE_DASHBD


categorymng = Blueprint(
    name='category',
    import_name=__name__,
    url_prefix='/category',
    template_folder="../../../templates/pages/ManagementPage/CategoryMngPage"
)


@categorymng.get('/')
def index():
    return render_template(
        title=TITLE_DASHBD,
        template_name_or_list='category.html'
    )

