import yaml
import os

class task:
    def __init__(self, tip, text, answer):
        self.tip = tip
        self.text = text
        self.answer = answer
    def __repr__(self):
        return "tip: {}\n text:{}\n answer:{}\n".format(self.tip, self.text, self.answer)


def load_tasks(file_path):
    with open(file=file_path, mode="r", encoding="utf-8") as fin:
        data = yaml.load(fin)
    if "tasks" not in data.keys() or len(data["tasks"])==0:
        raise BaseException("There are no tasks in src data!") 
    
    tasks = []   
    for t in data["tasks"]:
         tasks.append(task(t['tip'], t['text'], t['answer']))

    return tasks


tasks_file = os.path.join(os.path.split(__file__)[0], "tasks.txt")
tasks = load_tasks(tasks_file)
