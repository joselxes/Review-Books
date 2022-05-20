import os
import requests
from flask import Flask, session, render_template, request, redirect, jsonify, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *


app = Flask(__name__)
app.secret_key="hello"
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
engine = create_engine(os.getenv("DATABASE_URL"))
# Set up database
db = scoped_session(sessionmaker(bind=engine))
def integra( palabra):
    if palabra is None:
        return ''    
    return '%'+palabra+'%'

def integr( palabra):
    add=' '
    return add+palabra+add


def fComment(LReviews,RReview):
    print(RReview)
    for i in LReviews:
        print(i,)
        if i[1]==RReview:
            return False
    return True

@app.route("/",methods=["GET","POST"])
def index():
    if not("mensaje" in session) :
        session["mensaje"]="Bienvenido"
    if "reader" in session:
        if request.method == "POST":
            session["session"] = request.form.get("session")
            if session["session"] == "no":
                session.pop('reader',None)
                session["mensaje"]="ingresa o registrate"            
                session["mensaje"]="session cerrada"
        else:
            return redirect(url_for('searchPage'))

    # else:0

    return  render_template("trueLogin.html",mensaje=session["mensaje"])

@app.route("/checklog",methods=["GET","POST"])
def checklog():

    if request.method == "POST":
    # submit login or register
        session["reader"] = request.form.get("reader")
        session["register"] = request.form.get("register")
        session["psw1"] = request.form.get("psw1")

    # check if user is in users 
        print(db.execute("""SELECT * FROM "readers_id" """).fetchall())
        session["exists"]=db.execute("""SELECT * FROM "readers_id" WHERE "reader_id" = :reader""", {"reader":session["reader"] }).fetchone()
        print(session["exists"],session["register"])
        print(111111,session["register"],11111)
        if (session["exists"] is None) and session["register"]=="0":
            print("puta mierda", session["reader"] )
            session.pop('reader',None)
            session["mensaje"]="usuario no existe"
            return redirect(url_for('index'))
        # print(session["exists"],"xxxxxxxx",session["exists"][0],session["exists"][0]==session["reader"])

        elif session["register"]=="0":
            if session["exists"]==(session["reader"],session["psw1"]):
                print("user and pass correct")
                return redirect(url_for('searchPage'))
            else:
                session.pop('reader',None)
                session["mensaje"]="contrasena o usuario, incorrecto"   
                return redirect(url_for('index'))

    # check if passwords correct 
        session["psw2"] = request.form.get("psw2")
        if session["psw2"]==session["psw1"]:
            print("register user")
            print(session["exists"],4444444444)
    # check if user exists
            try:
                addi=Reader(reader_id=session["reader"], password=session["psw1"])
                db.add(addi)
                db.commit()            
            except:
                print("except")
                return redirect(url_for('index'))
            return redirect(url_for('searchPage'))

    # if no problem add user
        else:
            session["mensaje"]="contrasenas no coinciden"
            return redirect(url_for('index'))
    else: 
        return redirect(url_for('index'))

@app.route("/searchPage",methods=["GET","POST"])
def searchPage():
    # try:
        if session["reader"] is None:
            print("kk")
            return redirect(url_for('index'))
        # print(session["sbnNumber"],session["title"],session["author"],session["pubYear"])
        session["sbnNumber"]=integra(request.form.get("sbnNumber"))
        session["title"]=integra(request.form.get("title"))
        session["author"]=integra(request.form.get("author"))
        session["pubYear"]=integra(request.form.get("pubYear"))
        print(session["sbnNumber"],session["title"],session["author"],session["pubYear"])
        try:
            session["books"]=db.execute("""SELECT "sbnNumber","title","author", "pubYear" FROM "books" WHERE "title" LIKE :titulo AND "pubYear" LIKE :year AND "author" LIKE :creador AND "sbnNumber" LIKE :num""",{"titulo":session["title"],"year":session["pubYear"],"creador":session["author"],"num":session["sbnNumber"]}).fetchall()
        except:
            session.pop('reader',None)
            session["mensaje"]=" User'Id not available"
            return redirect(url_for('index'))
        print(session["books"]),"/////////////////////"


        return  render_template("searchPage.html",name=session["reader"],books=session["books"])
    # except:
    #     session["mensaje"]="ingresa primero"
    #     return redirect(url_for('index'))


    # return render_template("searchPage.html",bks=session["books"],
    # ,mensaje=" busqueda exitosa")


@app.route("/searchPage/<Source>", methods=["GET","POST"] )
def bookdata(Source):
    session["databook"]=db.execute("""SELECT * FROM "books" WHERE "sbnNumber" = :Source""",{"Source":Source}).fetchone()
    session["datareview"] = db.execute("""SELECT * FROM "reviews" WHERE "sbnNumber" = :Sour""",{"Sour":Source}).fetchall()
    session["comentar"]=fComment(session["datareview"],session["reader"])
    session["sbnNumber"]=Source
    # print(session["reader"])
    print(session["comentar"])

    return  render_template("review.html",book=session["databook"],reviews=session["datareview"],reader=session["reader"],oneComment=session["comentar"])


@app.route("/checkComment",methods=["GET","POST"])
def checkComment():
    if request.method == "POST":
        # try:
            session["comentario"]=request.form.get("comentario")
            session["rate"]=request.form.get("rate")
            print("888888888888888888",session["reader"],session["sbnNumber"],session["comentario"],session["rate"])
            addi=Review(sbnNumber=session["sbnNumber"],reader_id=session["reader"], comentario=session["comentario"],rate=session["rate"])
            db.add(addi)
            db.commit()            
            return redirect(url_for('.bookdata',Source=session["sbnNumber"]))
    #     except:
    #         print("error")
    # return render_template("error.html")+

# @app.route("/endSession",methods=["GET","POST"])
# def endSession():

#     if request.method == "POST":
#         # print("cerrar Session-----",session["reader"])
#         session.clear()
#         print("Session cerrarda -----\n")
#         # return  render_template("trueLogin.html",mensaje="mensaje")
#         return redirect(url_for('/'))
#     else:
#         return redirect(url_for('searchPage'))


# NO HAY API DE GOODREADERS QUE KK AHI QUEDA
@app.route("/api/searchPage/<Source>" )
def bookAPI(Source):

    session["datareview"]=""
    session["databook"]=db.execute("""SELECT * FROM "books" WHERE "sbnNumber" = :Source""",{"Source":Source}).fetchone()
    print(session["databook"])
    if session["databook"] is None:
        return jsonify({"error":"invalid requested book "}),404
    session["res"] = requests.get("https://www.goodreads.com/book/review_counts.json",params={"key": "XpBeTod1UwDEF989WE4g", "isbns": Source})
    print(type(session["res"]),"----------")


    return session["res"]
    return jsonify({
    "title": session["databook"].title,
    "author": session["databook"].author,
    "year": int(session["databook"].pubYear),
    "isbn": session["databook"].sbnNumber,
    "review_count":session["data"]["books"][0]["work_ratings_count"],
    "average_score":session["data"]["books"][0]["average_rating"]
    })



