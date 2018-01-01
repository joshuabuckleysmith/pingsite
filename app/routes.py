from flask import render_template, flash, redirect, url_for
from app import app
from app import pingfunctions
from app.forms import LoginForm
import os
import threading


def pinger(ip):
    os.system('ping {}'.format(ip))
    
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    print('prevalid')
    print(form.is_submitted())
    if form.is_submitted():
        print('valid')
        store = form.store.data
        pinger(store)
    return render_template('index.html', title='Home', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.store.data, form.remember_me.data))
        th = T(target = pinger, args = form.store.data)
        th.start()
        
        return redirect(url_for('index'))
    
    return render_template('login.html', title='Sign In', form=form)