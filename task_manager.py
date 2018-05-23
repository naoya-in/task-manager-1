# coding: UTF-8
from bottle import route, run, template, redirect, request
import sqlite3

# データベースに接続
dbname = "todo.db"
conn = sqlite3.connect(dbname)
c = conn.cursor()

conn.commit()
conn.close()


# / にアクセスしたら、index関数が呼ばれる
@route("/")
def index():
    todo_list = get_todo_list()
    return template("index", todo_list=todo_list)


# methodにPOSTを指定して、add関数を実装する
@route("/add", method="POST")
def add():
    name = request.forms.getunicode("name")
    important = request.forms["important"]
    deadline = request.forms["deadline"]

    todo_list = [name, important, deadline]

    save_todo(todo_list)
    return redirect("/")


# @routeデコレータの引数で<xxxx>と書いた部分は引数として関数に引き渡すことができます。
# intは数字のみ受け付けるフィルタ
@route("/delete/<todo_id:int>")
def delete(todo_id):
    delete_todo(todo_id)
    return redirect("/")


@route("/done/<todo_id:int>")
def done(todo_id):
    done_todo(todo_id)

    return redirect("/")


def get_todo_list():
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    select = "select task.id, task.name, task.important, task.deadline, task.is_done from task"
    c.execute(select)
    todo_list = []
    for row in c.fetchall():
        todo_list.append({
            "id": row[0],
            "name": row[1],
            "important": row[2],
            "deadline": row[3],
            "is_done": row[4],
        })
    conn.close()
    return todo_list


def save_todo(todo_list):
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()

    name = todo_list[0]
    important = todo_list[1]
    deadline = ""

    if len(todo_list) == 3:
        deadline = todo_list[2]

    task = (name, important, deadline, False)

    insert = 'INSERT INTO task(name, important, deadline, is_done) VALUES (?, ?, DATE (?), ?)'

    cursor.execute(insert, task)
    connection.commit()
    connection.close()


def delete_todo(todo_id):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    delete = "delete from task where id=?"
    c.execute(delete, (todo_id,))
    conn.commit()
    conn.close()


def done_todo(todo_id):
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()

    update = "UPDATE task SET is_done = TRUE WHERE id = ?"

    cursor.execute(update, (todo_id,))
    connection.commit()
    connection.close()


# テスト用のサーバをlocalhost:8080で起動する
run(host="localhost", port=12345, debug=True, reloader=True)
