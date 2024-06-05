from flask import Flask, render_template, request, redirect, url_for, session, g
import sqlite3
import json
from scraper import get_data
from flask import Flask, request, render_template_string, send_from_directory
import subprocess
import os
from datetime import datetime

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

@app.route('/')
def index():
    return redirect('/entrance')

@app.route('/entrance')
def entrance():
    return render_template('entrancePage.html')

@app.route('/register')
def register():
    return render_template('registerPage.html')

@app.route('/home')
def home():
    return render_template('homePage.html')

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

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data.get('password', None)

    conn = get_db()
    # user = conn.execute('SELECT * FROM users WHERE name = ? AND password = ?', (username, password)).fetchone()
    user = conn.execute('SELECT * FROM users WHERE name = ? ', (username,)).fetchone()
    mypassword=user[2]
    #print(mypassword)
    conn.close()
    if user is None:
        return jsonify({'status': 'error', 'message': 'Invalid username or password'})

    session['username'] = username
    return jsonify({'status': 'success','password':mypassword})

@app.route('/register_user', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data['username']
    password = data['password']

    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT MAX(user_id) FROM users')
    max_id = cursor.fetchone()[0]
    new_id = 0 if max_id is None else max_id + 1

    cursor.execute('INSERT INTO users (user_id, name, password) VALUES (?, ?, ?)', (new_id, username, password))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success', 'user_id': new_id})
    

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
    post = conn.execute('SELECT p.title, u.name, p.created_at, p.content, '
                        '(SELECT COUNT(*) FROM likesForPost WHERE post_id = p.post_id) as likes '
                        'FROM posts p JOIN users u ON p.author_id = u.user_id '
                        'WHERE p.post_id = ? AND p.visible = 1 AND p.deleted = 0', (post_id,)).fetchone()
    
    comments = conn.execute('SELECT c.content, u.name, c.created_at '
                            'FROM comments c JOIN users u ON c.author_id = u.user_id '
                            'WHERE c.post_id = ? AND c.deleted = 0', (post_id,)).fetchall()
    conn.close()

    if post is None:
        return jsonify({'status': 'error', 'message': 'Post not found'})

    post_details = {
        'title': post[0],
        'author': post[1],
        'created_at': post[2],
        'content': post[3],
        'likes': post[4],
        'comments': [{'content': comment[0], 'author': comment[1], 'created_at': comment[2]} for comment in comments]
    }
    
    return jsonify({'status': 'success', 'post': post_details})

@app.route('/like', methods=['POST'])
def like_post():
    data = request.get_json()
    post_id = data['post_id']
    usrname = data['usrname']
    conn = get_db()
    cursor = conn.cursor()
    user_id = cursor.execute('SELECT user_id FROM users WHERE name = ?', (usrname,)).fetchone()[0]


    if not user_id:
        return jsonify({'status': 'error', 'message': 'User not logged in'})

    
    
    # Check if user already liked the post
    liked = cursor.execute('SELECT * FROM likesForPost WHERE post_id = ? AND user_id = ?', (post_id, user_id)).fetchone()
    
    if liked:
        cursor.execute('DELETE FROM likesForPost WHERE post_id = ? AND user_id = ?', (post_id, user_id))
    else:
        cursor.execute('INSERT INTO likesForPost (post_id, user_id) VALUES (?, ?)', (post_id, user_id))

    conn.commit()
    conn.close()

    return jsonify({'status': 'success'})

@app.route('/comment', methods=['POST'])
def add_comment():
    data = request.get_json()
    post_id = data['post_id']
    content = data['content']
    usrname = data['usrname']
    conn = get_db()
    cursor = conn.cursor()
    user_id = cursor.execute('SELECT user_id FROM users WHERE name = ?', (usrname,)).fetchone()[0]
    if not user_id:
        return jsonify({'status': 'error', 'message': 'User not logged in'})


    
    cursor.execute('INSERT INTO comments (author_id, post_id, content, created_at, updated_at) VALUES (?, ?, ?, ?, ?)',
                   (user_id, post_id, content, datetime.now().isoformat(), datetime.now().isoformat()))

    conn.commit()
    conn.close()

    return jsonify({'status': 'success'})


@app.route('/postsss/<int:post_id>', methods=['GET'])
def getsss_post(post_id):
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

@app.route('/likesss/<int:post_id>', methods=['POST'])
def likesss_post(post_id):
    user_id = session.get('user_id')
    if user_id is None:
        return jsonify({'status': 'error', 'message': 'User not logged in'})

    conn = get_db()
    conn.execute('INSERT INTO likes (type, correspond_id, user_id, liked_at) VALUES (1, ?, ?, ?)', (post_id, user_id, datetime.now()))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success', 'message': 'Post liked'})

@app.route('/commentsss/<int:post_id>', methods=['POST'])
def add_commentsss(post_id):
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

@app.route('/profile')
def profile():
    # 從資料庫獲取用戶數據
    user = get_user_from_database()
    if user is None:
        return redirect(url_for('entrance'))
    posts = get_posts_from_database(user['id'])
    posts_amount = len(posts)

    return render_template('profile.html', user=user, posts=posts, posts_amount=posts_amount)

def get_user_from_database():
    # 假設這裡有一個函數來從資料庫提取數據
    conn = get_db()
    cursor = conn.cursor()
    if 'username' in session and session['username']:
        cursor.execute('''select * from users where name = ?''', (session['username'],))
        res = cursor.fetchone()
        return {
            'id': res[0],
            'username': res[1],
            'gender': res[5],
            'birthday': res[4],
            'bio': '一個熱愛技術的開發者',
            'website_href': 'http://example.com',
            'website_name': 'example.com'
        }
    else:
        return None

def get_posts_from_database(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''select * from posts where author_id = ?''', (user_id,))
    posts = cursor.fetchall()
    print(posts)
    return posts

if __name__ == '__main__':
    app.run(debug=True)


# def init_db():
#     with app.app_context():
#         db = get_db()
#         cursor = db.cursor()
#         cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
#                             id INTEGER PRIMARY KEY AUTOINCREMENT,
#                             name TEXT,
#                             course TEXT,
#                             deadline TEXT)''')
#         cursor.execute('''CREATE TABLE IF NOT EXISTS courses (
#                             id INTEGER PRIMARY KEY AUTOINCREMENT,
#                             name TEXT)''')
#         db.commit()

# #@app.before_first_request
# def initialize():
#     init_db()


    