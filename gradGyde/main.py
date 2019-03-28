from gradGyde import app

@app.route('/')
def index():
    return "hello world"

@app.route('/test')
def test():
    return "test"
