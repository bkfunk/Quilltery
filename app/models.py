from hashlib import md5
from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    quillts = db.relationship('Quillt', backref = 'author', lazy = 'dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    followed = db.relationship('User', 
            secondary = followers, 
            primaryjoin = (followers.c.follower_id == id), 
            secondaryjoin = (followers.c.followed_id == id), 
            backref = db.backref('followers', lazy = 'dynamic'), 
            lazy = 'dynamic')

    @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname = nickname).first() == None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname = new_nickname).first() == None:
                break
            version += 1
        return new_nickname

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.nickname)
        
    def avatar(self, size):
        return ('http://www.gravatar.com/avatar/' + 
            md5(self.email).hexdigest() + 
            '?d=mm&s=' + str(size))
            
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    """def followed_posts(self):
        return Post.query.join(followers, 
                (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id).order_by(
                Post.timestamp.desc())"""
                
class Quillt(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(280));
    passages = db.relationship('Passage', backref = 'quillt', lazy = 'dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
class Trigger(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    
class Passage(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(280))
    body = db.Column(db.Text)
    quillt_id = db.Column(db.Integer, db.ForeignKey('quillt.id'))
    
class Snippet(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    