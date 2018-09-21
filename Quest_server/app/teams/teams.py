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


def load_teams():
    files = os.listdir(os.path.split(__file__)[0])
    team_files = list(filter(lambda f: os.path.splitext(f)[1]=='.txt', files))

    teams = [] 

    for f in team_files:
        with open(file=os.path.join(os.path.split(__file__)[0], f), mode="r", encoding="utf-8") as fin:
            data = yaml.load(fin)
        
        if "teams" not in data.keys() or len(data["teams"])==0:
            raise BaseException("There are no teams in src data!") 

        for t in data["teams"]:
            teams.append(team(t['name'], t['key'], t['task_id'], 
                t['task_sequence'], t['geo_position'] if 'geo_position' in t.keys() else None))

    return teams


def load_team_text(team_name):
    team_file_path = os.path.join(os.path.split(__file__)[0], "{}.txt".format(team_name))
    if os.path.exists(team_file_path):
        with open(file=team_file_path, mode="r", encoding='utf-8') as fin:
            data = fin.read()
        return data

    return "No data for these team: {}".format(team_name)


def load_definite_team(team_name):
    team_file_path = os.path.join(os.path.split(__file__)[0], "{}.txt".format(team_name))
    if os.path.exists(team_file_path):
        with open(file=team_file_path, mode="r", encoding='utf-8') as fin:
            t = yaml.load(fin)['teams'][0]

        return team(t['name'], t['key'], t['task_id'], 
                t['task_sequence'], t['geo_position'] if 'geo_position' in t.keys() else None)

    print("No data for these team: {}".format(team_name))
    return None


def save_team_text_and_reload_this_team(team_name, data):
    team_file_path = os.path.join(os.path.split(__file__)[0], "{}.txt".format(team_name))
    with open(file=team_file_path, mode="w", encoding='utf-8') as fout:
        fout.write(data)
        
    return load_definite_team(team_name)

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


def save_team(team):
    save_teams([team], file_path = os.path.join(os.path.split(__file__)[0], "{}.txt".format(team.name)))


def reset_teams_progress(teams, file_path=teams_file):
    teams = load_teams()
    for team in teams:
        team.task_id = 0

    save_teams(teams)
    

teams = load_teams()


def search_team(key, teams=teams):
    for team in teams:
        if key == team.key:
            return team
    return None

def search_team_index(key, teams=teams):
    for index, team in enumerate(teams):
        if key == team.key:
            return index
    return None