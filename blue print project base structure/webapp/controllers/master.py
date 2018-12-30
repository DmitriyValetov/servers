from flask import (render_template,
                   current_app,
                   Blueprint,
                   redirect,
                   url_for,
                   request,
                   flash,
                   session)


master_blueprint = Blueprint(
    'master',
    __name__,
    template_folder='../templates/master'
)


@master_blueprint.route('/')
def index():
    return render_template('index.html')