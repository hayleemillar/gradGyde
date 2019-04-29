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
    return render_template('signup_form.html')


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

    # valid types: "divisional", "double", "slash"
    aocs = {
        "aoc0": {
            "id": 0,
            "name": "Anthropology",
            "year": 2019,
            "type": "divisional",
            "requirements": {
                "req0": {
                    "id": 3,
                    "name": "Intro Anthro",
                    "amount": 1,
                    "fulfilled": False,
                    "classes": {}
                },
                "req1": {
                    "id": 4,
                    "name": "Intro Archeology",
                    "amount": 1,
                    "fulfilled": False,
                    "classes": {}
                },
                "req2": {
                    "id": 5,
                    "name": "Upper Level or Thematic Course",
                    "amount": 1,
                    "fulfilled": False,
                    "classes": {}
                },
                "req3": {
                    "id": 6,
                    "name": "History of Anthro Theory ",
                    "amount": 1,
                    "fulfilled": False,
                    "classes": {}
                },
                "req4": {
                    "id": 7,
                    "name": "Linguistic or Physical Anthro",
                    "amount": 1,
                    "fulfilled": False,
                    "classes": {}
                },
                "req5": {
                    "id": 8,
                    "name": "Method and Theory In Archeology ",
                    "amount": 1,
                    "fulfilled": False,
                    "classes": {}
                },
                "req6": {
                    "id": 9,
                    "name": "Foreign Lanuguage ",
                    "amount": 4,
                    "fulfilled": False,
                    "classes": {}
                }
            }
        },
        "aoc1": {
            "id": 1,
            "name": "Russian",
            "year": 2019,
            "type": "divisional",
            "requirements": {
                "req0": {
                    "id": 1,
                    "name": "Russian Language",
                    "amount": 6,
                    "fulfilled": False,
                    "classes": {}
                },
                "req1": {
                    "id": 2,
                    "name": "Russian Literature",
                    "amount": 6,
                    "fulfilled": False,
                    "classes": {}
                }
            }
        }
    }

    doubles = {
        "aoc0": {
            "id": 2,
            "name": "Classics",
            "year": 2019,
            "type": "double",
            "requirements": {
                "req0": {
                    "id": 69,
                    "name": "Greek or Latin",
                    "amount": 9,
                    "fulfilled": False,
                    "classes": {}
                },
                "req1": {
                    "id": 70,
                    "name": "Greek and Roman Culture",
                    "amount": 4,
                    "fulfilled": False,
                    "classes": {}
                }
            }
        }
    }

    slashes = {
        "aoc0": {
            "id": 3,
            "name": "Classics",
            "year": 2019,
            "type": "slash",
            "requirements": {
                "req0": {
                    "id": 69,
                    "name": "Greek or Latin",
                    "amount": 9,
                    "fulfilled": False,
                    "classes": {}
                },
                "req1": {
                    "id": 70,
                    "name": "Greek and Roman Culture",
                    "amount": 4,
                    "fulfilled": False,
                    "classes": {}
                }
            }
        }
    }


    aocs = json.dumps(aocs)
    doubles = json.dumps(doubles)
    slashes = json.dumps(slashes)

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

    return render_template('lac.html', lac=lac)


@app.route('/student_dashboard/lacs/post', methods=['POST'])
def lacs_form_submit():
    if 'google_token' not in session:
        return redirect('/login')

    oldJson = request.args.get("old")
    newJson = request.args.get("new")

    return redirect('/student_dashboard/lacs')


@app.route('/student_dashboard/settings')
def settings():
    if 'google_token' not in session:
        return redirect('/login')

    name = "Haylee"
    year = 2017

    aocs = {
        "aoc0": {
            "id": 2,
            "name": "Anthropology",
            "year": 2019,
            "type": "divisional",
            "requirements": {
                "req0": {
                    "id": 3,
                    "name": "Intro Anthro",
                    "amount": 1,
                    "fulfilled": False,
                    "classes": {}
                },
                "req1": {
                    "id": 4,
                    "name": "Intro Archeology",
                    "amount": 1,
                    "fulfilled": False,
                    "classes": {}
                },
                "req2": {
                    "id": 5,
                    "name": "Upper Level or Thematic Course",
                    "amount": 1,
                    "fulfilled": False,
                    "classes": {}
                },
                "req3": {
                    "id": 6,
                    "name": "History of Anthro Theory ",
                    "amount": 1,
                    "fulfilled": False,
                    "classes": {}
                },
                "req4": {
                    "id": 7,
                    "name": "Linguistic or Physical Anthro",
                    "amount": 1,
                    "fulfilled": False,
                    "classes": {}
                },
                "req5": {
                    "id": 8,
                    "name": "Method and Theory In Archeology ",
                    "amount": 1,
                    "fulfilled": False,
                    "classes": {}
                },
                "req6": {
                    "id": 9,
                    "name": "Foreign Lanuguage ",
                    "amount": 4,
                    "fulfilled": False,
                    "classes": {}
                }
            }
        },
        "aoc1": {
            "id": 1,
            "name": "Russian",
            "year": 2019,
            "type": "divisional",
            "requirements": {
                "req0": {
                    "id": 1,
                    "name": "Russian Language",
                    "amount": 6,
                    "fulfilled": False,
                    "classes": {}
                },
                "req1": {
                    "id": 2,
                    "name": "Russian Literature",
                    "amount": 6,
                    "fulfilled": False,
                    "classes": {}
                }
            }
        }
    }

    doubles = {
        "aoc0": {
            "id": 11,
            "name": "Classics",
            "year": 2019,
            "type": "double",
            "requirements": {
                "req0": {
                    "id": 69,
                    "name": "Greek or Latin",
                    "amount": 9,
                    "fulfilled": False,
                    "classes": {}
                },
                "req1": {
                    "id": 70,
                    "name": "Greek and Roman Culture",
                    "amount": 4,
                    "fulfilled": False, "classes": {}
                }
            }
        }
    }

    slashes = {
        "aoc0": {
            "id": 11,
            "name": "Classics",
            "year": 2019,
            "type": "slash",
            "requirements": {
                "req0": {
                    "id": 69,
                    "name": "Greek or Latin",
                    "amount": 9,
                    "fulfilled": False,
                    "classes": {}
                },
                "req1": {
                    "id": 70,
                    "name": "Greek and Roman Culture",
                    "amount": 4,
                    "fulfilled": False, "classes": {}
                }
            }
        }
    }

    return render_template('settings.html',
                           name=name,
                           year=year,
                           aocs=aocs,
                           doubles=doubles,
                           slashes=slashes)


@app.route('/student_dashboard/settings/post', methods=['POST'])
def settings_form_submit():
    if 'google_token' not in session:
        return redirect('/login')

    # name = request.form['name']
    # year = request.form['year']

    return redirect('/student_dashboard/settings')


@app.route('/student_dashboard/courses')
def my_courses():
    if 'google_token' not in session:
        return redirect('/login')

    courses = {
        'COURSE0' : {
            'name' : 'course0',
            'year' : 2018,
            'id' : 327678,
            'semester' : 'Fall'
        },
        'COURSE1' : {
            'name' : 'course1',
            'year' : 2017,
            'id' : 345890,
            'semester' : 'Spring'
        }
    }

    courses = json.dumps(courses)

    return render_template('courses.html',
                           courses=courses)



@app.route('/student_dashboard/explore')
def explore():
    if 'google_token' not in session:
        return redirect('/login')
    return render_template('explore.html')


@app.route('/student_dashboard/explore_results', methods=['GET', 'POST'])
def explore_results():
    if 'google_token' not in session:
        return redirect('/login')

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


@app.route('/removecourse', methods=['POST'])
def remove_course():

    # remove from db
    course = request.form['id']
    print(course)

    return "Successfully removed course " + course


@app.route('/removeaoi', methods=['POST'])
def remove_aoi():

    aoi = request.form['id']

    return "Successfully removed AOI " + aoi


@app.route('/addcourse', methods=['POST'])
def add_course():

    course = request.form['id']

    return "Successfully added course " + course


@app.route('/addaoi', methods=['POST'])
def add_aoi():

    aoi = request.form['id']

    return "Successfully add AOI " + aoi


@app.route('/admin')
def admin():

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
