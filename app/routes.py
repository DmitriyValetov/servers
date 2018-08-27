from app import app
from flask import Flask, request, render_template, redirect, url_for, session

from .teams import teams, search_team, save_teams
from .tasks import tasks 

@app.route('/', methods=['GET', 'POST'])
def index():
    print("index page: {}".format(request.method))
    if request.method == 'POST':
        print("index page form: {}".format(request.form))
    
        if request.form['control_button'] == 'login':
            key = request.form['key']
            team = search_team(key, teams)
            if team is None:
                return render_template('index.html', log_text="there is no team with this key!")
            else:
                print('team: \"{}\"  redirected to task page'.format(team.name))
                return redirect(url_for('task'), code=307)
    
    return render_template('index.html')


@app.route('/task', methods=['GET', 'POST'])
def task():
    print("task page: {}".format(request.method))
    if request.method == "POST":
        print("task page form: {}".format(request.form))

        if 'key' not in request.form.keys():
            print("there is not key in request - redirect to index")
            return redirect(url_for('index'))
        key = request.form['key']
        team = search_team(key, teams)
        if team is None:
            return redirect(url_for('index'))
        print("team {} entered task page.".format(team.name))
        print("team {} has task_id: {}".format(team.name, team.task_id))
        print("team {} task sequence is {}".format(team.name, team.task_sequence))

        if team.task_id is None:
            print("team {} has ended the game already.".format(team.name))
            print("team {} redirect to end_game page.".format(team.name))
            return redirect(url_for('end_game'), code=307)

        elif team.task_id >= len(team.task_sequence):
            print("team {} has just ended the game already.".format(team.name))
            print("team {} redirect to end_game page.".format(team.name))
            team.task_id = None # finale
            return redirect(url_for('end_game'), code=307)

        else:
            task = tasks[team.task_sequence[team.task_id]]

            if 'answer' in request.form.keys():
                team_answer = request.form['answer']
                # answering by submit
                if team_answer in task.answer:
                    print("team {} answered correctly on {} with {}.".format(team.name, task.text, team_answer))
                    print("correct answers are: {}".format(task.answer))
                    team.task_id += 1
                    save_teams(teams)
                    return redirect(url_for('success'), code='307')
                else:
                    print("team {} answered incorrectly on {} with {}.".format(team.name, task.text, team_answer))
                    print("correct answers are: {}".format(task.answer))
                    return redirect(url_for('fail'), code='307')
            else:
                # first time
                print("teams attempts to answer {}".format(task.text))
                print("correct answers are: {}".format(task.answer))
                return render_template('task.html', tip=task.tip, text=task.text, key=key)


    print("strange enter the task page - redirect tot index")
    return redirect(url_for('index'))


@app.route('/end_game', methods=['GET', 'POST'])
def end_game():
    print("end_game page: {}".format(request.method))
    if 'key' in request.form.keys():
        key = request.form['key']
    else:
        key = None
    return render_template('end_game.html', key=key)


@app.route('/success', methods=['GET', 'POST'])
def success():
    print("success page: {}".format(request.method))
    if 'key' in request.form.keys():
        key = request.form['key']
    else:
        key = None
    return render_template('success.html', key=key)


@app.route('/fail', methods=['GET', 'POST'])
def fail():
    print("fail page: {}".format(request.method))
    if 'key' in request.form.keys():
        key = request.form['key']
    else:
        key = None
    return render_template('fail.html', key=key)