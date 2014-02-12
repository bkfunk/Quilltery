from flask import render_template, render_template_string, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, m #, lm, oid
from app import models

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
    #return render_template_string(template)
    passage = models.Passage.query.first().body
    print("This is the passage:\n" + passage)
    passage_md = m.render(passage)
    print("This is the passage marked up:\n" + passage_md)
    return render_template('index.html', passage = passage_md)

@app.route('/q/<q_id>')
@app.route('/q/<q_id>/<p_id>')
def show_node(q_id, p_id = None):
    quillt = models.Quillt.query.filter_by(id = q_id)
    if not p_id:
        passage = models.Passage.query.filter_by(quillt_id = q_id).first()
    else:
        passage = models.Passage.query.filter_by(quillt_id = q_id, id = p_id).first()
    return render_template('quillt.html', quillt = quillt, passage = passage)

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