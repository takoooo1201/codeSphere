from flask import Flask, render_template, request, redirect, url_for, session, g
import sqlite3
import json
from scraper import get_data
from flask import Flask, request, render_template_string, send_from_directory
import subprocess
import os

from flask import jsonify
from captcha.image import ImageCaptcha
import random
import string


# @app.route('/')
# def index():
#     return render_template_string(open('index.html').read())

app = Flask(__name__)
app.secret_key = 'supersecretkey'
DATABASE = 'codeSphere.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            course TEXT,
                            deadline TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS courses (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT)''')
        db.commit()

#@app.before_first_request
def initialize():
    init_db()

@app.route('/entrance')
def entrance():
    return render_template('entrancePage.html')

@app.route('/postPage')
def postPage():
    return render_template('postPage.html')

@app.route('/test')
def test():
    username = session.get('username')
    if username:
        return render_template('testing.html', username=username)
    return render_template('testing.html')

@app.route('/display')
def display():
    #get_posts()
    return render_template('displayPage.html')
    

@app.route('/posts', methods=['GET'])
def get_posts():
    conn = get_db()
    posts = conn.execute('SELECT * FROM posts WHERE visible = 1 AND deleted = 0').fetchall()
    conn.close()

    post_list = [{'post_id': post[0], 'title': post[2], 'content': post[3]} for post in posts]

    return jsonify({'status': 'success', 'posts': post_list})

@app.route('/post/<int:post_id>', methods=['GET'])
def get_post(post_id):
    conn = get_db()
    post = conn.execute('SELECT * FROM posts WHERE post_id = ?', (post_id,)).fetchone()
    comments = conn.execute('SELECT * FROM comments WHERE post_id = ? AND deleted = 0', (post_id,)).fetchall()
    conn.close()

    if post is None:
        return jsonify({'status': 'error', 'message': 'Post not found'})

    post_data = {
        'post_id': post[0],
        'author_id': post[1],
        'title': post[2],
        'content': post[3],
        'created_at': post[6],
        'updated_at': post[8]
    }

    comments_data = [{'comment_id': comment['comment_id'], 'author_id': comment['author_id'], 'content': comment['content'], 'created_at': comment['created_at']} for comment in comments]

    return jsonify({'status': 'success', 'post': post_data, 'comments': comments_data})

@app.route('/like/<int:post_id>', methods=['POST'])
def like_post(post_id):
    user_id = session.get('user_id')
    if user_id is None:
        return jsonify({'status': 'error', 'message': 'User not logged in'})

    conn = get_db()
    conn.execute('INSERT INTO likes (type, correspond_id, user_id, liked_at) VALUES (1, ?, ?, ?)', (post_id, user_id, datetime.now()))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success', 'message': 'Post liked'})

@app.route('/comment/<int:post_id>', methods=['POST'])
def add_comment(post_id):
    data = request.get_json()
    comment_text = data['comment']
    user_id = session.get('user_id')
    if user_id is None:
        return jsonify({'status': 'error', 'message': 'User not logged in'})

    conn = get_db()
    conn.execute(
        'INSERT INTO comments (post_id, author_id, content, created_at, updated_at) VALUES (?, ?, ?, ?, ?)',
        (post_id, user_id, comment_text, datetime.now(), datetime.now())
    )
    conn.commit()
    conn.close()

    return jsonify({'status': 'success', 'message': 'Comment added'})


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data.get('password', None)

    conn = get_db()
    # user = conn.execute('SELECT * FROM users WHERE name = ? AND password = ?', (username, password)).fetchone()
    user = conn.execute('SELECT * FROM users WHERE name = ? ', (username,)).fetchone()
    mypassword=user[2]
    print(mypassword)
    conn.close()

    if user is None:
        return jsonify({'status': 'error', 'message': 'Invalid username or password'})

    session['username'] = username
    return jsonify({'status': 'success','password':mypassword})


@app.route('/yt')
def yt():
    return render_template('yt.html')


@app.route('/calendar')
def calendar():
    if 'username' in session:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM tasks')
        tasks = cursor.fetchall()
        cursor.execute('SELECT * FROM courses')
        courses = cursor.fetchall()
        print(courses)
        tasks_json = json.dumps([
            {"title": task[0], "start": task[2], "course": task[1]}
            for task in tasks
        ])

        return render_template('calendar.html', tasks_json=tasks_json, courses=courses)
    return redirect(url_for('eeclasslogin'))

@app.route('/eeclasslogin', methods=['GET', 'POST'])
def eeclasslogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session['username'] = username
        session['password'] = password
        initialize()
        tasks, courses = get_data(username, password)
        db = get_db()
        cursor = db.cursor()

        for course in courses:
            cursor.execute('SELECT * FROM courses WHERE name = ?', (course,))
            if cursor.fetchone() is None:
                cursor.execute('INSERT INTO courses (name) VALUES (?)', (course,))

        for task in tasks:
            cursor.execute('SELECT * FROM tasks WHERE name = ?', (task['title'],))
            if cursor.fetchone() is None:
                cursor.execute('INSERT INTO tasks (name, course, deadline) VALUES (?, ?, ?)', 
                               (task['title'], task['source'], task['deadline']))
        
        db.commit()
        return redirect(url_for('calendar'))
    return render_template('eeclasslogin.html')

@app.route('/eeclasslogout')
def logout():
    session.pop('username', None)
    session.pop('password', None)
    return redirect(url_for('eeclasslogin'))

@app.route('/download', methods=['POST'])
def download():
    link = request.form['link']
    path = request.form['path']
    format = request.form['format']
    path = r'C:\Users\whsun\Desktop\\'
    if format == 'mp3':
        format_option = 'bestaudio/best'
        ext = 'mp3'
    else:
        format_option = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4'
        ext = 'mp4'

    title="myvideo"
    command = [
        './yt-dlp.exe',
        link,
        '-f', 'b[ext=mp4]', #format_option,
        '-o', f'{path}%(title)s.%(ext)s'
    ]

    # Execute command and capture output
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #output = result.stdout.decode()

    # Assuming the filename is based on the video title, which we don't know until the download completes
    # For demonstration, just attempting to send the first file with the correct extension in the specified directory

    try:
        # List all files in the directory
        files = [f for f in os.listdir(path) if f.endswith(ext)]
        if not files:
            return "No files found to download.", 404

        filename = files[0]  # Taking the first file that matches the extension
        #return send_from_directory(directory=path, filename=filename, as_attachment=True)\
        return "good"
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)