import os
import requests
from flask import Flask, session, render_template, request, redirect, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker




app = Flask(__name__)

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
    add='%'
    return add+palabra+add
def integr( palabra):
    add=' '
    return add+palabra+add
# def confirma( palabra):
#     if palabra is None:
#         return "u"
#     return palabra

@app.route("/",methods=["GET","POST"])
def index():

    # if session.get("reader") is None:
    #     session["reader"] = []
    #     session["contrasena"] = ""
    #     session["session"] = "si"
    #     return  render_template("trueLogin.html")

    if request.method == "POST":
        session["session"]=request.form.get("session")
    # salir de la sesion
        if session["session"] == "no" :
            print("if2-1")
            session.clear()
            session["reader"] = []
            session["psw1"] = ""
            session["psw2"] = ""
            session["session"] = "si"
            return  render_template("trueLogin.html")
    # submit login or register
        else:
            session["reader"] = request.form.get("reader")
            session["register"] = request.form.get("register")
            session["psw1"] = request.form.get("psw1")
    # check if user is in users  db.execute("""SELECT * FROM "users" WHERE "user" = :user""", {"user":session["reader"] }).fetchone()
            print(db.execute("""SELECT * FROM "readers_id" WHERE "reader_id" = :reader_id""", {"reader_id":session["reader"] }).fetchone())
            if session["register"]=="0":
                if session["reader"]in Users:
                    if Passwords[Users.index(session["reader"])]==session["psw1"]:
                        print("user and pass correct")
                        # return redirect(url_for('searchPage'))
                return render_template("error.html")
    # check if passwords correct
            session["psw2"] = request.form.get("psw2")
            if not session["psw2"]==session["psw1"]:
                return render_template("error.html")
    # if no problem add user
            else:
                Users.append(session["reader"])
                Passwords.append(session["psw1"])
                # return redirect(url_for('searchPage'))

            # db.execute("""INSERT INTO "users" ("user","password") VALUES  (:reader , :psw1) """, {"reader":session["reader"],"psw1":session["psw1"]})
            # db.commit()

        # return  render_template("trueLogin.html")
    return  render_template("trueLogin.html")


# ["""SELECT "sbnNumber","title","author", "pubYear" FROM "books" WHERE "title" LIKE :tito AND "pubYear" LIKE :yer AND "author" LIKE :crea AND "sbnNumber" LIKE :num""",{"tito":integra(session["title"]),"yer":integra(session["pubYear"]),"crea":integra(session["author"]),"num":integra(session["sbnNumber"])}]
#     # -------------------------------------------
#     if session.get("reader") is None:
#         session["reader"] = []
#         session["contrasena"] = ""
#         session["session"] = "si"
#     # book = Book(sbnNumber=sbnNumber, title=title, author=author, pubYear=pubYear)
#     # db.session.add(book)
#     if request.method == "POST":
#         session["session"]=request.form.get("session")
#         if session["session"] == "no" :
#             session.clear()
#             session["reader"] = []
#             clienteFijo=""
#             session["psw"] = ""
#             session["session"] = "si"
#             return  render_template("trueLogin.html")
#         else:
#             session["reader"] = request.form.get("reader")
#             session["psw"] = request.form.get("psw")
#             db.execute("""INSERT INTO "users" ("user","password") VALUES  (:reader , :psw) """, {"reader":session["reader"],"psw":session["psw"]})
#             db.commit()

#         # return  render_template("trueLogin.html")

#     return  render_template("trueLogin.html")
# @app.route("/searchPage", methods=["GET","POST"])
# def searchPage():
#     if request.method == "POST":
#         session["password"]=request.form.get("psw")
#         session["reader"]=request.form.get("reader")
#     else:
#         if session["reader"] is None:

#     session["cliente"] = db.execute("""SELECT * FROM "users" WHERE "user" = :user""", {"user":session["reader"] }).fetchone()
#     if session.get("cliente") is None:
#             return  render_template("trueLogin.html")
#     if session["cliente"].password != session["password"]:
#                 return  render_template("trueLogin.html")
#     if session.get("books") is None:
#         session["title"]=""
#         session["pubYear"]=""
#         session["author"]=""
#         session["sbnNumber"]=""
#         session["books"]=""#db.execute("""SELECT "sbnNumber","title","author", "pubYear" FROM "books" WHERE "title" LIKE :tito AND "pubYear" LIKE :yer AND "author" LIKE :crea AND "sbnNumber" LIKE :num""",




#     session["title"]=request.form.get("title")
#     session["pubYear"]=request.form.get("pubYear")
#     session["author"]=request.form.get("author")
#     session["sbnNumber"]=request.form.get("sbnNumber")
#     comando=["""SELECT "sbnNumber","title","author", "pubYear" FROM "books" WHERE "title" LIKE :tito AND "pubYear" LIKE :yer AND "author" LIKE :crea AND "sbnNumber" LIKE :num""",{"tito":integra(session["title"]),"yer":integra(session["pubYear"]),"crea":integra(session["author"]),"num":integra(session["sbnNumber"])}]
#     print(comando)
#     session["books"]=db.execute("""SELECT "sbnNumber","title","author", "pubYear" FROM "books" WHERE "title" LIKE :tito AND "pubYear" LIKE :yer AND "author" LIKE :crea AND "sbnNumber" LIKE :num""",{"tito":integra(session["title"]),"yer":integra(session["pubYear"]),"crea":integra(session["author"]),"num":integra(session["sbnNumber"])}).fetchall()

#     return render_template("searchPage.html",bks=session["books"],
#     lol=session["sbnNumber"],
#     psw=session["password"],
#     reader=session["reader"])
#     #,mensaje=" busqueda exitosa")

# @app.route("/searchPage/<Source>", methods=["GET","POST"] )
# def bookdata(Source):
#     # session["reader"]=request.form.get("reader")
#     print(session["reader"])
#     session["review"]=request.form.get("review")
#     session["rate"]=request.form.get("rate")
#     session["databook"]=db.execute("""SELECT * FROM "books" WHERE "sbnNumber" = :Source""",{"Source":Source}).fetchone()
#     session["datareview"] = db.execute("""SELECT * FROM "reviews" WHERE "sbnNumber" = :Sour""",{"Sour":Source}).fetchall()    
#     session["comentar"]=not(session["review"] is None)
#     print(session["comentar"],session["review"])
#     if session["databook"] is None:
#         return  render_template("error.html",mensaje="no disponemos de este libro"),404


#     if session["comentar"]:
#         for i in session["datareview"]:
#             if i[1]==session["reader"]:
#                 session["comentar"]=False

#     # session["oneComment"] = db.execute("""SELECT "user" FROM "reviews" WHERE "sbnNumber" = :Sour AND "user" = :nombre """,{"Sour":Source, "nombre":session["reader"]}).fetchall()
#     # print("------------------------\n",session["datareview"],"\n",session["oneComment"],"\n------------------------\n")
#     # if (session["review"] is None) and (session["comentar"]):
#     #     print("-----------\n",session["datareview"],"\n",session["oneComment"],"\n--------")
#         # if session["datareview"] is None:
#         #     return  render_template("review.html",book=session["databook"],reader=session["reader"],oneComment=True)
#         # return  render_template("review.html",book=session["databook"],reviews=session["datareview"],rates=[1,2,3,4,5],sbnN=Source,reader=session["reader"],oneComment=(session["reader"]!=session["oneComment"][0]["user"]))

#     try:
#         db.execute("""INSERT INTO "reviews" ("user","sbnNumber","comentario","rate") VALUES  (:reader , :source,:review,:rate) """,{"reader":session["reader"],"source":Source,"review":session["review"],"rate":session["rate"]})
#     except :
#         print("error")
#         return  render_template("review.html",book=session["databook"],reviews=session["datareview"],reader=session["reader"],oneComment=session["comentar"])
#         # return  render_template("error.html",mensaje="no puede realizar otro comentario"),404
#     db.commit()
#     # session["datareview"] = db.execute("""SELECT * FROM "reviews" WHERE "sbnNumber" = :Sour""", {"Sour":Source }).fetchall()
#     print("-----------\n",session["datareview"],"\n",session["comentar"],"--------\n")
#     return  render_template("review.html",book=session["databook"],reviews=session["datareview"],reader=session["reader"],oneComment=session["comentar"])

# @app.route("/api/searchPage/<Source>" )
# def bookAPI(Source):

#     session["datareview"]=""
#     session["databook"]=db.execute("""SELECT * FROM "books" WHERE "sbnNumber" = :Source""",{"Source":Source}).fetchone()
#     if session["databook"] is None:
#         return jsonify({"error":"invalid requested book "}),404
#     session["res"] = requests.get("https://www.goodreads.com/book/review_counts.json",params={"key": "XpBeTod1UwDEF989WE4g", "isbns": Source})
#     session["data"]=session["res"].json()

#     return jsonify({
#     "title": session["databook"].title,
#     "author": session["databook"].author,
#     "year": int(session["databook"].pubYear),
#     "isbn": session["databook"].sbnNumber,
#     "review_count":session["data"]["books"][0]["work_ratings_count"],
#     "average_score":session["data"]["books"][0]["average_rating"]
#     })
