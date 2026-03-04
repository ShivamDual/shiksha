from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
import sqlite3
import os
import functools

dashboard = Blueprint('dashboard', __name__, template_folder='templates')

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'shabdakosh', 'database.db')

PASSWORD = "shiksha2024"

def login_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect('/dashboard/login')
        return f(*args, **kwargs)
    return decorated

@dashboard.route('/')
@login_required
def index():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # Total searches
    total_searches = conn.execute('SELECT COUNT(*) FROM usage_log').fetchone()[0]

    # Top searched terms this week
    top_searches = conn.execute('''
        SELECT search_query, COUNT(*) as count 
        FROM usage_log 
        WHERE timestamp >= datetime('now', '-7 days')
        GROUP BY search_query 
        ORDER BY count DESC 
        LIMIT 10
    ''').fetchall()

    # Searches per day (last 7 days)
    daily_searches = conn.execute('''
        SELECT DATE(timestamp) as date, COUNT(*) as count
        FROM usage_log
        WHERE timestamp >= datetime('now', '-7 days')
        GROUP BY DATE(timestamp)
        ORDER BY date
    ''').fetchall()

    # Total terms
    total_terms = conn.execute('SELECT COUNT(*) FROM terms').fetchone()[0]

    # Pending contributions
    pending = conn.execute('''
        SELECT COUNT(*) FROM pending_terms WHERE status = "pending"
    ''').fetchone()[0] if conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='pending_terms'"
    ).fetchone() else 0

    conn.close()

    return render_template('dashboard.html',
        total_searches=total_searches,
        top_searches=[dict(r) for r in top_searches],
        daily_searches=[dict(r) for r in daily_searches],
        total_terms=total_terms,
        pending=pending
    )

@dashboard.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == PASSWORD:
            session['logged_in'] = True
            return redirect('/dashboard/')
        return render_template('login.html', error="Wrong password")
    return render_template('login.html', error=None)

@dashboard.route('/logout')
def logout():
    session.clear()
    return redirect('/')