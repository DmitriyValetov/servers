from app import app, core
from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug.utils import secure_filename
from app.Optimization_Engine import General
import random


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect('/' + request.form['main_choice'])
    else:
        pass
    return render_template('index.html')

'''
Далее идут функции для каждого из пунктов главного меню:
    1) sensitivity
        1.1) sensitivity_settings
    2) optimization
        2.1) optimization_settings
        2.2) template_check
        2.3) instructions_check
    3) multivar_and_uncertainty
        3.1) multivar_and_uncertainty_settings
    4) gamma_test
    5) variogram_modeling
    6) stats_corr_analysis
    7) unconditional_generators
    8) conditional_generators
    

'''
"""
class inter:
    def __init__(self):
        pass
    def table(self, input = None): #таблицы должны быть прямоугольными
        pass 
"""  

class Optim:
    def __init__(self):
        #self.work_folder = None
        pass
    def set_work_folder(self, folder_name):
        self.work_folder = folder_name
    def set_executable_file(self, file_name):
        self.executable_file = file_name

optim = Optim()
#optim.set_work_folder(None)

@app.route('/debug', methods=['GET', 'POST'])
def deb(optim = optim):
    tab = [['удалить', 'line 1', 'spam', 'spam'],
           ['удалить', 'line 2', 'spam', 'spam'],
           ['удалить', 'line 3', 'spam', 'spam']]
    
    return render_template('debug.html', optim = optim)
    #df = pd.read_csv('static/table_test.csv', sep=';')
    #ht = df.to_html()
    #return render_template('debug2.html', table = ht)
    """
    tab = inter.table()
    tab = [['удалить', 'line 1', 'spam', 'spam'],
           ['удалить', 'line 2', 'spam', 'spam'],
           ['удалить', 'line 3', 'spam', 'spam']]
    return render_template('debug.html', table = tab, n_row = 3, n_col = 4)
    """

@app.route('/sensitivity', methods=['GET', 'POST'])
def sensitivity():
    if request.method == 'POST':
        if request.form['sens_command'] == 'open_cfg_file':
            fin = open('static/OstIn.txt')
            cfg_text = fin.read()
            fin.close()
                
        if request.form['sens_command'] == 'edit_settings':
            return redirect('/sensitivity/settings')
                
            #return redirect('/' + request.form['main_choice'])
    
    else:
        pass
    return render_template('sensitivity.html')

@app.route('/sensitivity/settings', methods=['GET', 'POST'])
def sensitivity_settings():
    return render_template('sensitivity_settings.html')

@app.route('/optimization', methods=['GET', 'POST'])
def optimization(cfg_text = None):
    if "optimization" not in core.keys():
        core[optimization] = dict()
        core[optimization]["opt"] = General.optimizator()

    if request.method == 'POST':
        if request.form['opt_command'] == 'open_cfg_file':
            fin = open('static/OstIn.txt')
            cfg_text = fin.read()
            fin.close()
            
        if request.form['opt_command'] == 'edit_settings':
            return redirect('/optimization/settings')
            
        #return redirect('/' + request.form['main_choice'])
    
    else:
        pass
    return render_template('optimization.html', cfg_text = cfg_text)


#вот здесь типа скрепка будет
@app.route('/optimization/settings', methods=['GET', 'POST'])
def optimization_settings(help_text = None, choice_method = None, params = None):
    parm_names = None
    default_params = None
    methods_names = core[optimization]["opt"].methods_names
    if request.method == 'POST':
        print(request.form)
        if "opt_command" in request.form.keys() and request.form['opt_command'] == 'open_clip':
            help_text = 'Рекомендую метод {}! \nОн отлично себя показал в прошлый раз.'.format(random.choice(methods_names))
        if "method_chosen" in request.form.keys():
            session["method_chosen"] = request.form["method_chosen"]
            parm_names = core[optimization]["opt"].get_method_parameters_names(session["method_chosen"])
            choice_method = session["method_chosen"]
            
        if "opt_command" in request.form.keys() and request.form['opt_command'] == 'load':
            default_params = core[optimization]["opt"].get_default_method_parameters(session["method_chosen"])
            parm_names = core[optimization]["opt"].get_method_parameters_names(session["method_chosen"])
            choice_method = session["method_chosen"]
            print(default_params)

    return  render_template('optimization_settings.html', help_text = help_text,
                           choice_method = choice_method, euristic_methods_names=methods_names, params_names=parm_names, params = default_params)
    
@app.route('/multivar_and_uncertainty', methods=['GET', 'POST'])
def multivar_and_uncertainty():
    if request.method == 'POST':           
        if request.form['command'] == 'edit_settings':
            return redirect('/multivar_and_uncertainty/settings')
    else:
        pass
    return render_template('multivar_and_uncertainty.html')

@app.route('/multivar_and_uncertainty/settings', methods=['GET', 'POST'])
def multivar_and_uncertainty_settings():
    return render_template('multivar_and_uncertainty_settings.html')

@app.route('/gamma_test', methods=['GET', 'POST'])
def gamma_test():
    return render_template('gamma_test.html')

@app.route('/variogram_modeling', methods=['GET', 'POST'])
def variogram_modeling():
    return render_template('variogram_modeling.html')

@app.route('/stats_corr_analysis', methods=['GET', 'POST'])
def stats_corr_analysis():
    return render_template('stats_corr_analysis.html')

@app.route('/unconditional_generators', methods=['GET', 'POST'])
def unconditional_generators():
    return render_template('unconditional_generators.html')

@app.route('/conditional_generators', methods=['GET', 'POST'])
def conditional_generators():
    return render_template('conditional_generators.html')