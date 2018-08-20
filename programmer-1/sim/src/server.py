import flask

APPLICATION = flask.Flask(__name__)

@APPLICATION.route('/', methods=['GET'])
def index():
    return flask.render_template('index.html')
