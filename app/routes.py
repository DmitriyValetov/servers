from app import app
from flask import Flask, request, render_template, redirect, url_for, session


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pass
        
    return render_template('index.html')