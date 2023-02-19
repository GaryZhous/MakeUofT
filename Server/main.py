from flask import Flask, abort, render_template
from markupsafe import escape
from datetime import datetime, timedelta

import crud


app = Flask(__name__)


@app.route('/')
def index():
    room_ids = crud.list_rooms()
    rooms = []
    for _id in room_ids:
        room = crud.read(_id)
        rooms.append((room.room_id, room.need_move(), room.str_timedelta()))

    return render_template('index.html', rooms=rooms)


@app.route('/api')
def api_index():
    return "<p>Welcome to RAPID.</p>"


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

    if room.need_move():
        return 'Need move!'
    else:
        return 'OK!'


@app.route('/api/force_move/<string:room_id>')
def force_move(room_id):
    room = crud.read(room_id)

    if room is None:
        abort(404)

    room.last_moved = datetime.now() - timedelta(hours=3)
    crud.update(room)

    return 'OK!'


if __name__ == '__main__':
    crud.init_db()
    app.run('0.0.0.0', '8080')
