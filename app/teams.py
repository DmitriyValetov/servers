import yaml
import os

class team:
    def __init__(self, name, key, task_id, position=None):
        self.name = name
        self.key = key 
        self.task_id = task_id
        self.position = position
    def __repr__(self):
        return "team:: name:{}\n key:{}\n task_id:{}\n position:{}\n".format(self.name, self.key, self.task_id, self.position)


def load_teams(file_path):
    with open(file=file_path, mode="r", encoding="utf-8") as fin:
        data = yaml.load(fin)
    if "teams" not in data.keys() or len(data["teams"])==0:
        raise BaseException("There are no teams in src data!") 
    
    teams = []   
    for t in data["teams"]:
         teams.append(team(t['name'], t['key'], t['task_id'], t['position'] if 'position' in t.keys() else None))

    return teams


teams_file = os.path.join(os.path.split(__file__)[0], "teams.txt")
teams = load_teams(teams_file)
