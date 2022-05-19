from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Reader(db.Model):
    __tablename__= "readers_id"
    reader_id = db.Column(db.String, primary_key=True)
    password =db.Column(db.String, nullable=False)
    def __init__(self,reader_id,password):
        self.reader_id = reader_id
        self.password = password

# sbnNumber,title,author,year
class Book(db.Model):
    __tablename__= "books"
    sbnNumber = db.Column(db.String, primary_key = True)
    title = db.Column(db.String, nullable = False)
    author = db.Column(db.String, nullable = False)
    pubYear = db.Column(db.String, nullable = False)
    bookCounter = 0
    def __init__(self,sbnNumber,title,author,pubYear):
        self.sbnNumber =sbnNumber
        self.title = title
        self.author = author
        self.pubYear =pubYear
        self.bookCounter= 0


class Review(db.Model):
    __tablename__= "reviews"
    sbnNumber = db.Column(db.String,db.ForeignKey("books.sbnNumber"), primary_key=True)
    reader_id = db.Column(db.String, db.ForeignKey("readers_id.reader_id"), primary_key=True)
    comentario= db.Column(db.String)
    rate= db.Column(db.String)
    def __init__(self,sbnNumber,reader_id,comentario,rate):
        self.sbnNumber =sbnNumber
        self.reader_id = reader_id
        self.comentario = comentario
        self.rate=rate
        
        
