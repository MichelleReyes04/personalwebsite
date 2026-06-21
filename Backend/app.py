from pathlib import Path
import os

from flask import Flask, render_template, request
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_URL = os.environ.get('DATABASE_URL')
DB_PATH = Path(os.environ.get(
    'DATABASE_PATH',
    Path(__file__).resolve().parent / 'database.db'
))

app = Flask(
    __name__,
    template_folder=str(BASE_DIR),
    static_folder=str(BASE_DIR),
    static_url_path=''
)


def init_db():
    if DATABASE_URL:
        import psycopg

        with psycopg.connect(DATABASE_URL) as connection:
            connection.execute('''
                CREATE TABLE IF NOT EXISTS tickets (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    issue TEXT NOT NULL,
                    category TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    description TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
        return

    with sqlite3.connect(DB_PATH) as connect:
        connect.execute('''
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                issue TEXT NOT NULL,
                category TEXT NOT NULL,
                priority TEXT NOT NULL,
                description TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')


def save_ticket(ticket):
    if DATABASE_URL:
        import psycopg

        with psycopg.connect(DATABASE_URL) as connection:
            connection.execute(
                '''
                INSERT INTO tickets
                    (name, email, issue, category, priority, description)
                VALUES (%s, %s, %s, %s, %s, %s)
                ''',
                ticket
            )
        return

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            '''
            INSERT INTO tickets
                (name, email, issue, category, priority, description)
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            ticket
        )


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/submit-ticket', methods=['GET', 'POST'])
def submit_ticket():
    if request.method == 'GET':
        return render_template('submit-ticket.html')

    ticket = (
        request.form['name'],
        request.form['email'],
        request.form['issue'],
        request.form['category'],
        request.form['priority'],
        request.form['description']
    )

    save_ticket(ticket)

    return render_template(
        'submit-correct.html',
        message='Ticket submitted successfully!'
    )


@app.route('/add_user', methods=['POST'])
def add_user():
    return submit_ticket()


init_db()


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
