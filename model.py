#encoding: utf-8

import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__, static_folder='./dist/static', template_folder='./dist')
app.config.from_object(config)
db = SQLAlchemy(app)

salt = "2sjx*7sa8*(0&^@9de2-fd23+fd*/ds"
paySalt = "sd$S#A*%${ds]dddfa}d54789eqw16^&^d<?dss"

# Data table User
# create table user (
#     username varchar(50),
#     password varchar(256),
#     avator BLOB,
#     nickname varchar(50),
#     paypassword varchar(256),
#     description varchar(256),
#     money int,
#     # commentID int,
#     primary key (username)
# )
# alter table user modify column avator varchar(256);
# alter table user alter column money set default 1000;
# alter table user alter column avator set default "/static/img/avatar_2x.png";
# alter table user alter column nickname set default "Tony";
# alter table user alter column description set default "freedom and equality";
# alter table user modify column paypassword varchar(256);
class User(db.Model):
    __tablename__ = 'user'
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(256), nullable=False)
    avator = db.Column(db.String(256), default="/static/img/avatar_2x.png")
    nickname = db.Column(db.String(50), default="Tony")
    paypassword = db.Column(db.String(256))
    description = db.Column(db.String(256), default="freedom and equality")
    money = db.Column(db.Integer, default=1000)
    __table_args__ = {
        "mysql_charset" : "utf8"
    }

# Data table Movie
# create table movie (
#     movieID int,
#     movieName varchar(50),
#     poster varchar(256),
#     primaryActors varchar(256),
#     duration int,
#     movieType varchar(50),
#     description varchar(256),
#     rating int,
#     showtime date,
#     isOnShow boolean,
#     primary key (movieID)
# );
# alter table movie modify column poster varchar(256);
# alter table movie modify column duration int;
# insert into movie (movieName, poster, primaryActors, duration, movieType, description, rating) values ("深海越狱","https://p0.meituan.net/128.180/movie/200526fd0facc141caeef984314f7ef8328722.jpg","深海越狱演员",104,"剧情, 动作, 犯罪", "深海越狱介绍",5);
# insert into movie (movieName, poster, primaryActors, duration, movieType, description, rating) values ("超时空同居","https://p0.meituan.net/148.208/movie/f193e43ca706aa6bc6a26d6f53f0115a5315542.jpg","苏伦(导演) / 雷佳音 / 佟丽娅 / 张衣",101,"喜剧, 爱情, 奇幻","来自2018年谷小焦（佟丽娅 饰）与1999年陆鸣（雷佳音 饰），两人时空重叠意外住在同一个房间。从互相嫌弃到试图“共谋大业”，阴差阳错发生了一系列好笑的事情。乐在其中的两人并不知道操控这一切的神秘人竟是想要去2037年“投机取巧”的2018年的……",4);
# alter table movie add column showtime date;
# alter table movie add column isOnShow boolean;

class Movie(db.Model):
    __tablename__ = 'movie'
    movieID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movieName = db.Column(db.String(50), nullable=False)
    poster = db.Column(db.String(256))
    primaryActors = db.Column(db.String(256))
    duration = db.Column(db.Integer)
    movieType = db.Column(db.String(50))
    description = db.Column(db.String(256))
    rating = db.Column(db.Integer)
    showtime = db.Column(db.Date)
    isOnShow = db.Column(db.Boolean)
    __table_args__ = {
        "mysql_charset" : "utf8"
    }

# Data table Comment
# create table comment (
#     commentID int,
#     time datetime,
#     rating int,
#     description varchar(256),
#     username varchar(50),
#     movieID int,
#     primary key (commentID),
#     foreign key (username) references user(username),
#     foreign key (movieID) references movie(movieID)
# )
class Comment(db.Model):
    __tablename__ = 'comment'
    commentID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    rating = db.Column(db.Integer)
    description = db.Column(db.String(256)),
    username = db.Column(db.String(50), db.ForeignKey('user.username'))
    movieID = db.Column(db.Integer, db.ForeignKey('movie.movieID'))
    __table_args__ = {
        "mysql_charset" : "utf8"
    }


# Data table MovieHall
# create table movieHall(
#     movieHallID int,
#     primary key (movieHallID)
# )
class MovieHall(db.Model):
    __tablename__ = 'movieHall'
    movieHallID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address = db.Column(db.String(256))
    __table_args__ = {
        "mysql_charset" : "utf8"
    }


# Data table Screen
# create table screen (
#     screenID int,
#     beginTime datetime,
#     ticketPrice float,
#     movieHallID int,
#     movieID int,
#     rest int,
#     primary key (screenID),
#     foreign key (movieHallID) references movieHall(movieHallID),
#     foreign key (movieID) references movie(movieID)
# )
# alter table screen modify column ticketPrice float;
# insert into screen (beginTime, ticketPrice, movieHallID, movieID, rest) values ("2018-06-14 08:00:00", 42.00, 4, 2, 20);
# insert into screen (beginTime, ticketPrice, movieHallID, movieID, rest) values ("2018-06-14 12:00:00", 42.00, 4, 2, 0);
class Screen(db.Model):
    __tablename__ = 'screen'
    screenID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    beginTime = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    ticketPrice = db.Column(db.Float)
    movieHallID = db.Column(db.Integer)
    movieID = db.Column(db.Integer)
    rest = db.Column(db.Integer)
    __table_args__ = {
        "mysql_charset" : "utf8"
    }


# Data table Seat
# create table seat (
#     seatID int,
#     isAvailable boolean,
#     screenID int,
#     position varchar(50),
#     orderID int,
#     primary key (seatID),
#     foreign key (screenID) references screen(screenID),
#     foreign key (orderID) references movieorder(orderID)
# )
# alter table seat add column position varchar(50);
# insert into seat (isAvailable, screenID, position) values (1, 1, "(0, 0)");

# alter table seat add column orderID int;
# alter table seat add constraint FK_order foreign key(orderID) references movieorder(orderID);
class Seat(db.Model):
    __tablename__ = 'seat'
    seatID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isAvailable = db.Column(db.Boolean, nullable=False)
    screenID = db.Column(db.Integer, db.ForeignKey('screen.screenID'))
    position = db.Column(db.String(50))
    orderID = db.Column(db.Integer, db.ForeignKey('movieorder.orderID'))
    __table_args__ = {
        "mysql_charset": "utf8"
    }


# Data table MovieOrder 
# create table movieorder (
#     orderID int,
#     genTime datetime,
#     payTime datetime,
#     price int,
#     username varchar(50),
#     phone varchar(32),
#     primary key (orderID),
#     foreign key (username) references user(username)
# )
# alter table movieorder drop column seatID;???
# alter table movieorder add column phone varchar(32);
# alter table movieorder modify column payTime datetime;
class Order(db.Model):
    __tablename__ = 'movieorder'
    orderID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    genTime = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    payTime = db.Column(db.DateTime)
    price = db.Column(db.Integer)
    username = db.Column(db.String(50), db.ForeignKey('user.username'))
    # seatID = db.Column(db.Integer, db.ForeignKey('seat.seatID'))
    phone = db.Column(db.String(32))
    __table_args__ = {
        "mysql_charset": "utf8"
    }

