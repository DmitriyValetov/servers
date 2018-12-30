from flask import (render_template,
                   Blueprint,
                   redirect,
                   url_for,
                   abort)


slave_1_blueprint = Blueprint(
    'slave_1',
    __name__,
    template_folder='../templates/slave_1',
    url_prefix="/slave_1"
)


@slave_1_blueprint.route('/')
@slave_1_blueprint.route('/<int:page>')
def slave_1_index(page=1):
    return render_template('slave_1_index.html')