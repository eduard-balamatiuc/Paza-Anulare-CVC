import sqlite3
import random
import string
import threading

mutex = threading.Lock()

def request(function):
    def wrapper(*args):
        mutex.acquire()
        result = function(*args)
        mutex.release()
        return result
    return wrapper

@request
def loginServer(email, password):
    print('Start connection...')
    db = sqlite3.connect('test.db')
    cursor = db.cursor()
    print('Connection started successfully...')

    cursor.execute(
        f'SELECT * FROM users WHERE email="{email}" AND password="{password}"')
    result = cursor.fetchall()

    if result == []:
        db.commit()
        db.close()
        print('Wrong email')
        print('Connection closed')
        return []

    print('Successfull login')
    print('Loading localSettings...')
    id = result[0][0]

    cursor.execute(
        f'SELECT cameraAllowed, dataAllowed FROM localSettings WHERE idUser={id}')
    result = cursor.fetchall()[0]
    preferences = list(result)
    print('Loaded')

    db.commit()
    db.close()
    print('Connection closed')

    return id, preferences

@request
def registerServer(name, email, password, image):
    print('Start connection...')
    db = sqlite3.connect('test.db')
    cursor = db.cursor()
    print('Connection started successfully...')

    cursor.execute(f'SELECT * FROM users WHERE email="{email}";')

    if cursor.fetchall() != []:
        db.commit()
        db.close()
        print('Wrong email')
        print('Connection closed')
        return []

    print('Loading data...')

    cursor.execute('INSERT INTO users(name, email, password, photo) VALUES (?, ?, ?, ?);',
                   (name, email, password, image))
    print('Data loaded')

    cursor.execute(f'SELECT idUser FROM users WHERE email="{email}";')
    idUser = cursor.fetchall()[0][0]
    print('Loading localSettings...')

    cursor.execute('INSERT INTO localSettings VALUES (?,?,?,?,?,?,?,?,?,?);', (idUser, 0, 0, 0, 0, 0, 0, 0, 0, 0))
    print('LocalSettings loaded')

    print('Insert false collab')
    cursor.execute(f'INSERT INTO collab VALUES (?, ?);', (idUser, idUser))
    print('Inserted')

    db.commit()
    db.close()
    print('Connection closed')
    return idUser

@request
def changePasswordServer(email, password):
    print('Start connection...')
    db = sqlite3.connect('test.db')
    cursor = db.cursor()
    print('Connection started successfully...')

    cursor.execute(f'SELECT * FROM users WHERE email="{email}";')
    result = cursor.fetchall()
    if result == []:
        db.commit()
        db.close()
        print('Wrong email')
        print('Connection closed')
        return []

    print('Loading new Password...')
    cursor.execute(
        f'UPDATE users SET password="{password}" WHERE email="{email}";')

    print('Password loaded')
    db.commit()
    db.close()
    print('Connection closed')

    return result[0][0]

@request
def allowCameraServer(id):
    print('Start connection...')
    db = sqlite3.connect('test.db')
    cursor = db.cursor()
    print('Connection started successfully...')

    print('Loading localSettings...')
    cursor.execute(f'UPDATE localSettings SET cameraAllowed=1 WHERE idUser={id}')
    print('Loaded')

    db.commit()
    db.close()
    print('Connection closed')

@request
def allowDataServer(id):
    print('Start connection...')
    db = sqlite3.connect('test.db')
    cursor = db.cursor()
    print('Connection started successfully...')

    print('Loading localSettings...')
    cursor.execute(f'UPDATE localSettings SET dataAllowed=1 WHERE idUser={id}')
    print('Loaded')

    db.commit()
    db.close()
    print('Connection closed')

@request
def getPreferencesServer(id):
    print('Start connection...')
    db = sqlite3.connect('test.db')
    cursor = db.cursor()
    print('Connection started successfully...')

    print('Loading preferences...')
    cursor.execute(
        f'SELECT cameraAllowed, dataAllowed FROM localSettings WHERE idUser={id}')
    print('Preferences Loaded')
    preferences = cursor.fetchall()[0]

    db.commit()
    db.close()
    print('Connection closed')
    return preferences

@request
def activateServer(id, roomName, admin):
    print('Start connection...')
    db = sqlite3.connect('test.db')
    cursor = db.cursor()
    print('Connection started successfully...')
    print(id, roomName, admin)

    if admin:
        cursor.execute(f'UPDATE Rooms SET active = 1 WHERE idAdmin={id} AND roomName="{roomName}"')
        cursor.execute(f'SELECT idRoom from Rooms WHERE idAdmin={id} AND roomName="{roomName}"')
        idRoom = cursor.fetchall()[0][0]
        cursor.execute(f'UPDATE localSettings SET connected={idRoom} WHERE idUser={id}')
    else:
        cursor.execute(f'SELECT idRoom from Rooms WHERE roomName="{roomName}"')
        idRoom = cursor.fetchall()[0][0]
        cursor.execute(f'UPDATE localSettings SET connected={idRoom} WHERE idUser={id}')
        cursor.execute(f'UPDATE roomsParticipants SET present=1 WHERE idUser={id} AND idRoom={idRoom}')

    db.commit()
    db.close()
    print('Connection closed')
    return idRoom

@request
def getFilesServer(id):
    print('Start connection...')
    db = sqlite3.connect('test.db')
    cursor = db.cursor()
    print('(upload from db) Connection started successfully...')

    cursor.execute(f'SELECT filename, file FROM presentations WHERE idUser={id};')
    print("Done")
    files = cursor.fetchall()

    db.close()
    return files

@request
def loadFilesServer(id, filename, file):
    print('Start connection...')
    db = sqlite3.connect('test.db')
    cursor = db.cursor()
    print('(file insertion) Connection started successfully...')
    cursor.execute(f'SELECT * FROM presentations WHERE fileName="{filename}" AND idUser ={id};')
    print("Done")
    result = cursor.fetchall()
    if result == []:
        cursor.execute(f'INSERT INTO presentations(idUser, fileName, file) VALUES (?, ?, ?);',(id, filename, file))
        print('Inserted file')
    elif result != [] and result[0][2]!=file:
        cursor.execute(f'UPDATE presentations SET file={file} WHERE fileName="{filename}" AND idUser ={id};')
    db.commit()
    db.close()

@request
def deleteFileServer(id, filename, file):
    print('Start connection...')
    db = sqlite3.connect('test.db')
    cursor = db.cursor()
    print('Connection started successfully...')

    cursor.execute(f'DELETE FROM presentations WHERE idUser={id} AND filename="{filename}";')
    print("Done")
    db.commit()
    db.close()

@request
def getCollabsServer(id):
    print('Start connection...')
    db = sqlite3.connect('test.db')
    cursor = db.cursor()
    print('Connection started successfully...')
    print('Loading id of user\'s collabs...')

    print('Loading private info about user\'s collabs')
    cursor.execute(
        f'SELECT name, photo from Users WHERE idUser IN (SELECT idCollab FROM collab WHERE idUser={id})')
    data = cursor.fetchall()
    print('Loaded')

    db.commit()
    db.close()
    print('Connection closed')
    return data

@request
def getRoomsAdminServer(id):
    print('Start connection...')
    db = sqlite3.connect('test.db')
    cursor = db.cursor()
    print('Connection started successfully...')
    print('Loading id of user\'s collabs...')

    print('Loading private info about user\'s collabs')
    cursor.execute(f'SELECT roomName, idAdmin, key from Rooms WHERE idAdmin={id}')
    data = cursor.fetchall()
    rooms = list()
    print('Loaded')
    if len(data):
        for i in range(len(data)):
            cursor.execute(f'SELECT email from Users WHERE idUser={data[i][1]}')
            username = cursor.fetchall()[0][0]
            rooms += [(data[i][0], username, data[i][2])]
    else:
        rooms = []

    db.commit()
    db.close()
    print('Connection closed')
    return rooms

@request
def getRoomsParticipantsServer(id):
    print('Start connection...')
    db = sqlite3.connect('test.db')
    cursor = db.cursor()
    print('Connection started successfully...')
    print('Loading id of user\'s collabs...')

    print('Loading private info about user\'s collabs')
    cursor.execute(f'SELECT roomName, idAdmin FROM Rooms INNER JOIN roomsParticipants ON Rooms.idRoom = '
                   f'roomsParticipants.idRoom WHERE roomsParticipants.idUser = {id}')
    data = cursor.fetchall()

    print('Loaded')
    if len(data):
        cursor.execute(f'SELECT email from Users WHERE idUser={data[0][1]}')
        username = cursor.fetchall()[0][0]
        data = [(data[0][0], username)]
    else:
        data = []
    db.commit()
    db.close()
    print('Connection closed')
    return data

@request
def deleteRoomServer(id, roomName, admin=False):
    print('Start connection...')
    db = sqlite3.connect('test.db')
    cursor = db.cursor()
    print('Connection started successfully...')

    if admin:
        cursor.execute(f'DELETE FROM rooms WHERE roomName="{roomName}" AND idAdmin={id};')
    else:
        cursor.execute(f'SELECT idRoom from Rooms WHERE roomName="{roomName}";')
        idRoom = cursor.fetchall()[0][0]
        cursor.execute(f'DELETE FROM roomsParticipants WHERE idRoom={idRoom} AND idUser={id}')

    print("Done")
    db.commit()
    db.close()

@request
def createRoomServer(id, roomName):
    print('Start connection...')
    db = sqlite3.connect('test.db')
    cursor = db.cursor()
    print('Connection started successfully...')
    print('Searching for the room...')

    cursor.execute(f'SELECT idRoom FROM Rooms WHERE roomName = "{roomName}"')
    idRoom = cursor.fetchall()
    print('Loaded')
    key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
    if not len(idRoom):
        cursor.execute('INSERT INTO Rooms(key, roomName, idAdmin, active) VALUES (?, ?, ?, ?)', (key, roomName, id, 0))
        db.commit()
        db.close()
        return key
    else:
        db.commit()
        db.close()
        return []

@request
def joinRoomServer(id, key):
    print('Start connection...')
    db = sqlite3.connect('test.db')
    cursor = db.cursor()
    print('Connection started successfully...')
    print('Searching for the room...')

    cursor.execute(f'SELECT idRoom FROM Rooms WHERE key = "{key}"')
    idRoom = cursor.fetchall()
    print(idRoom)
    print('Loaded')
    if len(idRoom):
        cursor.execute('INSERT INTO roomsParticipants(idRoom, idUser, present) VALUES (?, ?, ?)', (idRoom[0][0], id, 0))
        print('hero')
        db.commit()
        db.close()
        return True
    else:
        db.commit()
        db.close()
        return False

@request
def getUserDataServer(id):
    print('Start connection...')
    db = sqlite3.connect('test.db')
    cursor = db.cursor()
    print('Connection started successfully...')

    print('Loading data about user...')
    cursor.execute(f'SELECT name, email, photo FROM users WHERE idUser={id};')
    data = cursor.fetchall()[0]
    print('Loaded')

    db.commit()
    db.close()
    print('Connection closed')
    return data

@request
def getSettingsServer(id):
    print('Start connection...')
    db = sqlite3.connect('test.db')
    cursor = db.cursor()
    print('Connection started successfully...')

    print('Loading localSettings about user...')
    cursor.execute(
        f"SELECT translate, attendance, mood, presentation, graph, sport FROM localSettings WHERE idUser={id};")
    options = cursor.fetchall()[0]
    print('Loaded')

    db.commit()
    db.close()
    print('Connection closed')
    return options

@request
def updateSettingsServer(id, settings):
    print('Start connection...')
    db = sqlite3.connect('test.db')
    cursor = db.cursor()
    print('Connection started successfully...')

    print('Loading localSettings from user...')

    cursor.execute(
        f'''UPDATE localSettings SET translate={settings[0]},attendance={settings[1]},mood={settings[2]},presentation={settings[3]},
        graph={settings[4]},sport={settings[5]} WHERE idUser={id}''')
    print('Loaded')

    db.commit()
    db.close()
    print('Connection closed')

@request
def getRoomNameServer(id):
    print('Start connection...')
    db = sqlite3.connect('test.db')
    cursor = db.cursor()
    print('Connection started successfully...')

    cursor.execute(f'SELECT connected from localSettings WHERE idUser="{id}";')
    idRoom = cursor.fetchall()[0][0]
    if idRoom:
        cursor.execute(f'SELECT roomName from Rooms WHERE idRoom="{idRoom}";')
        name = cursor.fetchall()[0][0]
        print("Done")
        db.close()
        return name, idRoom
    else:
        db.close()
        return [[], None]

@request
def leaveRoomServer(id, idRoom):
    print('Start connection...')
    db = sqlite3.connect('test.db')
    cursor = db.cursor()
    print('Connection started successfully...')

    cursor.execute(f'UPDATE localSettings SET connected = 0 WHERE idUser={id};')
    cursor.execute(f'SELECT idAdmin from Rooms WHERE idRoom={idRoom};')
    idAdmin = cursor.fetchall()[0][0]

    if idAdmin == id:
        cursor.execute(f'UPDATE Rooms SET active=0 WHERE idAdmin={id};')
    else:
        cursor.execute(f'UPDATE roomsParticipants SET present=0 WHERE idUser={id} AND idRoom={idRoom};')

    print('Done')
    db.commit()
    db.close()

@request
def isConnectedServer(id):
    print('Start connection...')
    db = sqlite3.connect('test.db')
    cursor = db.cursor()
    print('Connection started successfully...')

    cursor.execute(f'SELECT connected from localSettings WHERE idUser={id};')
    id = cursor.fetchall()[0][0]
    print('Done')
    db.close()

    return id


