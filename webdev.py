from flask import Flask, request, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'user'
app.config['MYSQL_PASSWORD'] = 'pass'
app.config['MYSQL_DB'] = 'webdevb'
app.config['MYSQL_PORT'] = 3306
mysql = MySQL(app)

with app.app_context():
    cur = mysql.connection.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS score (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50),
            question1 VARCHAR(50),
            question2 VARCHAR(50),
            question3 VARCHAR(50)
        )
    ''')
    mysql.connection.commit()
    cur.close()

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/questionary')
def questionary():
    return render_template('questionary.html')

@app.route('/save', methods=['POST'])
def save():
    username = request.form['username']
    question1 = request.form['question1']
    question2 = request.form['question2']
    question3 = request.form['question3']
    if not username:
        error = 'ERROR - The username is mandatory!'
        return render_template('error.html', error=error)
    else:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO score (username, question1, question2, question3) VALUES (%s, %s, %s, %s)", (username, question1, question2, question3))
        mysql.connection.commit()
        cur.close()
        message = 'Thank you!'
        return render_template('save.html', message=message)


@app.route('/result', methods=['GET'])
def result():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM score")
    scores = cur.fetchall()
    return render_template('result.html', scores=scores)

if __name__ == '__main__':
    app.run(debug=True)
