from contextlib import contextmanager
from pathlib import Path
import sqlite3

from flask import Flask, abort, redirect, render_template, request, url_for

app = Flask(__name__)
DATABASE = Path(__file__).with_name("tasks.db")


def connect_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


@contextmanager
def db_connection():
    connection = connect_db()
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()


def initialize_db():
    with db_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                details TEXT NOT NULL DEFAULT ''
            )
            """
        )


@app.route("/")
def index():
    with db_connection() as connection:
        tasks = connection.execute(
            "SELECT id, title, details FROM tasks ORDER BY id DESC"
        ).fetchall()
    return render_template("index.html", tasks=tasks)


@app.route("/tasks/new", methods=["GET", "POST"])
def create_task():
    title = ""
    details = ""
    error = None

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        details = request.form.get("details", "").strip()

        if not title:
            error = "Enter a title for the task."
        else:
            with db_connection() as connection:
                connection.execute(
                    "INSERT INTO tasks (title, details) VALUES (?, ?)",
                    (title, details),
                )
            return redirect(url_for("index"))

    return render_template(
        "task_form.html",
        page_title="Add a task",
        button_text="Create task",
        title=title,
        details=details,
        error=error,
    ), 400 if error else 200


@app.route("/tasks/<int:task_id>/edit", methods=["GET", "POST"])
def edit_task(task_id):
    with db_connection() as connection:
        task = connection.execute(
            "SELECT id, title, details FROM tasks WHERE id = ?",
            (task_id,),
        ).fetchone()

    if task is None:
        abort(404)

    title = task["title"]
    details = task["details"]
    error = None

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        details = request.form.get("details", "").strip()

        if not title:
            error = "Enter a title for the task."
        else:
            with db_connection() as connection:
                connection.execute(
                    "UPDATE tasks SET title = ?, details = ? WHERE id = ?",
                    (title, details, task_id),
                )
            return redirect(url_for("index"))

    return render_template(
        "task_form.html",
        page_title="Edit task",
        button_text="Save changes",
        title=title,
        details=details,
        error=error,
    ), 400 if error else 200


@app.route("/tasks/<int:task_id>/delete", methods=["POST"])
def delete_task(task_id):
    with db_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,),
        )

    if cursor.rowcount == 0:
        abort(404)
    return redirect(url_for("index"))


initialize_db()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
# min ga lar par
