import yaml
import os

class task:
    def __init__(self, location, task_text, answer, post_text):
        self.location = location
        self.task_text = task_text
        self.answer = answer
        self.post_text = post_text

    def __repr__(self):
        return "\nlocation: {}\n task_text:{}\n answer:{}\n post_text:{}\n\n".format(self.location, 
            self.task_text, self.answer, self.post_text)


def load_tasks(file_path):
    with open(file=file_path, mode="r", encoding="utf-8") as fin:
        data = yaml.load(fin)
    if "tasks" not in data.keys() or len(data["tasks"])==0:
        raise BaseException("There are no tasks in src data!") 
    
    tasks = []   
    for t in data["tasks"]:
         tasks.append(task(t['location'], t['task_text'], t['answer'], t['post_text']))

    return tasks


def load_all_tasks():
    files = os.listdir(os.path.split(__file__)[0])
    tasks_files = list(filter(lambda f: os.path.splitext(f)[1]=='.txt', files))

    tasks = dict()

    for f in tasks_files:
        team = f.split('.')[0]
        tasks[team] = []

        with open(file=os.path.join(os.path.split(__file__)[0], f), mode="r", encoding="utf-8") as fin:
            data = yaml.load(fin)
        
        if "tasks" not in data.keys() or len(data["tasks"])==0:
            raise BaseException("There are no tasks in src data!") 

        for t in data["tasks"]:
            tasks[team].append(task(t['location'], t['task_text'], t['answer'], t['post_text']))

    return tasks


tasks_file = os.path.join(os.path.split(__file__)[0], "tasks.txt")
tasks = load_all_tasks() # load_tasks(tasks_file)

def get_tasks_file(tasks_file=tasks_file):
    with open(file=tasks_file, mode="r") as fin:
        data = fin.read()
    return data

def get_tasks_file_by_team_name(team_name):
    file_path = os.path.join(os.path.split(__file__)[0], "{}.txt".format(team_name))
    if not os.path.exists(file_path):
        return None

    with open(file=file_path, mode="r") as fin:
        data = fin.read()
    return data


def get_tasks_by_team_name(team_name):
    file_path = os.path.join(os.path.split(__file__)[0], "{}.txt".format(team_name))
    if not os.path.exists(file_path):
        return "no task data for this team: {}".format(team_name)

    with open(file=file_path, mode="r") as fin:
        tasks_dicts_list = yaml.load(fin)['tasks']

    tasks = []
    for t in tasks_dicts_list:
        tasks.append(task(t['location'], t['task_text'], t['answer'], t['post_text']))
    return tasks

def save_tasks_file_by_team_name(team_name, data):
    file_path = os.path.join(os.path.split(__file__)[0], "{}.txt".format(team_name))
    with open(file=file_path, mode="w") as fin:
        fin.write(data)