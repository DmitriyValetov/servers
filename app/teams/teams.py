import yaml
import os


teams_file = os.path.join(os.path.split(__file__)[0], "teams.txt")

class team:
    def __init__(self, name, key, task_id, task_sequence, geo_position=None):
        self.name = name
        self.key = key 
        self.task_id = task_id
        self.task_sequence = task_sequence
        self.geo_position = geo_position

    def __repr__(self):
        return "team:: name:{}\n key:{}\n task_id:{}\n task_sequence: {}\n geo_position:{}\n".format(self.name, self.key, self.task_id, self.task_sequence, self.geo_position)


def load_teams(file_path=teams_file):
    with open(file=file_path, mode="r", encoding="utf-8") as fin:
        data = yaml.load(fin)
    if "teams" not in data.keys() or len(data["teams"])==0:
        raise BaseException("There are no teams in src data!") 
    
    teams = []   
    for t in data["teams"]:
         teams.append(team(t['name'], t['key'], t['task_id'], 
            t['task_sequence'], t['geo_position'] if 'geo_position' in t.keys() else None))

    return teams

def save_teams(teams, file_path=teams_file):
    data = dict()
    data['teams'] = []
    team_attributes = list(filter(lambda x: x[0]!='_', dir(teams[0])))

    for team in teams:
        team_dict = dict()
        for attr in team_attributes:
            team_dict[attr] = getattr(team, attr)
        data['teams'].append(team_dict)

    with open(file=file_path, mode="w", encoding="utf-8") as fout:
        yaml.dump(data, fout)


def reset_teams_progress(teams, file_path=teams_file):
    teams = load_teams()
    for team in teams:
        team.task_id = 0

    save_teams(teams)
    

def search_team(key, teams):
    for team in teams:
        if key == team.key:
            return team
    return None


teams = load_teams(teams_file)
