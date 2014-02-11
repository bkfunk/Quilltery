from flask import render_template, render_template_string, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db #, lm, oid
# Index/Main page
@app.route('/')
@app.route('/index')
def index():
    #return render_template('index.html')
    template = """
    {% extends "base.html" %}
    {% block content %}
    {% endblock %}
    """
    return render_template_string(template)

@app.route('/<quillt>/<node>')
def show_node(quillt, node):
    return render_template('quillt.html', quillt = quillt, node = node)

# Login page
#@app.route('/login', methods = ['GET', 'POST'])
#@oid.loginhandler
"""def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
    return render_template('login.html', 
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])
"""