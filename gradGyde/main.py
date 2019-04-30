# pylint: disable=R1714
import os
import json
from flask import render_template, request, session, url_for
from flask_oauthlib.client import OAuth, redirect
from gradGyde import app
from .db_helper import (assign_aoc,
                        delete_class_taken,
                        delete_pref_aoc,
                        get_aoc_by_id,
                        get_aoc_json,
                        get_class_by_id,
                        get_classes,
                        get_classes_taken,
                        get_classes_taken_json,
                        get_lacs_json,
                        get_user,
                        make_user,
                        search_aoc_json,
                        search_classes_json,
                        take_class,
                        update_user)
from .models import UserType, SemesterType
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
    return redirect('/login')


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
    session['user_type'] = user.user_type.value
    if session['user_type'] == UserType.ADMIN.value:
        return redirect('/admin')
    return redirect('/student_dashboard')

@app.route('/login')
def login():
    if 'google_token' in session:
        return redirect('/student_dashboard')
    return render_template('login.html')

@app.route('/logout')
def oauth_logout():
    session.pop('google_token', None)
    session.pop('google_user', None)
    session.pop('user_email', None)
    session.pop('user_year', None)
    session.pop('user_type', None)
    return redirect('/login')

@app.route('/signup_form')
def signup_form():
    if 'google_token' not in session:
        return redirect('/login')
    return render_template('signup_form.html')


@app.route('/signup_form/post', methods=['POST'])
def signup_form_submit():
    if 'google_token' not in session:
        return redirect('/login')
    name = request.form['name']
    #aoc = request.form.getlist(''divisional'')
    #slash = request.form.getlist('slash')
    da_year = request.form['year']
    make_user(session['user_email'], name, da_year, UserType.STUDENT)
    user = get_user(session['user_email'])
    session['user_name'] = user.user_name
    session['user_year'] = user.year_started
    session['user_type'] = user.user_type.value
    return redirect('/student_dashboard')


@app.route('/student_dashboard')
def dash_stud():
    if 'google_token' not in session:
        return redirect('/login')
    if session['user_type'] == UserType.ADMIN.value:
        return redirect('/admin')
    user = get_user(session['user_email'])
    aocs = get_aoc_json(user, 'divisional')
    doubles = get_aoc_json(user, 'double')
    slashes = get_aoc_json(user, 'slash')
    #print(aocs)
    #print(doubles)
    #print(slashes)
    return render_template('dash_stud.html',
                           name=session['user_name'],
                           aocs=aocs,
                           doubles=doubles,
                           slashes=slashes)


@app.route('/student_dashboard/lacs')
def lacs():
    if 'google_token' not in session:
        return redirect('/login')
    lac = {
        'LAC0' : {
            'name' : 'Diverse Perspectives',
            'fulfilled' : True,
            'courses' : ['External Credit'],
            'id' : 0
            },
        'LAC1' : {
            'name' : 'Social Science',
            'fulfilled' : False,
            'courses' : None,
            'id' : 1
            }
    }
    if session['user_type'] == UserType.ADMIN.value:
        return redirect('/admin')
    # user = get_user(session['user_email'])
    lac = get_lacs_json(user)
    #print(lac)
    return render_template('lac.html', lac=lac)


@app.route('/student_dashboard/lacs/post', methods=['POST'])
def lacs_form_submit():
    if 'google_token' not in session:
        return redirect('/login')
    if session['user_type'] == UserType.ADMIN.value:
        return redirect('/admin')

    print(request.form)
    # old_json = data["old"]
    # new_json = data["new"]
    return render_template('lac.html')


@app.route('/student_dashboard/settings')
def settings():
    if 'google_token' not in session:
        return redirect('/login')
    if session['user_type'] == UserType.ADMIN.value:
        return redirect('/admin')
    user = get_user(session['user_email'])
    aocs = get_aoc_json(user, 'divisional')
    aocs_slash = get_aoc_json(user, "slash")
    aocs_double = get_aoc_json(user, "double")
    return render_template('settings.html',
                           name=session['user_name'],
                           year=session['user_year'],
                           aocs=json.loads(aocs),
                           doubles=json.loads(aocs_double),
                           slashes=json.loads(aocs_slash))

@app.route('/student_dashboard/settings/post', methods=['POST'])
def settings_form_submit():
    if 'google_token' not in session:
        return redirect('/login')
    if session['user_type'] == UserType.ADMIN.value:
        return redirect('/admin')
    name = request.form['name']
    da_year = request.form['year']
    update_user(session['user_email'], name, da_year)
    user = get_user(session['user_email'])
    session['user_name'] = user.user_name
    session['user_year'] = user.year_started
    return redirect('/student_dashboard/settings')


@app.route('/student_dashboard/courses')
def my_courses():
    if 'google_token' not in session:
        return redirect('/login')
    if session['user_type'] == UserType.ADMIN.value:
        return redirect('/admin')
    user = get_user(session['user_email'])
    course_list = get_classes_taken(user)
    #print(course_list)
    courses = get_classes_taken_json(course_list)
    #print(courses)
    return render_template('courses.html',
                           courses=courses)

@app.route('/student_dashboard/explore')
def explore():
    if 'google_token' not in session:
        return redirect('/login')
    if session['user_type'] == UserType.ADMIN.value:
        return redirect('/admin')
    return render_template('explore.html')


@app.route('/student_dashboard/explore_results', methods=['GET', 'POST'])
def explore_results():
    if 'google_token' not in session:
        return redirect('/login')
    if session['user_type'] == UserType.ADMIN.value:
        return redirect('/admin')
    user = get_user(session['user_email'])
    search_type = request.args.get('type')
    search_name = request.args.get('name')
    search_year = request.args.get('year')
    if search_name == "" or search_name == "Any":
        search_name = None
    if search_year == "" or search_year == "Any":
        search_year = None
    #print(request.args) = ([('type', 'courses'), ('name', ''), ('year', ''), ('semester', 'Fall')]
    # query db to get results based on user input.
    # NOTE: the user isn't required to fill in every field
    if search_type == "courses":
        search_semester = request.args.get('semester')
        semester_enums = {'Spring' : SemesterType.SPRING,
                          'Summer' : SemesterType.SUMMER,
                          'Fall' : SemesterType.FALL}
        search_semester = semester_enums[search_semester]
        classes = get_classes(search_name, search_year, search_semester)
        results = search_classes_json(user, classes)

    elif search_type == "aocs":
        results = search_aoc_json(user, 'divisional', search_name, search_year)
    elif search_type == "doubles":
        results = search_aoc_json(user, 'double', search_name, search_year)
    elif search_type == "slashes":
        results = search_aoc_json(user, 'slash', search_name, search_year)
    else:
        results = None
    return results


@app.route('/removecourses', methods=['POST'])
def remove_course():
    user = get_user(session['user_email'])
    # remove from db
    course = request.form['id']
    delete_class_taken(user.user_id, course)
    return "Successfully removed course " + course


@app.route('/removeaoi', methods=['POST'])
def remove_aoi():
    user = get_user(session['user_email'])
    aoi = request.form['id']
    delete_pref_aoc(user.user_id, aoi)
    return "Successfully removed AOI " + aoi


@app.route('/addcourse', methods=['POST'])
def add_course():
    user = get_user(session['user_email'])
    course = request.form['id']
    take_class(get_class_by_id(course), user)
    return "Successfully added course " + course

@app.route('/addaoi', methods=['POST'])
def add_aoi():
    user = get_user(session['user_email'])
    aoi = request.form['id']
    assign_aoc(get_aoc_by_id(aoi), user)
    return "Successfully add AOI " + aoi


@app.route('/admin')
def admin():
    if 'google_token' not in session:
        return redirect('/login')
    if session['user_type'] == UserType.STUDENT.value:
        return redirect('/student_dashboard')
    return render_template('admin.html')



@app.route('/admin/results', methods=['GET'])
def admin_results():

    search_type = request.args.get('type')

    # query db to get results based on user input.
    # NOTE: the user isn't required to fill in every field
    if search_type == "courses":
        results = {
            'COURSE0' : {
                'name' : 'course0',
                'year' : 2017,
                'id' : 327678,
                'semester' : 'Fall',
                'taken' : True
            },
            'COURSE1' : {
                'name' : 'course1',
                'year' : 2017,
                'id' : 345890,
                'semester' : 'Spring',
                'taken' : False
            }
        }
    elif search_type == "aocs":
        results = {
            "AOC0": {
                "id": 1,
                "name": "Computer Science (Regular)",
                "type": "aoc",
                "year": 2017,
                "assigned" : True,
                "requirements": {
                    "req0": {
                        "id": 1,
                        "name": "CS Introductory Course",
                        "amount": 1,
                        "fulfilled": False,
                        "classes": {
                            "class0": {
                                "id": 1,
                                "name": "Introduction to Programming With Python",
                                "taken": False
                            },
                            "class1": {
                                "id": 2,
                                "name": "Test 1",
                                "taken": False
                            },
                            "class2": {
                                "id": 3,
                                "name": "Test 2",
                                "taken": False
                            },
                            "class3": {
                                "id": 4,
                                "name": "Test 3",
                                "taken": False
                            }
                        }
                    },
                    "req1": {
                        "id": 2,
                        "name": "Object Oriented Programming With Java",
                        "amount": 1,
                        "fulfilled": False,
                        "classes": {
                            "class0": {
                                "id": 1,
                                "name": "Introduction to Programming With Python",
                                "taken": False
                            },
                            "class1": {
                                "id": 4,
                                "name": "Test 3",
                                "taken": False
                            }
                        }
                    }
                }
            }
        }
    elif search_type == "doubles":
        results = {
            "AOC0": {
                "id": 2,
                "name": "Computer Science (Regular)",
                "type": "double",
                "year": 2017,
                "assigned" : False,
                "requirements": {
                    "req0": {
                        "id": 1,
                        "name": "CS Introductory Course",
                        "amount": 1,
                        "fulfilled": False,
                        "classes": {
                            "class0": {
                                "id": 1,
                                "name": "Introduction to Programming With Python",
                                "taken": False
                            },
                            "class1": {
                                "id": 2,
                                "name": "Test 1",
                                "taken": False
                            },
                            "class2": {
                                "id": 3,
                                "name": "Test 2",
                                "taken": False
                            },
                            "class3": {
                                "id": 4,
                                "name": "Test 3",
                                "taken": False
                            }
                        }
                    },
                    "req1": {
                        "id": 2,
                        "name": "Object Oriented Programming With Java",
                        "amount": 1,
                        "fulfilled": False,
                        "classes": {
                            "class0": {
                                "id": 1,
                                "name": "Introduction to Programming With Python",
                                "taken": False
                            },
                            "class1": {
                                "id": 4,
                                "name": "Test 3",
                                "taken": False
                            }
                        }
                    }
                }
            }
        }
    elif search_type == "slashes":
        results = {
            "AOC0": {
                "id": 1,
                "name": "Computer Science (Regular)",
                "type": "aoc",
                "year": 2017,
                "assigned" : False,
                "requirements": {
                    "req0": {
                        "id": 1,
                        "name": "CS Introductory Course",
                        "amount": 1,
                        "fulfilled": False,
                        "classes": {
                            "class0": {
                                "id": 1,
                                "name": "Introduction to Programming With Python",
                                "taken": False
                            },
                            "class1": {
                                "id": 2,
                                "name": "Test 1",
                                "taken": False
                            },
                            "class2": {
                                "id": 3,
                                "name": "Test 2",
                                "taken": False
                            },
                            "class3": {
                                "id": 4,
                                "name": "Test 3",
                                "taken": False
                            }
                        }
                    },
                    "req1": {
                        "id": 2,
                        "name": "Object Oriented Programming With Java",
                        "amount": 1,
                        "fulfilled": False,
                        "classes": {
                            "class0": {
                                "id": 1,
                                "name": "Introduction to Programming With Python",
                                "taken": False
                            },
                            "class1": {
                                "id": 4,
                                "name": "Test 3",
                                "taken": False
                            }
                        }
                    }
                }
            }
        }
    else:
        results = {}
    results = json.dumps(results)

    return results


@app.route('/admin/removecourse', methods=['POST'])
def admin_removecourse():
    if 'google_token' not in session:
        return redirect('/login')
    if session['user_type'] == UserType.STUDENT.value:
        return redirect('/student_dashboard')

    course = request.form['id']

    return "Successfully removed course " + course


@app.route('/admin/removeaoi', methods=['POST'])
def admin_removeaoi():
    if 'google_token' not in session:
        return redirect('/login')
    if session['user_type'] == UserType.STUDENT.value:
        return redirect('/student_dashboard')

    aoi = request.form['id']

    return "Successfully removed AOI " + aoi
