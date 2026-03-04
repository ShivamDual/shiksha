from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)
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

    # Log the search
    conn = get_db()
    conn.execute('INSERT INTO usage_log (search_query) VALUES (?)', (query,))
    conn.commit()
    conn.close()

    return jsonify({'results': [dict(r) for r in results]})

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

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)