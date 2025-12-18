from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Koble til database
def get_db_connection():
    conn = sqlite3.connect("notes.db")
    conn.row_factory = sqlite3.Row
    return conn

# Opprett tabell hvis den ikke finnes
def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        note = request.form["note"]

        if note.strip() != "":
            conn = get_db_connection()
            conn.execute("INSERT INTO notes (content) VALUES (?)", (note,))
            conn.commit()
            conn.close()

        return redirect("/")

    conn = get_db_connection()
    notes = conn.execute("SELECT * FROM notes ORDER BY id DESC").fetchall()
    conn.close()

    return render_template("index.html", notes=notes)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
