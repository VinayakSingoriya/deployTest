from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

# Database local connection
# db = pymysql.connect(host='localhost',user='root',password='vinayak',database='todo',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

# Database remote connection
db = pymysql.connect(
            host='record-testing.cmjf6xf1uo4z.us-east-1.rds.amazonaws.com',
            user='admin',
            password='vinayak123',
            database='vinayakRecord',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)

# Routing

@app.route("/")
def home():
    sql_select_Query = "select * from record"
    cursor = db.cursor()
    cursor.execute(sql_select_Query )
    todo_list =  cursor.fetchall()  
    return render_template("base.html", todo_list=todo_list)

# DONE
@app.route("/add", methods=["POST"])
def add():
    cursor = db.cursor()
    title = request.form.get("title")
    sql = """INSERT INTO record(title, complete) VALUES(%s, %s)"""
    data = (title, False)
    cursor.execute(sql, data)
    db.commit()
    return redirect(url_for("home"))


@app.route("/update/<int:todo_id>")
def update(todo_id):
    cursor = db.cursor()
    select_query = "select * from record where id = %s"
    cursor.execute(select_query, todo_id)
    record = cursor.fetchone()
    val = not(record["complete"])
    update_query = """update record set complete = %s where id = %s"""
    data = (val, todo_id)
    cursor.execute(update_query, data)
    db.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    cursor = db.cursor()
    Delete_query = """Delete from record where id = %s"""
    cursor.execute(Delete_query, todo_id)
    db.commit()
    return redirect(url_for("home"))

@app.route("/reset")
def reset():
    cursor = db.cursor()
    cursor.execute("TRUNCATE TABLE record")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=False)
 