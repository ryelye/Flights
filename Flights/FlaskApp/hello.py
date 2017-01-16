import flask

mysql = flask.MySQL()
app = flask.Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'oliver'
app.config['MYSQL_DATABASE_PASSWORD'] = 'quahi7ul'
app.config['MYSQL_DATABASE_DB'] = 'flights'
app.config['MYSQL_DATABASE_HOST'] = 'rdsinstance.cpzyzqzkyyhy.ap-southeast-2.rds.amazonaws.com'
mysql.init_app(app)

@app.route("/")
def hello():
    return flask.render_template('templates/home.html')

@app.route('/Authenticate')
def Authenticate():
    username = flask.request.args.get('Username')
    password = flask.request.args.get('Password')
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * FROM users WHERE username = '%s' AND password = '%s'"%(username, password))
    data = cursor.fetchone()
    if data is None:
        return "Wrong username or password"
    else:
        return "Successful login"

if __name__ == "__main__":
    app.run()

