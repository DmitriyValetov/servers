from flask import (render_template,
                   redirect,
                   url_for)


from flask import Blueprint

module_1_blueprint = Blueprint(
    name = 'module_1',
    import_name = __name__,
    template_folder='./templates',
    static_folder='./static',
    url_prefix="/module_1"
)


@module_1_blueprint.route('/')
@module_1_blueprint.route('/<int:page>')
def slave_1_index(page=1):
    return render_template('module_1_index.html')