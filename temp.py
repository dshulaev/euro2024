if request.form['submit_button'] == 'Внести результат':
    form_team1 = request.form['team1']
    form_team2 = request.form['team2']
    form_match_id = request.form['match_id']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('INSERT INTO results VALUES (% s, % s, %s)', form_match_id, form_team1, form_team2)
    player_bets = cursor.fetchone()
    mysql.connection.commit()
