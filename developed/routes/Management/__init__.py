from flask import Blueprint, render_template, request, redirect, url_for, session, current_app as app

management = Blueprint (
    name='management', 
    import_name=__name__,
    url_prefix='/manage',
    template_folder='../../templates/pages/ManagementPage'
)


from .Category import categorymng
from .Template import templatemng

management.register_blueprint(categorymng)
management.register_blueprint(templatemng)