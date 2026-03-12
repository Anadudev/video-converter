import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL

app = Flask(__name__)

mysql = MySQL(app)
app.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
app.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
app.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")


# print(app.config["MYSQL_HOST"])
@app.route('/login', methods=['POST'])
def login():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return "Credentials missing", 401
    cur = mysql.connection.cursor()
    res = cur.execute(
        "select emal, password frm user WHERE email=%s",
        (auth_header.username)
    )
    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]

        if not (auth_header.password == password and auth_header.username == email):
            return "Invalid credentials", 401
        else:
            return createJWT(auth_header.username, os.environ.get("JWT_SECRET"), True)
    else:
        return "invalid credentials", 401

@app.route('/validate', methods=['POST'])
def validate():
    encoded_jwt = request.headers['Authorization']

    if not encoded_jwt:
        return "Missing credentials", 401
    encoded_jwt = encoded_jwt.split(" ")[1]
    try:
        decoded = jwt.decode(
            encoded_jwt,
            os.environ.get("JWT_SECRET"),
            algorithms=["HS256"]
        )
    except:
        return "Not authorized", 403

    return decoded, 200



def createJWT(username, secrete, authz):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "admin": authz
        },
        secrete,
        algorithm="HS256"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0",  port=5000, debug=True)
