import os
import json
from flask import render_template, request, session, url_for
from flask_oauthlib.client import OAuth, redirect
from gradGyde import app
from .db_helper import get_user, make_user
from .models import UserType

OAUTH = OAuth()
GOOGLE = OAUTH.remote_app('google',
                          consumer_key=os.getenv('GOOGLE_CONS_KEY'),
                          consumer_secret=os.getenv('GOOGLE_CONS_SECRET'),
                          request_token_params={'scope': 'email'},
                          base_url='https://www.googleapis.com/oauth2/v1/',
                          request_token_url=None,
                          access_token_method='POST',
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          authorize_url='https://accounts.google.com/o/oauth2/auth')


@GOOGLE.tokengetter
def get_google_token():
    return session.get("google_token")


@app.route('/')
def index():
    return redirect('/student_dashboard')


@app.route('/oauth_google')
def oauth_google():
    return GOOGLE.authorize(callback=url_for('oauth_google_authorized',
                                             _external=True))


@app.route('/authorized/')
def oauth_google_authorized():
    resp = GOOGLE.authorized_response()
    if resp is None:
        return 'Google denied access. Reason: %s \n Error: %s' % (
            request.args['error_reason'],
            request.args['error_description'])
    session['google_token'] = (resp['access_token'], '')
    user_info = GOOGLE.get('userinfo').data
    session['google_user'] = user_info
    session['user_email'] = session['google_user']['email']
    user = get_user(session['user_email'])
    if user is None:
        return redirect('/signup_form')
    session['user_name'] = user.user_name
    session['user_year'] = user.year_started
    session['user_type'] = str(user.user_type)
    return redirect('/student_dashboard')


@app.route('/login')
def login():
    if 'google_token' in session:
        return redirect('/student_dashboard')
    return render_template('login.html')


@app.route('/logout')
def oauth_logout():
    session.pop('google_token', None)
    session['google_user'] = None
    session['user_email'] = None
    return redirect('/login')


@app.route('/signup_form')
def signup_form():
    if 'google_token' not in session:
        return redirect('/login')
    # Change these to pull from the database
    aoc = ['Wizardry',
           'Computer Science',
           'General Studies',
           'Underwater Basket Weaving',
           'Biology']
    return render_template('signup_form.html',
                           aocs=aoc,
                           slashs=aoc,
                           doubles=aoc)


@app.route('/signup_form/post', methods=['POST'])
def signup_form_submit():
    if 'google_token' not in session:
        return redirect('/login')
    name = request.form['name']
    #aoc = request.form.getlist('AOC')
    #slash = request.form.getlist('slash')
    da_year = request.form['year']
    make_user(session['user_email'], name, da_year, UserType.STUDENT)
    user = get_user(session['user_email'])
    session['user_name'] = user.user_name
    session['user_year'] = user.year_started
    session['user_type'] = str(user.user_type)
    return redirect('/student_dashboard')


@app.route('/student_dashboard')
def dash_stud():
    if 'google_token' not in session:
        return redirect('/login')

    aocs = {
        "AOC1" : {
            "Name" : "Computer Science 2018",
            "Requirements" : {
                "Req1" : {
                    "Name" :  "CS Introductory Course",
                    "Amount" : 1,
                    "Fulfilled" : True,
                    "Classes" : {
                        "Class1" : {
                            "Name" : "Intro to Programming in Python",
                            "Taken" : False
                        },
                        "Class2" : {
                            "Name" : "Intro to Programming in C",
                            "Taken" : True
                        }
                    }
                },
                "Req2" : {
                    "Name" :  "Math",
                    "Amount" : 2,
                    "Fulfilled" : False,
                    "Classes" : {
                        "Class1" : {
                            "Name" : "Calculus 1",
                            "Taken" : False
                        },
                        "Class2" : {
                            "Name" : "Discrete Mathematics for Computer Science",
                            "Taken" : True
                        },
                        "Class3" : {
                            "Name" : "Dealing With Data",
                            "Taken" : False
                        }
                    }
                }
            }
        }
    }

    aocs = json.dumps(aocs)

    return render_template('dash_stud.html',
                           name=session['user_name'],
                           aocs=aocs)


@app.route('/student_dashboard/lacs')
def lacs():
    if 'google_token' not in session:
        return redirect('/login')
    lacs = {
        'LAC0' : {
            'name' : 'Diverse Perspectives',
            'fullfilled' : True,
            'course' : 'Norman Conquests'
            },
        'LAC1' : {
            'name' : 'Social Science',
            'fullfilled' : False,
            'course' : None
            }
    }
    return render_template('lac.html', lacs=lacs)


@app.route('/student_dashboard/lacs/post', methods=['POST'])
def lacs_form_submit():
    if 'google_token' not in session:
        return redirect('/login')
    return redirect('/student_dashboard/lacs')


@app.route('/student_dashboard/settings')
def settings():
    if 'google_token' not in session:
        return redirect('/login')
    aocs = ['Wizardry',
            'Computer Science',
            'General Studies',
            'Underwater Basket Weaving',
            'Biology']
    return render_template('settings.html',
                           aocs=aocs,
                           doubles=aocs,
                           slashes=aocs)


@app.route('/student_dashboard/settings/post', methods=['POST'])
def settings_form_submit():
    if 'google_token' not in session:
        return redirect('/login')
    return redirect('/student_dashboard/settings')
