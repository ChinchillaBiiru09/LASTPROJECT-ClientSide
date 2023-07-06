from flask import Blueprint, render_template, request, redirect, url_for, session, current_app as app

invitation = Blueprint(
    name='invitation',
    import_name=__name__,
    url_prefix='/invitation',
    template_folder="../../templates/pages/InvitationPage"
)


@invitation.get('/')
def create():
    return render_template(
        title="Creavitation",
        template_name_or_list='invitation.html'
    )

