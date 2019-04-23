import os
import json
from flask import render_template, request, session, url_for
from flask_oauthlib.client import OAuth, redirect
from gradGyde import app
from .db_helper import (assign_aoc,
                        get_aoc,
                        get_aoc_json,
                        get_aocs_by_type,
                        get_user, 
                        make_user)
from .db_helper_test import db_helper_test
from .models import UserType

db_helper_test()
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

    aocs_divisional = get_aocs_by_type("Divisonal")
    aocs_divisional_names = []
    for aoc in aocs_divisional:
        aocs_divisional_names.append(aoc.aoc_name)

    aocs_slash = get_aocs_by_type("Slash")
    aocs_slash_names = []
    for aoc in aocs_slash:
        aocs_slash_names.append(aoc.aoc_name)

    aocs_double = get_aocs_by_type("Double")
    aocs_double_names = []
    for aoc in aocs_double:
        aocs_double_names.append(aoc.aoc_name)
    return render_template('signup_form.html',
                           aocs=aocs_divisional_names,
                           slashs=aocs_slash_names,
                           doubles=aocs_double_names)


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
    comp_sci = get_aoc("Computer Science (Regular)", "Divisonal")
    assign_aoc(comp_sci, user)
    return redirect('/student_dashboard')


@app.route('/student_dashboard')
def dash_stud():
    if 'google_token' not in session:
        return redirect('/login')
    user = get_user(session['user_email']) 
    aocs = get_aoc_json(user, "Divisonal")
    print(aocs)
    return render_template('dash_stud.html',
                           name=session['user_name'],
                           aocs=aocs)


@app.route('/student_dashboard/lacs')
def lacs():
    if 'google_token' not in session:
        return redirect('/login')
    lac = {
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
    return render_template('lac.html', lac=lac)


@app.route('/student_dashboard/lacs/post', methods=['POST'])
def lacs_form_submit():
    if 'google_token' not in session:
        return redirect('/login')
    return redirect('/student_dashboard/lacs')


@app.route('/student_dashboard/settings')
def settings():
    if 'google_token' not in session:
        return redirect('/login')
    aocs_divisional = get_aocs_by_type("Divisonal")
    aocs_divisional_names = []
    for aoc in aocs_divisional:
        aocs_divisional_names.append(aoc.aoc_name)
    print(aocs_divisional_names)
    aocs_slash = get_aocs_by_type("Slash")
    aocs_slash_names = []
    for aoc in aocs_slash:
        aocs_slash_names.append(aoc.aoc_name)

    aocs_double = get_aocs_by_type("Double")
    aocs_double_names = []
    for aoc in aocs_double:
        aocs_double_names.append(aoc.aoc_name)
    return render_template('settings.html',
                           aocs=aocs_divisional_names,
                           doubles=aocs_double_names,
                           slashs=aocs_slash_names)


@app.route('/student_dashboard/settings/post', methods=['POST'])
def settings_form_submit():
    if 'google_token' not in session:
        return redirect('/login')
    return redirect('/student_dashboard/settings')
