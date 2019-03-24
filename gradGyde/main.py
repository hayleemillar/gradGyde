from gradGyde import app
from flask import jsonify, request, session, url_for
from flask_oauthlib.client import OAuth, redirect
import json

oauth = OAuth()
google = oauth.remote_app('google',
	consumer_key=app.config['GOOGLE_CONS_KEY'], 
    consumer_secret=app.config['GOOGLE_CONS_SECRET'], 
    request_token_params={'scope': 'email'},
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
	authorize_url='https://accounts.google.com/o/oauth2/auth'
	)

@google.tokengetter
def get_google_token(token=None):
	return session.get("google_token")


@app.route('/')
def index():
    return "hello world"

@app.route('/test')
def test():
    return "test"

@app.route('/oauth_test')
def oauth_test():
	return google.authorize(callback=url_for('oauth_google_authorized', 
		_external=True))

@app.route('/authorized/')
def oauth_google_authorized():
	next_url = request.args.get('next') or url_for('oauth_sucess')
	resp = google.authorized_response()
	if resp is None:
		print('You denied the request to sign in.')
		return 'Google denied access. Reason: %s \n Error: %s' %(
			request.args['error_reason'],
			request.args['error_description'])
	session['google_token'] = (
		resp['access_token'], '')
	user_info = google.get('userinfo').data
	session['google_user']= user_info
	session['user_name'] = session['google_user']['email']
	print('You were signed in as %s' % session['user_name'])
	return redirect('/oauth_test_success')

@app.route('/oauth_test_success')
def oauth_sucess():
	return "%s Successfully logged in! Yaaaay!" % session['user_name']
