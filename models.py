from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Idea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idea = db.Column(db.String(100), nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))    #связь один ко многим

    def __repr__(self):
        return f"<User {self.idea}>"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    ideas = db.relationship('Idea', backref='user', lazy=True)


    def __repr__(self):
        return f"<User {self.first_name}>"