from flask import Flask, request
import pymysql.cursors
import flask_login

class Database():
    def __init__(self):
        self.con = pymysql.connect(host='izba.ovh',
                                        user='kortti',
                                        password='peli321',
                                        db='KorttiPeli')


app = Flask(__name__)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
db = Database()
app.secret_key = 'super secret key'


class user(flask_login.UserMixin):
        def __init__(self, id):
                super().__init__()
                self.id = str(id)
        def get_id(self):
                return self.id

global userList
userList = list()

global ID
ID = 1

def rSql(argument):
    switcher = {
        "Pari": ["SELECT Parit FROM Yht", "UPDATE Yht SET Parit = %s"],
        "2Paria": ["Select 2Paria FROM Yht", "UPDATE Yht SET 2Paria = %s"],
        "3Samaa": ["SELECT 3Samaa FROM Yht","UPDATE Yht SET 3Samaa = %s"],
        "4Samaa": ["SELECT 4Samaa FROM Yht","UPDATE Yht SET 4Samaa = %s"],
        "5Samaa": ["SELECT 5Samaa FROM Yht","UPDATE Yht SET 5Samaa = %s"],
        "Vari": ["SELECT Vari FROM Yht","UPDATE Yht SET Vari = %s"],
        "Suora": ["SELECT Suora FROM Yht","UPDATE Yht SET Suora = %s"],
        "Tays": ["SELECT Tays FROM Yht","UPDATE Yht SET Tays = %s"],
        "Varisuora": ["SELECT Varisuora FROM Yht","UPDATE Yht SET Varisuora = %s"],
        "Kuningasvarisuora": ["SELECT Kuningasvarisuora FROM Yht","UPDATE Yht SET Kuningasvarisuora = %s"]
    }
    return switcher.get(argument, "Nothing")



@app.route("/korttipeli/getScores", methods=["GET"])
@flask_login.login_required
def getScores():
        while True:
                try:
                    with db.con.cursor() as cursor:
                        sql = "SELECT username, tulos FROM Highscore ORDER BY tulos DESC limit 10"
                        cursor.execute(sql)
                        result = cursor.fetchall()
                        print(result)
                        break
                except:
                        db = Database()
        return str(result)

@app.route("/korttipeli/getOsumat", methods=["GET"])
@flask_login.login_required
def getOsumat():
    while True:
        try:
            with db.con.cursor() as cursor:
                sql = "SELECT * FROM Yht"
                cursor.execute(sql)
                result = cursor.fetchone()
                print(result)
                break
        except:
            db = Database()
    return str(result)

@app.route("/korttipeli/addOsuma", methods=["POST"])
@flask_login.login_required
def addOsuma():
        while True:
         try:
                with db.con.cursor() as cursor:
                        osuma = request.form["Osuma"]
                        print(osuma)
                        sql = rSql(str(osuma))
                        cursor.execute(sql[0])
                        result = cursor.fetchone()[0]
                        r= int(result) + 1
                        cursor.execute(sql[1], r)
                        db.con.commit()
                        break
         except:
            db = Database()
        return "Osuma lisätty"

@login_manager.user_loader
def load_user(user_id):
        print("inside userloader")
        for x in range(0, len(userList)):
                if(userList[x].get_id() == user_id):
                        return userList[x]


@app.route("/korttipeli/addScore", methods=["POST"])
@flask_login.login_required
def addScore():
 while True:
    try:
        with db.con.cursor() as cursor:
            username = request.form["username"]
            score = request.form["score"]
            print(username)
            print(score)
            print()
            sql = "INSERT INTO Highscore(username, tulos) VALUES(%s, %s)"
            cursor.execute(sql, (username, score))
            print("before commit")
            db.con.commit()
            print("after commit")
            break
    except:
        db = Database()

 return "Tulos lisätty"

@app.route("/korttipeli/login", methods=["POST"])
def login():
        username = request.form["username"]
        password = request.form["password"]
        print(username)
        print(password)
        if(str(username) == "PeliUser"):
                if(str(password) == "PeliMysteeriSalasana132"):
                        global ID
                        global userList
                        u = user(ID)
                        userList.append(u)
                        flask_login.login_user(u)
                        ID = ID + 1
                        return "logged in"

if __name__ == "__main__":
        app.run(host="0.0.0.0", port="5000")