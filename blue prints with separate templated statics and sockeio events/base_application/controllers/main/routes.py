from flask import (render_template,
                   redirect,
                   url_for,
                   request,
                   session,
                   g)



from flask import Blueprint

# have to be initialized in routes file
main_blueprint = Blueprint(
    name = 'main',
    import_name = __name__,
    template_folder='./templates/',
    static_folder='./static', # add 'static_folder=None' in Flask(__name__, ***)
    url_prefix='/'
)

# from .blueprint import main_blueprint


@main_blueprint.route('/')
def index():
    return render_template('index.html')