import sqlite3
import datetime


DB_PATH = 'db.sqlite'


class Room:
    def __init__(self, room_id, last_moved=datetime.datetime.now()):
        self.room_id: int = room_id
        self.last_moved: datetime.datetime = last_moved

    def moved(self):
        self.last_moved = datetime.datetime.now()


def init_db():
    with sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS rooms ( id TEXT PRIMARY KEY, last_moved TIMESTAMP );')


def create(room: Room):
    with sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
        result = conn.execute('SELECT id FROM rooms WHERE id=? LIMIT 1', (room.room_id,)).fetchone()

        if result is not None:
            return result[0]

        conn.execute('INSERT INTO rooms (id, last_moved) VALUES (?,?)', (room.room_id, room.last_moved))

    return room.room_id


def read(room_id: str):
    with sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
        result = conn.execute('SELECT last_moved FROM rooms WHERE id=? LIMIT 1', (room_id,)).fetchone()

    return Room(room_id, result[0]) if result is not None else None


def update(room: Room):
    with sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
        conn.execute('UPDATE rooms SET last_moved=? WHERE id=?', (room.last_moved, room.room_id))


def delete(room_id: str):
    with sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
        conn.execute('DELETE FROM rooms WHERE id=?', (room_id,))
