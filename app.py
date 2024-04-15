from flask import Flask, render_template, request, redirect, url_for, session, g
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from datetime import date, datetime


app = Flask(__name__)

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'geekprofile'

mysql = MySQL(app)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM account WHERE username = % s \
            AND password = % s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['num'] = 0
            if  account['admin'] == 1:
                session['admin'] = True
            else:
                session['admin'] = False
            msg = 'Logged in successfully !'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM account WHERE username = % s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Такой пользователь уже есть!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Недопустимый email!'
#        elif not re.match(r'[A-Za-z0-9]+', username):
#            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO account VALUES \
                (NULL, % s, % s, % s)', (username, password, email))
            mysql.connection.commit()
            msg = 'Вы успешно зарегистрировались!'

    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)


@app.route("/index")
def index():
    if 'loggedin' in session:
        return render_template("index.html")
    return redirect(url_for('login'))


@app.route("/display")
def display():
    if 'loggedin' in session:
        if session['admin'] == True:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM account WHERE id = % s', (session['id'],))
            account = cursor.fetchone()
            return render_template("display_admin.html", account=account)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM account WHERE id = % s', (session['id'],))
        account = cursor.fetchone()
        return render_template("display.html", account=account)
    return redirect(url_for('login'))


@app.route("/update", methods=['GET', 'POST'])
def update():
    msg = ''
    if 'loggedin' in session:
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM account WHERE username = % s',(username,))
            account = cursor.fetchone()
            if account:
                msg = 'Такой пользователь уже есть!'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Недопустимый email!'
#            elif not re.match(r'[A-Za-z0-9]+', username):
#               msg = 'name must contain only characters and numbers !'
            else:
                cursor.execute('UPDATE account SET username =% s,\
                password =% s, email =% s WHERE id =% s', (username, password, email, (session['id'],),))
                mysql.connection.commit()
                msg = 'Данные успешно обновлены!!'
        elif request.method == 'POST':
            msg = 'Please fill out the form !'
        return render_template("update.html", msg=msg)
    return redirect(url_for('login'))

@app.route("/points")
def points():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM points WHERE Player_id = % s', (session['id'],))
        points = cursor.fetchone()
        return render_template("points.html", points=points)
    return redirect(url_for('login'))

@app.route('/my_bets')
def my_bets():
    current_day = date.today()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT matchs.ID, matchs.date, matchs.team1, matchs.team2, bets.goals1, bets.goals2 from matchs LEFT JOIN bets ON matchs.ID = bets.match_id WHERE bets.player_id = % s ORDER BY matchs.ID', (session['id'],))

    headers = ('№','Дата', 'Команда 1', 'Команда 2', 'Ставка 1 команда', 'Ставка 2 команда')
    tableDatalist = []
    tableDatalistFull = []
    tableData = cursor.fetchall()

    for i in tableData:
        tableDatalist.append(i)
    for i in tableDatalist:
        tableDatalistFull.append(tuple(i.values()))
    tableData = tuple(tableDatalistFull)

    return render_template(
        '/my_bets.html',
        headers=headers,
        tableData=tableData
    )

@app.route('/matchs')
def matchs():
    current_day = date.today()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * from matchs')

    headers = ('№','Дата', 'Команда 1', 'Команда 2')
    tableDatalist = []
    tableDatalistFull = []
    tableData = cursor.fetchall()

    for i in tableData:
        tableDatalist.append(i)
    for i in tableDatalist:
        tableDatalistFull.append(tuple(i.values()))
    tableData = tuple(tableDatalistFull)

    return render_template(
        '/matchs.html',
        headers=headers,
        tableData=tableData
    )

@app.route("/bet", methods=['GET', 'POST'])
def bet():
    def get_my_bet ():
        msg = ''
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT goals1, goals2 FROM bets WHERE player_id = %s and match_id = %s ',
                       (session['id'], (session["num"]+1)))
        result = cursor.fetchone()
        if result:
            score1 = str(result['goals1'])
            score2 = str(result['goals2'])
            msg += "Ваша текущая ставка " + score1 + ':' + score2
        return msg


    matchs = []
    teams1 = []
    teams2 = []
    match_id = []
    my_bet = []
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT ID, team1, team2 FROM matchs')
    matchs_cur = cursor.fetchall()
    dictionaries = []

    for i in matchs_cur:
        dictionaries.append(i)
    for i in dictionaries:
        matchs.append(list(i.values()))
    for i in matchs:
        teams1.append(i[1])
    for i in matchs:
        teams2.append(i[2])
    for i in matchs:
        match_id.append(i[0])

    if request.method == 'POST':

        if request.form['submit_button'] == 'Сделать ставку!':
            form_team1 = request.form['team1']
            form_team2 = request.form['team2']
            form_match_id = request.form['match_id']
            msg = get_my_bet()
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT match_id FROM bets WHERE player_id = %s and match_id = %s ', (session['id'], form_match_id))
            player_bets = cursor.fetchone()
            if player_bets:
                cursor.execute('UPDATE bets SET goals1 = %s, goals2 = %s WHERE player_id = %s and match_id = %s', (form_team1, form_team2, session['id'], form_match_id))
                mysql.connection.commit()

            else:
                cursor.execute('INSERT INTO bets VALUES (% s, % s, %s, % s)', (session['id'], form_match_id, form_team1, form_team2))
                mysql.connection.commit()

            session["num"] += 1
            msg = get_my_bet()
            if session["num"] == len(match_id) - 1:
                return render_template("bet_last.html", msg=msg, match_id=match_id[session["num"]],
                                       teams1=teams1[session["num"]], teams2=teams2[session["num"]], )
            return render_template("bet.html", msg=msg, match_id=match_id[session["num"]], teams1=teams1[session["num"]], teams2=teams2[session["num"]])
        elif request.form['submit_button'] == 'Предыдущий матч':
            if session["num"] == 0:
                msg = "Это первый матч"
                return render_template("bet.html", msg=msg, match_id=match_id[session["num"]],
                                       teams1=teams1[session["num"]], teams2=teams2[session["num"]])
            session["num"] -= 1
            msg = get_my_bet()
            return render_template("bet.html", msg=msg, match_id=match_id[session["num"]],
                                   teams1=teams1[session["num"]], teams2=teams2[session["num"]])
        elif request.form['submit_button'] == 'Следующий матч':
            session["num"] += 1
            msg = get_my_bet()
            if session["num"] == len(match_id) - 1:
                return render_template("bet_last.html", msg=msg, match_id=match_id[session["num"]],
                                       teams1=teams1[session["num"]], teams2=teams2[session["num"]], )
            return render_template("bet.html", msg=msg, match_id=match_id[session["num"]],
                                   teams1=teams1[session["num"]], teams2=teams2[session["num"]])
    elif request.method == 'GET':
        msg = get_my_bet()
        if session["num"] == 0:
            return render_template("bet_first.html", msg=msg, match_id=match_id[session["num"]],
                                   teams1=teams1[session["num"]], teams2=teams2[session["num"]], )
        else:
            return render_template("bet.html", msg=msg, match_id = match_id[session["num"]], teams1 = teams1[session["num"]], teams2 = teams2[session["num"]], )


@app.route("/admining")
def admining():
    if 'loggedin' in session:
        msg = 'Ты лучший'
        matchs = []
        teams1 = []
        teams2 = []
        match_id = []
        my_bet = []
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT ID, team1, team2 FROM matchs')
        matchs_cur = cursor.fetchall()
        dictionaries = []

        for i in matchs_cur:
            dictionaries.append(i)
        for i in dictionaries:
            matchs.append(list(i.values()))
        for i in matchs:
            teams1.append(i[1])
        for i in matchs:
            teams2.append(i[2])
        for i in matchs:
            match_id.append(i[0])

        if request.method == 'POST':

            if request.form['submit_button'] == 'Сделать ставку!':
                form_team1 = request.form['team1']
                form_team2 = request.form['team2']
                form_match_id = request.form['match_id']
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT match_id FROM bets WHERE player_id = %s and match_id = %s ',
                               (session['id'], form_match_id))
                player_bets = cursor.fetchone()
                if player_bets:
                    cursor.execute('UPDATE bets SET goals1 = %s, goals2 = %s WHERE player_id = %s and match_id = %s',
                                   (form_team1, form_team2, session['id'], form_match_id))
                    mysql.connection.commit()

                else:
                    cursor.execute('INSERT INTO bets VALUES (% s, % s, %s, % s)',
                                   (session['id'], form_match_id, form_team1, form_team2))
                    mysql.connection.commit()

                session["num"] += 1
                if session["num"] == len(match_id) - 1:
                    return render_template("bet_last.html", msg=msg, match_id=match_id[session["num"]],
                                           teams1=teams1[session["num"]], teams2=teams2[session["num"]], )
                return render_template("bet.html", msg=msg, match_id=match_id[session["num"]],
                                       teams1=teams1[session["num"]], teams2=teams2[session["num"]])
            elif request.form['submit_button'] == 'Предыдущий матч':
                if session["num"] == 0:
                    msg = "Это первый матч"
                    return render_template("bet.html", msg=msg, match_id=match_id[session["num"]],
                                           teams1=teams1[session["num"]], teams2=teams2[session["num"]])
                session["num"] -= 1
                return render_template("bet.html", msg=msg, match_id=match_id[session["num"]],
                                       teams1=teams1[session["num"]], teams2=teams2[session["num"]])
            elif request.form['submit_button'] == 'Следующий матч':
                session["num"] += 1
                if session["num"] == len(match_id) - 1:
                    return render_template("bet_last.html", msg=msg, match_id=match_id[session["num"]],
                                           teams1=teams1[session["num"]], teams2=teams2[session["num"]], )
                return render_template("bet.html", msg=msg, match_id=match_id[session["num"]],
                                       teams1=teams1[session["num"]], teams2=teams2[session["num"]])
        elif request.method == 'GET':
            if session["num"] == 0:
                return render_template("bet_first.html", msg=msg, match_id=match_id[session["num"]],
                                       teams1=teams1[session["num"]], teams2=teams2[session["num"]], )
            else:
                return render_template("bet.html", msg=msg, match_id=match_id[session["num"]],
                                       teams1=teams1[session["num"]], teams2=teams2[session["num"]], )


return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=int("5000"))