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
    difference = 0
    start_time = datetime.now()
    end_time = datetime(2024, 6, 14, 22, 0, 0)
    difference = end_time - start_time
    if difference:
        msg = 'До чемпионата Европы по футболу осталось: ' + str(difference)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM account WHERE username = % s \
            AND password = % s', (username, password,))
        account = cursor.fetchone()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT ID FROM matchs WHERE date > %s ORDER BY date  ', (start_time,))
        num = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['num'] = num['ID'] - 1
            session['correct_score'] = 3
            session['correct_difference'] = 2
            session['correct_issue'] = 1
            session['correct_champ_winner'] = 5

            if  account['admin'] == 1:
                session['admin'] = True
                session['admin_num'] = num['ID'] - 1
            else:
                session['admin'] = False
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect username / password!'
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
    msg = ''
    if 'loggedin' in session:
        return render_template("index.html",  msg=msg)
    return redirect(url_for('login'))


@app.route("/display")
def display():
    msg = ''
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
    msg = ''
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select SUM(points) from points WHERE player_id = %s GROUP BY player_id', (session['id'],))
        result = cursor.fetchone()
        #points = int(result['SUM(points)'])
        cursor.execute(
            'select  row_number() over (Order by player_id desc), account.username, SUM(points) from points left join account on points.player_id = account.id group by player_id')
        headers = ('№', 'Игрок', 'Очки')
        tableDatalist = []
        tableDatalistFull = []
        tableData = cursor.fetchall()

        for i in tableData:
            tableDatalist.append(i)
        for i in tableDatalist:
            tableDatalistFull.append(tuple(i.values()))
        tableData = tuple(tableDatalistFull)

        return render_template(
            '/points.html',
            headers=headers,
            tableData=tableData
        )
    return redirect(url_for('login'))

@app.route('/my_bets')
def my_bets():
    msg = ''
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
    msg = ''
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
    msg = ''
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
                                       teams1=teams1[session["num"]], teams2=teams2[session["num"]])
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
                                   teams1=teams1[session["num"]], teams2=teams2[session["num"]] )
        else:
            session["num"] = 0
            return render_template("bet.html", msg=msg, match_id = match_id[session["num"]], teams1 = teams1[session["num"]], teams2 = teams2[session["num"]] )


@app.route("/admining", methods=['GET', 'POST'])
def admining():

    msg = ''
    def points_count(match_id):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT match_id, goals1, goals2 FROM results WHERE match_id = %s', (match_id,))
        results = cursor.fetchone()
        cursor.execute('SELECT player_id, match_id, goals1, goals2 FROM bets WHERE match_id = %s', (match_id,))
        bets = cursor.fetchall()
        for i in bets:
            cursor.execute('SELECT player_id FROM points WHERE match_id = %s and player_id = %s', (match_id, i['player_id']))
            check_points = cursor.fetchone()
            if not check_points:
                if i['goals1'] == results['goals1'] and i['goals2'] == results['goals2']:
                    cursor.execute('INSERT into points Values(%s, %s, %s)', (i['player_id'], match_id, session['correct_score']))
                    mysql.connection.commit()
                elif (i['goals1'] - results['goals1']) == (i['goals2'] - results['goals2']):
                    cursor.execute('INSERT into points Values(%s, %s, %s)',
                                   (i['player_id'], match_id, session['correct_difference']))
                    mysql.connection.commit()
                elif ((i['goals1'] > i['goals2']) and (results['goals1'] > results['goals2'])) or ((i['goals1'] < i['goals2']) and (results['goals1'] < results['goals2'])):
                    cursor.execute('INSERT into points Values(%s, %s, %s)',
                                   (i['player_id'], match_id, session['correct_issue']))
                    mysql.connection.commit()
            else:
                if i['goals1'] == results['goals1'] and i['goals2'] == results['goals2']:
                    cursor.execute('Update points set points = %s WHERE player_id = %s and match_id = %s' , (session['correct_score'], i['player_id'], match_id ))
                    mysql.connection.commit()
                elif (i['goals1'] - results['goals1']) == (i['goals2'] - results['goals2']):
                    cursor.execute('Update points set points = %s WHERE player_id = %s and match_id = %s', (session['correct_difference'], i['player_id'], match_id ))
                    mysql.connection.commit()
                elif ((i['goals1'] > i['goals2']) and (results['goals1'] > results['goals2'])) or ((i['goals1'] < i['goals2']) and (results['goals1'] < results['goals2'])):
                    cursor.execute('Update points set points = %s WHERE player_id = %s and match_id = %s', (session['correct_issue'], i['player_id'], match_id ))
                    mysql.connection.commit()
        return bets

    if 'loggedin' in session:
        msg = 'Занесите результат матча: '
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

            if request.form['submit_button'] == 'Внести результат':
                form_team1 = request.form['team1']
                form_team2 = request.form['team2']
                form_match_id = request.form['match_id']
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT match_id FROM results WHERE  match_id = %s ', (form_match_id, ))
                results = cursor.fetchone()
                if results:
                    cursor.execute('UPDATE results SET goals1 = %s, goals2 = %s WHERE match_id = %s',
                                   (form_team1, form_team2, form_match_id))
                    mysql.connection.commit()

                else:
                    cursor.execute('INSERT INTO results VALUES (% s, % s, % s)',(form_match_id, form_team1, form_team2))
                    mysql.connection.commit()
                points_count(form_match_id)


                if session["admin_num"] < len(match_id) - 1:
                    session["admin_num"] += 1
                if session["admin_num"] == len(match_id) - 1:
                    return render_template("admining_last.html", msg=msg, match_id=match_id[session["admin_num"]],
                                           teams1=teams1[session["admin_num"]], teams2=teams2[session["admin_num"]], )
                return render_template("admining.html", msg=msg, match_id=match_id[session["admin_num"]],
                                       teams1=teams1[session["admin_num"]], teams2=teams2[session["admin_num"]])
            elif request.form['submit_button'] == 'Предыдущий матч':
                if session["admin_num"] == 0:
                    msg = "Это первый матч"
                    return render_template("admining.html", msg=msg, match_id=match_id[session["admin_num"]],
                                           teams1=teams1[session["admin_num"]], teams2=teams2[session["admin_num"]])
                session["admin_num"] -= 1
                if session["admin_num"] == 0:
                    return render_template("admining_first.html", msg=msg, match_id=match_id[session["admin_num"]],
                                       teams1=teams1[session["admin_num"]], teams2=teams2[session["admin_num"]])
                else:
                    return render_template("admining.html", msg=msg, match_id=match_id[session["admin_num"]],
                                           teams1=teams1[session["admin_num"]], teams2=teams2[session["admin_num"]])
            elif request.form['submit_button'] == 'Следующий матч':
                session["admin_num"] += 1
                if session["admin_num"] == len(match_id) - 1:
                    return render_template("admining_last.html", msg=msg, match_id=match_id[session["admin_num"]],
                                           teams1=teams1[session["admin_num"]], teams2=teams2[session["admin_num"]], )
                return render_template("admining.html", msg=msg, match_id=match_id[session["admin_num"]],
                                       teams1=teams1[session["admin_num"]], teams2=teams2[session["admin_num"]])

        elif request.method == 'GET':
            if session["admin_num"] == 0:
                return render_template("admining_first.html", msg=msg, match_id=match_id[session["admin_num"]],
                                       teams1=teams1[session["admin_num"]], teams2=teams2[session["admin_num"]])
            else:
                return render_template("admining.html", msg=msg, match_id=match_id[session["admin_num"]],
                                       teams1=teams1[session["admin_num"]], teams2=teams2[session["admin_num"]])


    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host="localhost", port=int("5000"), debug=True, use_reloader=False)
