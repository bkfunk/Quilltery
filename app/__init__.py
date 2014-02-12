from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
import os
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from flask.ext.admin import Admin
from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
from flask_misaka import Misaka
from app.renderers import QuilltRenderer

app = Flask(__name__)
app.config.from_object('config')
Bootstrap(app)
db = SQLAlchemy(app)
m = Misaka(app, QuilltRenderer())
print(m.render("This is a test (r) [[test]]"))


#lm = LoginManager()
#lm.init_app(app)
#lm.login_view = 'login'
#oid = OpenID(app, os.path.join(basedir, 'tmp'))

if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT), 
                'no-reply@' + MAIL_SERVER, ADMINS, 
                'microblog failure', credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)
    
if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/microblog.log', 
                                        'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('microblog startup')

from app import views, models

admin = Admin(app, name = "AppAdmin")
#admin.add_view(views.AdminView(models.Post, db.session))


# Testing

if not models.User.query.all():
    u = models.User(nickname='john', email='john@example.com', role=models.ROLE_USER)
    db.session.add(u)
    db.session.commit()
    
if not models.Quillt.query.all():
    q1 = models.Quillt(title='Quillt 1', user_id = models.User.query.first().id)
    q2 = models.Quillt(title='Quillt 2', user_id = models.User.query.first().id)
    db.session.add(q1)
    db.session.add(q2)
    db.session.commit()

text = """# The Beginning #
It began in the beginning. In the _beginnning_. It was the beginning when it began.

I suppose I'll start where it starts, at the end. The end is always where it starts of course. Even the end starts at the end. The question is, where does the end _end_?

He told me, ``Hello, son.''

``What?'' I said. I was pretty dumb about these things.

[[Go to the store]]
[[Leave town]]
[[also]]
[A custom link](thisisacustomlink.com "TITLE CUSTOM")
"""

if not models.Passage.query.all():
    p1 = models.Passage(title='A great passage',
        body=text, quillt_id = models.Quillt.query.get(1).id)
    db.session.add(p1)
    db.session.commit()


