from flask import Flask
import crud


app = Flask(__name__)


@app.route('/')
def hello_world():
    return "<p>Hello world!</p>"


@app.route('/api/create/<string:room_id>')
def create_room(room_id):
    pass


if __name__ == '__main__':
    app.run('0.0.0.0')
