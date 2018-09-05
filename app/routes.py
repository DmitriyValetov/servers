from app import app
from flask import Flask, request, render_template, redirect, url_for, session

from .teams import teams, search_team, save_team, load_team_text, save_team_text_and_reload_this_team, search_team_index
from .tasks import tasks, save_tasks_file_by_team_name, get_tasks_file_by_team_name, get_tasks_by_team_name


admin_key = '638732'

@app.route('/', methods=['GET', 'POST'])
def index():
    print("index page: {}".format(request.method))
    if request.method == 'POST':
        print("index page form: {}".format(request.form))
    
        if request.form['control_button'] == 'login':
            
            if request.form['key'] == admin_key:
                return redirect(url_for('admin'), code=307)

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

        if team.task_id is None:
            print("team {} has ended the game already.".format(team.name))
            print("team {} redirect to end_game page.".format(team.name))
            return redirect(url_for('end_game'), code=307)

        elif team.task_id >= len(tasks[team.name]):
            print("team {} has just ended the game already.".format(team.name))
            print("team {} redirect to end_game page.".format(team.name))
            team.task_id = None # finale
            return redirect(url_for('end_game'), code=307)

        else:
            task = tasks[team.name][team.task_id]

            if 'answer' in request.form.keys():
                team_answer = request.form['answer']
                # answering by submit
                if team_answer in task.answer:
                    print("team {} answered correctly on {} with {}.".format(team.name, task.task_text, team_answer))
                    print("correct answers are: {}".format(task.answer))
                    team.task_id += 1
                    save_team(team)
                    return redirect(url_for('success'), code='307')
                else:
                    print("team {} answered incorrectly on {} with {}.".format(team.name, task.task_text, team_answer))
                    print("correct answers are: {}".format(task.answer))
                    return redirect(url_for('fail'), code='307')
            else:
                # first time
                print("teams attempts to answer {}".format(task.task_text))
                print("correct answers are: {}".format(task.answer))
                return render_template('task.html', location=task.location, task_text=task.task_text, key=key)


    print("strange enter the task page - redirect tot index")
    return redirect(url_for('index'))


@app.route('/end_game', methods=['POST'])
def end_game():
    print("end_game page: {}".format(request.method))
    if 'key' in request.form.keys():
        key = request.form['key']
    else:
        return redirect(url_for('index'))

    team = search_team(key, teams)
    print("{} are on end_game page.".format(team.name))

    return render_template('end_game.html', key=key)


@app.route('/success', methods=['POST'])
def success():
    print("success page: {}".format(request.method))
    if 'key' in request.form.keys():
        key = request.form['key']
    else:
        return redirect(url_for('index'))

    team = search_team(key, teams)
    task = tasks[team.name][team.task_id-1]# old to get post text
    print("{} are on success page.".format(team.name))

    if request.method == 'POST' and "control_button" in request.form.keys() \
        and request.form["control_button"] == 'Продолжить':
        return redirect(url_for('task'), code=307)

    return render_template('success.html', key=key, post_text=task.post_text)


@app.route('/fail', methods=['POST'])
def fail():
    print("fail page: {}".format(request.method))
    if 'key' in request.form.keys():
        key = request.form['key']
    else:
        return redirect(url_for('index'))

    team = search_team(key, teams)
    print("{} are on fail page.".format(team.name))

    if request.method == 'POST' and "control_button" in request.form.keys() \
        and request.form["control_button"] == 'Попробовать снова':
        return redirect(url_for('task'), code=307)
    
    return render_template('fail.html', key=key)


@app.route('/admin', methods=['POST'])
def admin():
    page_template_file = 'admin.html'

    if request.method == 'POST':

        if admin_key != request.form['key']:
            return redirect(url_for('index'))
        key = request.form['key']
        print(request.form)

        # modes:
        # 0) main menu:
        #  - reset all teams == action
        #  - get definite team data in text area
        #  - get geolocation
        #  - get tasks in text area

        # sub menu
        # 1) definite team data choose
        # 2) get geolocation map
        # 3) text area for definite team data or tasks


        # no mode == main menu
        if 'mode' not in request.form.keys():
            if 'control_button' in request.form.keys():

                if request.form['control_button'] == 'reset_all':
                    print("Reseting the teams: ")
                    for team in teams:
                        team.task_id = 0
                        print(team)
                        save_team(team)

                    return render_template(page_template_file, key=key)


                elif request.form['control_button'] == 'edit_definite_team':
                    return render_template(page_template_file, key=key, mode='edit_definite_team', teams=teams)

                elif request.form['control_button'] == 'edit_tasks':
                    return render_template(page_template_file, key=key, mode='edit_tasks', teams=teams)

                elif request.form['control_button'] == 'geomap':
                    return render_template(page_template_file, key=key, mode='geomap')

        else: # with a mode teg
            if request.form['mode'] == 'edit_tasks':

                    
                # choose team to look into it's tasks:
                if 'team_key' not in request.form.keys(): # another time choose the team
                    # return from choosing the team to edit it's taks to admin menu:
                    if 'control_button' in request.form.keys() and request.form['control_button'] == 'cancel':
                        return render_template(page_template_file, key=key, mode=None)

                    return render_template(page_template_file, key=key, mode='edit_tasks', teams=teams)
                else:

                    # return from team tasks to choosing the team for tasks editing
                    team = search_team(request.form['team_key'], teams)                    
                    if 'control_button' in request.form.keys():
                        if request.form['control_button'] == 'cancel':
                            return render_template(page_template_file, key=key, mode='edit_tasks', teams=teams)

                        elif request.form['control_button'] == 'save':
                            save_tasks_file_by_team_name(team.name, request.form['tasks_text'])
                            tasks[team.name] = get_tasks_by_team_name(team.name)

                    # reopen and first enter the page and after save
                    tasks_text = get_tasks_file_by_team_name(team.name)
                    return render_template(page_template_file, key=key, mode='edit_tasks', 
                        team=team, tasks_text=tasks_text)

            elif request.form['mode'] == 'edit_definite_team':
                if "control_button" in request.form.keys():
                    if request.form['control_button'] == 'cancel' and 'team_text' not in request.form.keys():
                        return render_template(page_template_file, key=key) # back to main admin

                if 'team_key' not in request.form.keys(): # another time choose the team
                    return render_template(page_template_file, key=key, mode='edit_definite_team', teams=teams)
                else:
                    team = search_team(request.form['team_key'], teams)

                    if 'control_button' in request.form.keys():

                        if  request.form['control_button'] == 'save':
                            teams[search_team_index(team.key, teams)] = save_team_text_and_reload_this_team(team.name, request.form['team_text'])

                            # and return the same page with team data on it 

                        elif request.form['control_button'] == 'cancel':
                            return render_template(page_template_file, key=key, mode='edit_definite_team', teams=teams) 
                                 # back to choosing the team


                    #reload or first enter
                    team_text = load_team_text(team.name)
                    return render_template(page_template_file, key=key, mode='edit_definite_team', 
                        team=team, team_text=team_text)

        return render_template(page_template_file, key=key) 


    else: # GET request
        return redirect(url_for('index'))