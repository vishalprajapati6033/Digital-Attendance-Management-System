from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Connect to SQLite Database
def connect_db():
    return sqlite3.connect('database.db')

# Initialize Database
def init_db():
    with connect_db() as con:
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS attendance (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        student_name TEXT NOT NULL,
                        date TEXT NOT NULL,
                        status TEXT NOT NULL)''')
        con.commit()

# Home Page - List Students
@app.route('/')
def index():
    return render_template('index.html')

# Page to Add Attendance
@app.route('/add-attendance', methods=['GET', 'POST'])
def add_attendance():
    if request.method == 'POST':
        student_name = request.form['student_name']
        status = request.form['status']
        date = datetime.now().strftime('%Y-%m-%d')
        
        with connect_db() as con:
            cur = con.cursor()
            cur.execute("INSERT INTO attendance (student_name, date, status) VALUES (?, ?, ?)", (student_name, date, status))
            con.commit()

        return redirect(url_for('view_attendance'))

    return render_template('add_attendance.html')

# View Attendance
@app.route('/view-attendance')
def view_attendance():
    with connect_db() as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM attendance ORDER BY date DESC")
        rows = cur.fetchall()

    return render_template('view_attendance.html', rows=rows)

# Generate Attendance Report
@app.route('/report')
def generate_report():
    with connect_db() as con:
        cur = con.cursor()
        cur.execute('''SELECT student_name, COUNT(CASE WHEN status = 'Present' THEN 1 END) AS present_days,
                            COUNT(CASE WHEN status = 'Absent' THEN 1 END) AS absent_days
                            FROM attendance GROUP BY student_name''')
        report = cur.fetchall()

    return render_template('report.html', report=report)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
