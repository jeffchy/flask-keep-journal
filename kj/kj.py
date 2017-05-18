# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'kj.db'),
    SECRET_KEY='development key',
    USERNAME='jiangchy',
    PASSWORD='shstujeff97'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv
def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

# DB


pages = ['','experience','content','skill','curricular','project','award']

@app.route('/', methods=['GET', 'POST'])
def index():
    db = get_db()
    # cur = db.execute('select title, text from entries order by id desc')

    if request.method == 'POST':
        print(request.form['eventDate'])
        print(request.form['eventName'])
        print(request.form['discription'])
        print(request.form['rating'])
        print(request.form['selectCate'])

        db.execute('insert into '+pages[session['pageindex']]+' (title, cate,discription,eventdate,eventrank) values (?, ?,?,?,?)',
                     [request.form['eventName'], request.form['selectCate'],request.form['discription'],request.form['eventDate'],request.form['rating']])
        db.commit()

    nums = [len(db.execute('select id from '+ pages[i]).fetchall()) for i in range(1,7)]
    session['pageindex'] = 0;

    return render_template('index.html', nums=nums)

@app.route('/add_exp',methods=['GET'])
def add_exp():
    # if not session.get('logged_in'):
    #     abort(401)
    db = get_db()
    # db.execute('insert into entries (title, text) values (?, ?)',
    #             [request.form['title'], request.form['text']])
    # db.commit()
    session['pageid'] = 'experience';
    session['pageindex'] = 1;
    return render_template('addentry.html')

    # return redirect(url_for('show_entries'))

@app.route('/add/<type>',methods=['GET'])
def add(type):
    # if not session.get('logged_in'):
    #     abort(401)
    db = get_db()
    # db.execute('insert into entries (title, text) values (?, ?)',
    #             [request.form['title'], request.form['text']])
    # db.commit()
    pageinfo = {
        'exp':(1,'experience'),
        'sc':(2,'School Content'),
        'ps':(3,'Professional Skill'),
        'ec':(4,'Extra Curricular'),
        'pj':(5,'Project'),
        'ah':(6,'Awards and Honor'),
    }
    session['pageid'] = pageinfo[type][1]
    session['pageindex'] = pageinfo[type][0]
    session['pagetype'] = type
    return render_template('addentry.html')


@app.route('/show/<type>',methods=['POST','GET'])
def show(type):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    db = get_db() # find all the element of exp

    pageinfo = {
        'exp':(1,'experience','experience'),
        'sc':(2,'School Content','content'),
        'ps':(3,'Professional Skill','skill'),
        'ec':(4,'Extra Curricular','curricular'),
        'pj':(5,'Project','project'),
        'ah':(6,'Awards and Honor','award'),
    }

    if request.method == 'POST':
        print("delete from " + pageinfo[type][2] + "where title=" + request.form['deleteData'])
        db.execute("delete from " + pageinfo[type][2] + " where title=\'" + request.form['deleteData'] + "\'") ## delete the entry
        db.commit()



    cur = db.execute('select * from '+ pageinfo[type][2] + ' order by eventrank desc')
    session['pageid'] = pageinfo[type][1] # 'experience'
    session['pageindex'] = pageinfo[type][0]
    session['pagetype'] = type

    return render_template('showcase.html',list=cur)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('mylogin.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))
