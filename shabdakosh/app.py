from flask import Flask, render_template, request, jsonify
import sqlite3
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from dashboard.app import dashboard

app = Flask(__name__)
app.secret_key = "shiksha-secret-2024"
app.register_blueprint(dashboard, url_prefix='/dashboard')
DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS terms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            english TEXT NOT NULL,
            nepali TEXT NOT NULL,
            pronunciation TEXT,
            subject TEXT NOT NULL,
            grade TEXT,
            definition TEXT,
            example TEXT
        );
        CREATE VIRTUAL TABLE IF NOT EXISTS terms_fts USING fts5(
            english, nepali, definition, content=terms, content_rowid=id
        );
        CREATE TABLE IF NOT EXISTS usage_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            search_query TEXT,
            term_id INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search')
def search():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({'results': []})
    
    conn = get_db()
    results = conn.execute('''
        SELECT id, english, nepali, subject 
        FROM terms 
        WHERE english LIKE ? OR nepali LIKE ?
        LIMIT 10
    ''', (f'%{query}%', f'%{query}%')).fetchall()
    conn.close()

    return jsonify({'results': [dict(r) for r in results]})

@app.route('/api/log')
def log_search():
    query = request.args.get('q', '').strip()
    term_id = request.args.get('term_id', None)
    if query:
        conn = get_db()
        conn.execute('INSERT INTO usage_log (search_query, term_id) VALUES (?, ?)', (query, term_id))
        conn.commit()
        conn.close()
    return jsonify({'ok': True})

@app.route('/term/<int:term_id>')
def term(term_id):
    conn = get_db()
    t = conn.execute('SELECT * FROM terms WHERE id = ?', (term_id,)).fetchone()
    conn.close()
    if not t:
        return "Term not found", 404
    return render_template('term.html', term=dict(t))

@app.route('/subject/<subject_name>')
def subject(subject_name):
    conn = get_db()
    terms = conn.execute(
        'SELECT * FROM terms WHERE LOWER(subject) = LOWER(?)', 
        (subject_name,)
    ).fetchall()
    conn.close()
    return render_template('subject.html', terms=[dict(t) for t in terms], subject=subject_name)

@app.route('/contribute', methods=['GET', 'POST'])
def contribute():
    if request.method == 'POST':
        english = request.form.get('english', '').strip()
        nepali = request.form.get('nepali', '').strip()
        subject = request.form.get('subject', '').strip()
        grade = request.form.get('grade', '').strip()
        definition = request.form.get('definition', '').strip()
        example = request.form.get('example', '').strip()
        submitted_by = request.form.get('submitted_by', '').strip()

        if not english or not nepali or not subject:
            return render_template('contribute.html', error="English term, Nepali term and subject are required.", success=False)

        conn = get_db()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS pending_terms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                english TEXT, nepali TEXT, subject TEXT,
                grade TEXT, definition TEXT, example TEXT,
                submitted_by TEXT, status TEXT DEFAULT 'pending',
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.execute('''
            INSERT INTO pending_terms (english, nepali, subject, grade, definition, example, submitted_by)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (english, nepali, subject, grade, definition, example, submitted_by))
        conn.commit()
        conn.close()

        return render_template('contribute.html', success=True, error=None)

    return render_template('contribute.html', success=False, error=None)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)