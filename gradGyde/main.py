from gradGyde import app
from flask import request, session, url_for
from flask_oauthlib.client import OAuth, redirect

oauth = OAuth()
github = oauth.remote_app('github',
	consumer_key='2', #We need to register and obtain our own
    consumer_secret='2', 
    request_token_params={'scope': 'user:email'},
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
	authorize_url='https://github.com/login/oauth/authorize'
	)

@github.tokengetter
def get_github_token(token=None):
	return session.get("github_token")


@app.route('/')
def index():
    return "hello world"

@app.route('/test')
def test():
    return "test"

@app.route('/oauth_test')
def oauth_test():
	return github.authorize(callback=url_for('oauth_github_authorized', 
		next =request.args.get('next') or request.referrer or None))

@app.route('/oauth_github_authorized')
def oauth_github_authorized():
	next_url = request.args.get('next') or url_for('oauth_sucess')
	resp = github.authorized_response()
	if resp is None:
		flash(u'You denied the request to sign in.')
		print('You denied the request to sign in.')
		return redirect(next_url)
	session['github_token'] = (
		resp['oauth_token'],
		resp['oauth_token_secret'])
	session['github_user']=resp['screen_name']
	flash(u'You were signed in as %/' % resp['screen_name'])
	print('You were signed in as %/' % resp['screen_name'])
	return redirect('/oauth_test_success')

@app.route('/oauth_test_success')
def oauth_sucess():
	return "%/ Successfully logged in! Yaaaay!" % resp['screen_name']
