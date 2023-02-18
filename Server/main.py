from flask import Flask, abort
from markupsafe import escape
from datetime import datetime, timedelta

import crud


app = Flask(__name__)


@app.route('/')
def hello_world():
    return "<p>Hello world!</p>"


@app.route('/api/create/<string:room_id>')
def create_room(room_id):
    room = crud.Room(room_id)
    crud.create(room)
    return f'Room <code>{escape(room_id)}</code> created!'


@app.route('/api/moved/<string:room_id>')
def moved(room_id):
    room = crud.read(room_id)

    if room is None:
        abort(404)

    room.moved()
    crud.update(room)

    return f'Recorded <code>{escape(room_id)}</code> movement!'


@app.route('/api/need_move/<string:room_id>')
def need_move(room_id):
    room = crud.read(room_id)

    if room is None:
        abort(404)

    if datetime.now() - room.last_moved > timedelta(hours=2):
        return 'Need move!'
    else:
        return 'OK!'


if __name__ == '__main__':
    crud.init_db()
    app.run('0.0.0.0')
