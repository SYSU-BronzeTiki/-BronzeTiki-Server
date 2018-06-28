#encoding: utf-8

from model import *
from flask import request, session, redirect, render_template, url_for, jsonify, abort
import json
import hashlib, random, time, os, datetime
from werkzeug.utils import secure_filename

# create data tables
db.create_all()

def register_a_user(username, password, jsonData):
    result = User.query.filter(User.username == username).all()
    if len(result) == 0:
        try:
            md5psw = str(hashlib.md5((salt + password).encode()).digest())
            paypassword = "123456"
            md5paypsw = str(hashlib.md5((paySalt + paypassword).encode()).digest())
            user = User(username=username, password=md5psw, paypassword=md5paypsw)
            db.session.add(user)
            db.session.commit()
            jsonData['message'] = 'Register succeeded'
            return True
        except:
            jsonData['message'] = 'Register failed'
            return False
    else:
        jsonData['message'] = 'Username existed'
        return False

@app.route('/api/users/register', methods=['POST'])
def user_register():
    if request.method == 'POST':
        jsonData = {}
        jsonData['timestamp'] = time.time()
        # print(str(request.form))
        if 'username' not in request.form:
            jsonData['status'] = '0'
            jsonData['message'] = 'No username'
        elif 'password' not in request.form:
            jsonData['status'] = '0'
            jsonData['message'] = 'No password'
        else:
            # validate and register
            if register_a_user(request.form['username'], request.form['password'], jsonData):
                jsonData['status'] = 200
            else:
                jsonData['status'] = 0

        print(str(jsonData))           # debug the message
        message = json.dumps(jsonData) # convert to json
        return message

def login_the_user(username, password, jsonData):
    result = User.query.filter(User.username == username).first()
    md5psw = str(hashlib.md5((salt + password).encode()).digest())
    if result:
        if result.password == md5psw:
            try:
                result = User.query.filter(User.username == username).first()
                jsonData['avatar'] = result.avator
                jsonData['nickname'] = result.nickname
                jsonData['description'] = result.description
                jsonData['money'] = result.money
                jsonData['message'] = 'Login succeeded'
                return True
            except:
                jsonData['message'] = 'Login failed'
                return False
        else:
            jsonData['message'] = 'Invalid password'
            return False
    else:
        jsonData['message'] = 'Invalid username'
        return False

@app.route('/api/users/login', methods=['POST', 'DELETE'])
def user_login():
    # POST
    if request.method == 'POST':
        jsonData = {}
        jsonData['timestamp'] = time.time()

        if 'username' not in request.form:
            jsonData['status'] = '0'
            jsonData['message'] = 'No username'
        elif 'password' not in request.form:
            jsonData['status'] = '0'
            jsonData['message'] = 'No password'
        else:
            # validate and login
            if login_the_user(request.form['username'], request.form['password'], jsonData):
                session['username'] = request.form['username']
                session['avatar'] = jsonData['avatar']
                session['nickname'] = jsonData['nickname']
                session['description'] = jsonData['description']
                session['money'] = jsonData['money']
                session.permanent = True
                # session['uid'] = (random.randint(1000000, 9999999) + (int)(time.time())) % 1000000
                # jsonData['uid'] = session['uid']
                jsonData['status'] = 200
            else:
                jsonData['status'] = 0

        print(str(jsonData))           # debug the message
        message = json.dumps(jsonData) # convert to json
        return message
    # DELETE
    if request.method == 'DELETE':
        jsonData = {}
        jsonData['timestamp'] = time.time()

        if 'username' in session:
            # if request.args.get('logout'):
            session.clear()
            jsonData['message'] = 'Logout succeeded'
            jsonData['status'] = 200
        else:
            jsonData['message'] = 'Logout failed'
            jsonData['status'] = 0

        print(str(jsonData))           # debug the message
        message = json.dumps(jsonData) # convert to json
        return message


@app.route('/api/state', methods=['GET', 'POST'])
def state():
    jsonData = {}
    jsonData['timestamp'] = time.time()
    if 'username' not in session:
        jsonData['message'] = 'Offline'
        jsonData['status'] = 0
    elif 'username' in session:
        # jsonData['uid'] = jsonData['uid']
        jsonData['username'] = session.get('username', 'none')
        jsonData['avatar'] = session.get('avatar', 'none')
        jsonData['nickname'] = session.get('nickname', 'none')
        jsonData['description'] = session.get('description', 'none')
        jsonData['money'] = session.get('money', 'none')
        jsonData['message'] = 'Online'
        jsonData['status'] = 200
    print(str(jsonData))           # debug the message
    message = json.dumps(jsonData) # convert to json
    return message

def change_the_password(username, oldpassword, password, jsonData):
    result = User.query.filter(User.username == username).first()
    md5oldpsw = str(hashlib.md5((salt + oldpassword).encode()).digest())
    md5psw = str(hashlib.md5((salt + password).encode()).digest())
    if result:
        if result.password == md5oldpsw:
            try:
                result.password = md5psw
                db.session.commit()
                jsonData['message'] = 'Change password succeeded'
                return True
            except:
                jsonData['message'] = 'Change password failed'
                return False
        else:
            jsonData['message'] = 'Invalid old password'
            return False
    else:
        jsonData['message'] = 'Invalid username'
        return False

@app.route('/api/users/password', methods=['PATCH'])
def user_password():
    if request.method == 'PATCH':
        jsonData = {}
        jsonData['timestamp'] = time.time()
        
        if 'username' not in request.form:
            jsonData['status'] = '0'
            jsonData['message'] = 'No username'
        elif 'oldPassword' not in request.form:
            jsonData['status'] = '0'
            jsonData['message'] = 'No old password'
        elif 'newPassword' not in request.form:
            jsonData['status'] = '0'
            jsonData['message'] = 'No new password'
        else:
            # validate and change
            if change_the_password(request.form['username'], request.form['oldPassword'], request.form['newPassword'], jsonData):
                jsonData['status'] = 200
            else:
                jsonData['status'] = 0

        print(str(jsonData))           # debug the message
        message = json.dumps(jsonData) # convert to json
        return message

@app.route('/api/users/avatar', methods=['POST'])
def user_avatar():
    if request.method == 'POST':
        jsonData = {}
        jsonData['timestamp'] = time.time()
        
        if 'file' not in request.files:
            jsonData['message'] = 'No file part'
            jsonData['status'] = 0
        elif 'username' not in session:
            jsonData['status'] = 0
            jsonData['message'] = 'Offline'
        else:
            f = request.files['file']
            if f.filename == '':
                jsonData['message'] = 'Empty file'
                jsonData['status'] = 0
            else:
                diffStr = session.get('username', 'none')
                prefStr = str(hashlib.md5(diffStr.encode()).digest()[:10])
                filename = secure_filename(prefStr + f.filename)
                basePath = os.path.dirname(__file__)
                uploadPath = os.path.join(basePath, 'dist/static/img', filename)
                f.save(uploadPath)
                jsonData['avatar'] = '/static/img/' + filename
                jsonData['message'] = 'Upload-file succeed'
                jsonData['status'] = 200
                try:
                    result = User.query.filter(User.username == diffStr).first()
                    result.avator = '/static/img/' + filename
                    db.session.commit()
                except:
                    jsonData['message'] = 'Upload-file fail'
                    jsonData['status'] = 0

        print(str(jsonData))           # debug the message
        message = json.dumps(jsonData) # convert to json
        return message

@app.route('/api/users/nicknameAndDescription', methods=['PATCH'])
def user_nicknameAndDescription():
    if request.method == 'PATCH':
        jsonData = {}
        jsonData['timestamp'] = time.time()
        
        if 'nickname' not in request.form:
            jsonData['status'] = '0'
            jsonData['message'] = 'No nickname'
        elif 'description' not in request.form:
            jsonData['status'] = '0'
            jsonData['message'] = 'No description'
        elif 'username' not in session:
            jsonData['status'] = 0
            jsonData['message'] = 'Offline'
        else:
            # change
            try:
                username = session.get('username', 'none')
                result = User.query.filter(User.username == username).first()
                result.nickname = request.form['nickname']
                result.description = request.form['description']
                db.session.commit()
                jsonData['message'] = 'Update succeed'
                jsonData['status'] = 0
            except:
                jsonData['message'] = 'Update fail'
                jsonData['status'] = 0

        print(str(jsonData))           # debug the message
        message = json.dumps(jsonData) # convert to json
        return message

@app.route('/api/movies', methods=['GET'])
def movies():
    if request.method == 'GET':
        jsonData = {}
        jsonData['timestamp'] = time.time()

        jsonData['ret'] = True
        jsonData['data'] = {}
        movies = []
        for m in Movie.query.filter():
            item = {}
            item['id'] = m.movieID
            item['name'] = m.movieName
            item['poster'] = m.poster
            item['rating'] = m.rating
            item['classsfication'] = m.movieType
            item['primaryActors'] = m.primaryActors
            item['duration'] = m.duration
            item['showtime'] = str(m.showtime)
            item['description'] = m.description
            item['status'] = m.isOnShow
            movies.append(item)
            # id: 电影标识
            # poster： 海报的url
            # rating: 评分（0-5）
            # classsfication: 电影的分类，可以直接用string，也可以用数组
            # primaryActors: 电影的演员
            # duration: 电影时长，min为单位
            # showtime: 在大陆开始上映时间（可有可无的字段）
            # description: 电影简介
            # status: 电影是否在上映期间
        jsonData['data']['movies'] = movies
        jsonData['status'] = 200
        jsonData['message'] = 'movies succeeded'

        print(str(jsonData))           # debug the message
        message = json.dumps(jsonData) # convert to json
        return message

@app.route('/api/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    if request.method == 'GET':
        jsonData = {}
        jsonData['timestamp'] = time.time()

        jsonData['ret'] = True
        jsonData['data'] = {}
        result = Movie.query.filter(Movie.movieID == movie_id).first()
        if result:
            jsonData['data']['id'] = result.movieID
            jsonData['data']['name'] = result.movieName
            jsonData['data']['poster'] = result.poster
            jsonData['data']['rating'] = result.rating
            jsonData['data']['classsfication'] = result.movieType
            jsonData['data']['primaryActors'] = result.primaryActors
            jsonData['data']['duration'] = result.duration
            jsonData['data']['showtime'] = str(result.showtime)
            jsonData['data']['description'] = result.description
            jsonData['data']['status'] = result.isOnShow
            jsonData['message'] = 'movie found'
            jsonData['status'] = 200
            # id: 电影标识
            # poster： 海报的url
            # rating: 评分（0-5）
            # classsfication: 电影的分类，可以直接用string，也可以用数组
            # primaryActors: 电影的演员
            # duration: 电影时长，min为单位
            # showtime: 在大陆开始上映时间（可有可无的字段）
            # description: 电影简介
            # status: 电影是否在上映期间
        else:
            jsonData['message'] = 'movie not found'
            jsonData['status'] = 0

        print(str(jsonData))           # debug the message
        message = json.dumps(jsonData) # convert to json
        return message

@app.route('/api/screens/<int:movie_id>', methods=['GET'])
def get_screen(movie_id):
    if request.method == 'GET':
        jsonData = {}
        jsonData['timestamp'] = time.time()

        jsonData['ret'] = True
        jsonData['data'] = {}
        result = Movie.query.filter(Movie.movieID == movie_id).first()
        jsonData['data']['movieId'] = result.movieID
        jsonData['data']['movieName'] = result.movieName
        jsonData['data']['poster'] = result.poster
        selections = {}
        for s in Screen.query.filter(Screen.movieID == movie_id):
            item = {}
            item['screenId'] = s.screenID
            item['begin'] = str(s.beginTime)
            item['end'] = str(s.beginTime + datetime.timedelta(minutes=result.duration))
            item['hall'] = s.movieHallID
            item['price'] = s.ticketPrice
            item['rest'] = s.rest
            if str(s.beginTime.date()) in selections.keys():
                selections[str(s.beginTime.date())].append(item)
            else:
                selections[str(s.beginTime.date())] = []
                selections[str(s.beginTime.date())].append(item)

        jsonData['data']['selections'] = []
        for k, v in selections.items():
            item = {}
            item['date'] = k
            item['screens'] = v
            jsonData['data']['selections'].append(item)
        jsonData['message'] = 'screens succeeded'
        jsonData['status'] = 200

        print(str(jsonData))           # debug the message
        message = json.dumps(jsonData) # convert to json
        return message

@app.route('/api/seats/<int:screen_id>', methods=['GET'])
def get_seat(screen_id):
    if request.method == 'GET':
        jsonData = {}
        jsonData['timestamp'] = time.time()

        jsonData['ret'] = True
        jsonData['data'] = {}
        result = Screen.query.filter(Screen.screenID == screen_id).first()
        jsonData['data']['screenId'] = result.screenID
        jsonData['data']['screenDate'] = str(result.beginTime)
        jsonData['data']['screenHall'] = result.movieHallID
        seats = [[0 for i in range(10)] for j in range(10)]
        for s in Seat.query.filter(Seat.screenID == screen_id):
            position = s.position[1:-1].split(',')
            seats[int(position[0])][int(position[1])] = int(s.isAvailable)
        jsonData['data']['seats'] = seats
        jsonData['message'] = 'seats succeeded'
        jsonData['status'] = 200

        print(str(jsonData))           # debug the message
        message = json.dumps(jsonData) # convert to json
        return message

@app.route('/api/orders', methods=['GET', 'POST'])
def orders():
    if request.method == 'POST':
        jsonData = {}
        jsonData['timestamp'] = time.time()

        if 'username' not in session:
            jsonData['status'] = 0
            jsonData['message'] = 'Offline'
        elif 'data' in request.form:
            jsonData['ret'] = True
            jsonData['data'] = {}
            form = json.loads(request.form['data']) 
            # print(str(form))
            result = Screen.query.filter(Screen.screenID == int(form['screenId'])).first()
            # make sure rest is enough
            if result.rest >= len(list(form['seats'])):
                # make sure all the seats is available
                seats = []
                for s in list(form['seats']):
                    s = list(s)
                    pos = '({}, {})'.format(s[0], s[1])
                    seat = Seat.query.filter(Seat.position == pos).first()
                    if seat:
                        if not seat.isAvailable:
                            jsonData['status'] = 0
                            jsonData['message'] = 'seat '+pos+' is unavailable.'
                            
                            print(str(jsonData))           # debug the message
                            message = json.dumps(jsonData) # convert to json
                            return message
                        else:
                            seat.isAvailable = False
                        seats.append(seat)
                
                if len(seats) > 0:
                    total = result.ticketPrice*len(form['seats'])
                    username = session.get('username', 'none')
                    # username = '二狗子'
                    phone = form['phone']
                    order = Order(price=total, username=username, phone=phone)
                    db.session.add(order)
                    db.session.flush()
                    for s in seats:
                        s.orderID = order.orderID
                    result.rest = result.rest - len(seats)
                    db.session.commit()

                    jsonData['data']['orderId'] = order.orderID
                    jsonData['data']['screenId'] = result.screenID
                    jsonData['data']['movieId'] = result.movieID
                    movie = Movie.query.filter(Movie.movieID == result.movieID).first()
                    jsonData['data']['movieName'] = movie.movieName
                    jsonData['data']['movieBegin'] = str(result.beginTime)
                    jsonData['data']['orderBegin'] = str(order.genTime)
                    jsonData['data']['hall'] = result.movieHallID
                    jsonData['data']['seats'] = form['seats']
                    jsonData['data']['phone'] = phone
                    jsonData['data']['total'] = total
                    jsonData['data']['isPayed'] = False

                    jsonData['status'] = 200
                    jsonData['message'] = 'seats succeed'
                else:
                    jsonData['status'] = 0
                    jsonData['message'] = 'seats not available'                    
        else:
            jsonData['status'] = 0
            jsonData['message'] = 'no data'
        
        print(str(jsonData))           # debug the message
        message = json.dumps(jsonData) # convert to json
        return message
    elif request.method == 'GET':
        jsonData = {}
        jsonData['timestamp'] = time.time()

        if 'username' not in session:
            jsonData['status'] = 0
            jsonData['message'] = 'Offline'
        else:
            username = session.get('username', 'none')
            # username = '二狗子'
            orders = Order.query.filter(Order.username == username)
            if len(orders) > 0:
                jsonData['ret'] = True
                jsonData['data'] = {}
                jsonData['data']['orders'] = []
                for o in orders:
                    order = {}
                    order['orderId'] = o.orderID
                    order['phone'] = o.phone
                    order['total'] = o.price
                    order['isPayed'] = False if (o.payTime == None) else True

                    seats = Seat.query.filter(Seat.orderID == o.orderID)
                    order['seats'] = [s.position for s in seats]
                    screenId = seats.first().screenID
                    screen = Screen.query.filter(Screen.screenID == screenId).first()
                    movieId = screen.movieID
                    movie = Movie.query.filter(Movie.movieID == movieId).first()
                    order['movieName'] = movie.movieName
                    order['begin'] = str(screen.beginTime)
                    order['hall'] = str(screen.movieHallID)
                    jsonData['data']['orders'].append(order)
                jsonData['status'] = 200
                jsonData['message'] = 'orders succeed'
            else:
                jsonData['status'] = 0
                jsonData['message'] = 'no order'

        print(str(jsonData))           # debug the message
        message = json.dumps(jsonData) # convert to json
        return message

def check_the_paypassword(username, paypassword, jsonData):
    result = User.query.filter(User.username == username).first()
    md5paypsw = str(hashlib.md5((paySalt + paypassword).encode()).digest())
    if result:
        if result.paypassword == md5paypsw:
            jsonData['message'] = 'correct paypassword'
            return True
        else:
            jsonData['message'] = 'Invalid paypassword'
            return False
    else:
        jsonData['message'] = 'Invalid username'
        return False

@app.route('/api/orders/<int:order_id>', methods=['GET', 'PATCH'])
def get_order(order_id):
    if request.method == 'GET':
        jsonData = {}
        jsonData['timestamp'] = time.time()
        jsonData['ret'] = True
        jsonData['data'] = {}

        order = Order.query.filter(Order.orderID == order_id).first()
        if order:
            jsonData['data']['orderId'] = order.orderID
            jsonData['data']['phone'] = order.phone
            jsonData['data']['total'] = order.price
            jsonData['data']['isPayed'] = False if (order.payTime == None) else True
            try:
                seats = Seat.query.filter(Seat.orderID == order.orderID)
                jsonData['data']['seats'] = [s.position for s in seats]
                screenId = seats.first().screenID
                screen = Screen.query.filter(Screen.screenID == screenId).first()
                movieId = screen.movieID
                movie = Movie.query.filter(Movie.movieID == movieId).first()
                jsonData['data']['movieName'] = movie.movieName
                jsonData['data']['begin'] = str(screen.beginTime)
                jsonData['data']['hall'] = str(screen.movieHallID)
                jsonData['status'] = 200
                jsonData['message'] = 'orders succeed'
            except:
                jsonData['status'] = '0'
                jsonData['message'] = 'order no seat'
        else:
            jsonData['status'] = 0
            jsonData['message'] = 'orderId not found'
        
        print(str(jsonData))           # debug the message
        message = json.dumps(jsonData) # convert to json
        return message
    elif request.method == 'PATCH':
        jsonData = {}
        jsonData['timestamp'] = time.time()
        
        if 'username' not in session:
        # if False:
            jsonData['status'] = '0'
            jsonData['message'] = 'Offline'
        elif 'data' in request.form:
            jsonData['ret'] = True
            jsonData['data'] = {}
            form = json.loads(request.form['data'])            
            # check and update
            username = session.get('username', 'none')
            # username = "二狗子"
            if check_the_paypassword(username, form['password'], jsonData): 
                result = Order.query.filter(Order.orderID == order_id).first()
                if not result.payTime:
                    result.payTime = datetime.datetime.utcnow()
                    db.session.commit()
                    jsonData['data']['orderId'] = order_id
                    jsonData['message'] = 'Update succeed'
                    jsonData['status'] = 200
                else:
                    jsonData['message'] = 'Already payed'
                    jsonData['status'] = 0
            else:
                jsonData['status'] = 0
        else:
            jsonData['status'] = 0
            jsonData['message'] = 'no data'

        print(str(jsonData))           # debug the message
        message = json.dumps(jsonData) # convert to json
        return message

@app.route('/', defaults={'path': ''})  # root dir
@app.route('/<path:path>')              # any path
def front_end(path):
    if not request.headers.get('User-Agent'):
        abort(403)

    paths = path.split('/')
    print([x for x in paths])
    return render_template("index.html")

if __name__ == '__main__':
    debug=True
    app.run(host='0.0.0.0')
