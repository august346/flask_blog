import datetime

from myapp import db


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))

    def get_json(self):
        return {
            0: self.id,
            1: self.name
        }


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    text = db.Column(db.TEXT())
    description = db.Column(db.TEXT())
    picture = db.Column(db.String())
    tags = db.Column(db.String())
    pub_date = db.Column(db.DateTime, nullable=False,
                         default=datetime.datetime.utcnow)

    def get_json(self):
        return {
            0: self.id,
            1: self.title
        }


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    articles = db.Column(db.Integer(), default=1)

    def get_json(self):
        return {0: self.id, 1: self.name}