from flask import request, render_template, redirect, url_for

from .forms import MyForm


def bind_all_routes(app):

    @app.route('/', methods=['GET', 'POST'])
    def index():
        print('\n\nrequest method: ', request.method)
        form = MyForm()
        print(form.name)
        name = form.name.data

        if request.method == 'POST' and name:
            name += '!'

        if form.validate_on_submit(): # works not always...
            name += '!'
            print('submitted!')

        return render_template('index.html', form=form, name=name)