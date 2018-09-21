from flask import Flask

app = Flask(__name__)
app.config["SECRET_KEY"] = "2501"
core = dict()


from app import routes
