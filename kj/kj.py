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
    USERNAME='admin',
    PASSWORD='default'
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


# @app.route('/add_entry')
# def add_entry():
#     # if not session.get('logged_in'):
#     #     abort(401)
#     db = get_db()
#     # db.execute('insert into entries (title, text) values (?, ?)',
#     #              [request.form['title'], request.form['text']])
#     # db.commit()
#     session['pageid'] = 1;
#     flash('New entry was successfully posted')
#     return render_template('addentry.html')
#
#     # return redirect(url_for('show_entries'))

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

@app.route('/show_exp',methods=['GET'])
def show_exp():
    # if not session.get('logged_in'):
    #     abort(401)
    db = get_db() # find all the element of exp
    cur = db.execute('select * from experience order by eventrank desc')
    session['pageid'] = 'Experience';
    session['pageindex'] = 1;

    return render_template('showcase.html',list=cur,strtemp='show_exp')



@app.route('/add_sc',methods=['GET'])
def add_sc():
    # if not session.get('logged_in'):
    #     abort(401)
    session['pageid'] = 'School Content';
    session['pageindex'] = 2;
    return render_template('addentry.html')

@app.route('/show_sc',methods=['GET'])
def show_sc():
    # if not session.get('logged_in'):
    #     abort(401)
    db = get_db() # find all the element of exp
    cur = db.execute('select * from content order by eventrank desc')
    session['pageid'] = 'School Content';
    session['pageindex'] = 2;

    return render_template('showcase.html',list=cur)


@app.route('/add_ps',methods=['GET'])
def add_ps():
    # if not session.get('logged_in'):
    #     abort(401)
    session['pageid'] = 'Professional Skill';
    session['pageindex'] = 3;
    return render_template('addentry.html')

@app.route('/show_sc',methods=['GET'])
def show_ps():
    # if not session.get('logged_in'):
    #     abort(401)
    db = get_db() # find all the element of exp
    cur = db.execute('select * from skill order by eventrank desc')
    session['pageid'] = 'Professional Skill';
    session['pageindex'] = 3;

    return render_template('showcase.html',list=cur)

@app.route('/add_ec',methods=['GET'])
def add_ec():
    # if not session.get('logged_in'):
    #     abort(401)
    session['pageid'] = 'Extra Curricular';
    session['pageindex'] = 4;

    return render_template('addentry.html')

@app.route('/show_ec',methods=['GET'])
def show_ec():
    # if not session.get('logged_in'):
    #     abort(401)
    db = get_db() # find all the element of exp
    cur = db.execute('select * from curricular order by eventrank desc')
    session['pageid'] = 'Extra Curricular';
    session['pageindex'] = 4;

    return render_template('showcase.html',list=cur)

@app.route('/add_pj',methods=['GET'])
def add_pj():
    # if not session.get('logged_in'):
    #     abort(401)
    session['pageid'] = 'Project';
    session['pageindex'] = 5;

    return render_template('addentry.html')

@app.route('/show_pj',methods=['GET'])
def show_pj():
    # if not session.get('logged_in'):
    #     abort(401)
    db = get_db() # find all the element of exp
    cur = db.execute('select * from project order by eventrank desc')
    session['pageid'] = 'Project';
    session['pageindex'] = 5;
    return render_template('showcase.html',list=cur)

@app.route('/add_ah',methods=['GET'])
def add_ah():
    # if not session.get('logged_in'):
    #     abort(401)
    session['pageid'] = 'Awards and Honor';
    session['pageindex'] = 6;
    return render_template('addentry.html')

@app.route('/show_ah',methods=['GET'])
def show_ah():
    # if not session.get('logged_in'):
    #     abort(401)
    db = get_db() # find all the element of exp
    cur = db.execute('select * from award order by eventrank desc')
    session['pageid'] = 'Awards and Honor';
    session['pageindex'] = 6;
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
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)
