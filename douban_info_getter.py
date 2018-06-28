# from douban_client import DoubanClient
import time
import requests
import pprint

from sqlalchemy import text
from model import db, Movie

# 根据电影名字获取相关的电影信息
# 只需要调用get_movie_detail（）即可

BASE_API_URL = 'https://api.douban.com'
QUERY_MOVIE_URL = BASE_API_URL + '/v2/movie/search?'
GET_MOVIE_DETAIL_URL = BASE_API_URL + '/v2/movie/subject/'
GET_MOVIE_IN_THEATHER_URL = BASE_API_URL + '/v2/movie/in_theaters'
MAX_DESCRIPTION_LENGTH = 256


def get_movie_id(movieName):
    """ 获取电影在豆瓣上的ID, 同时
    Args
        str : movieName
    Retruns
        -1 : 没有这个名字的电影
        ID : 该电影在豆瓣上的ID，用于其他函数
    """
    query_params = {"q": movieName}
    tmpRes = requests.get(QUERY_MOVIE_URL, params=query_params)
    if tmpRes.status_code == 200:
        queryRes = tmpRes.json()
        # pprint.pprint(queryRes)
        if int(queryRes['total']) > 0 and queryRes['subjects'][0]['title'] == movieName:
            return str(queryRes['subjects'][0]['id'])
    return -1


def get_cast_name(cast_arr, director_arr):
    """ 处理主演演员格式
    Args
        array : cast_arr, director_arr
    Retruns
        string:
    """
    namesArr = []
    for actor in cast_arr:
        namesArr.append(actor['name'])
    for director in director_arr:
        namesArr.insert(0, str(director["name"] + "（导演）"))
    return "|".join(namesArr)

def handle_movie_record(tmpRes):
    """
    将豆瓣的返回的电影信息，提取出本地服务器需要的信息
    :param subject:
    :return: db_movie_record
    """
    finRes = {}
    finRes.update({'movieType': '|'.join(tmpRes['genres'])})
    finRes.update({'movieName': tmpRes['title']})
    # poster_url
    finRes.update({'poster': tmpRes['images']['small']})
    # finRes.update({'duration': '|'.join(tmpRes['duration'])})
    finRes.update({'primaryActors': get_cast_name(tmpRes['casts'], tmpRes['directors'])})
    finRes.update({'rating': tmpRes['rating']['average']})
    finRes.update({'description': tmpRes['summary'][: MAX_DESCRIPTION_LENGTH]})
    # finRes.update({'description': tmpRes['summary']})
    return finRes


def get_movie_detail(movieName):
    """根据电影名字返回相应的详细信息
    Args:
        电影名字
    Returns:
        dict 类型：
            如果没有该电影：空dict
            电影存在：返回电影信息,
            example:
            {
                "name": "超时空同居",
                "rating": 5,
                "duration": 101,  // 豆瓣上文档上有，但是返回的结果上没看到
                "poster": "https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2520331478.webp",
                "movieType": "喜剧|爱情|奇幻",
                "primaryActors": "苏伦(导演)/雷佳音/佟丽娅/张衣",
                "description": "来自2018年谷小焦（佟丽娅 饰）与1999年陆鸣（雷佳音 饰），两人时空重叠意外住在同一个。。。
                "showtime": "2018-05-18", // 跟时长一样
              }
    """
    finRes = {}
    tarMovieId = get_movie_id(movieName)
    if tarMovieId != -1 :
        tmpRes = requests.get(GET_MOVIE_DETAIL_URL + str(tarMovieId)).json()
        if len(tmpRes) != 0 :
            finRes = handle_movie_record(tmpRes)
        # pprint.pprint(tmpRes)
    return finRes

def check_movie_conflict(movieName):
    """
    检查该电影是否已经在数据库中
    :param movieName: 
    :return: True -> 已经存在, False -> 不存在
    """
    pass

def init_movie_table():
    """
    从豆瓣网站查询部分电影信息，存储进本地数据库中
    :return: True -> 初始化成功
    """
    # in_theaters_list = []
    tmpRes = requests.get(GET_MOVIE_IN_THEATHER_URL)
    if tmpRes.status_code == 200:
        time.sleep(1)
        queryRes = tmpRes.json()
        # pprint.pprint(queryRes)
        # 电影数目
        n = int(queryRes['total'])
        movies = queryRes['subjects']
        print(movies)
        for movie in movies:
            # in_theaters_list.append(queryRes['subjects']['title'])
            movieName = movie['title']
            movieInfo = get_movie_detail(movieName)
            movieRecord = Movie(**movieInfo)
            isExists = Movie.query.filter_by(movieName=movieName).first() != None
            if isExists:
                print("{0} Alread in database".format(movieName))
                continue
            try:
                db.session.add(movieRecord)
                db.session.commit()
                print(movieRecord.movieName + " " + str(movieRecord.movieID))
            except:
                print(movieRecord.movieName + " Error Occurs !! " )
        return True
    print("fail to get in-theater movies")
    return False


# def fuzzy_search(searchKey):
#     """
#     简化的模糊搜索,根据搜索关键字返回搜索结果列表
#     :param searchKey:
#     :return: 按照匹配程度从高到低排列的搜素结果
#     """
#     movie_list = {}
#     for word in searchKey:
#         # 看是否要修改
#         my_sql = "SELECT * FROM movie WHERE movieName like \'%{0}%\';".format(word)
#         print(my_sql)
#         result = db.engine.execute(text(my_sql))
#         for row in result:
#             matchName = row[0]
#             if matchName in movie_list:
#                 movie_list[matchName] += 1
#             else:
#                 movie_list[matchName] = 1
#     for k in movie_list:
#         print((k, movie_list[k]))
#     total = len(movie_list)
#     sortByVal = sorted(movie_list.items(), key = lambda kv: kv[1])
#     sortByVal.reverse()
#     # print(sortByVal)
#     searchResult = []
#     for i in range(min(total, 10)):
#         target_id = sortByVal[i][0]
#         result = Movie.query.filter(Movie.movieID == target_id).first()
#         # 原地修改会影响上一次的值,每次都应该新建立一个dict
#         data = {}
#         data['id'] = result.movieID
#         data['name'] = result.movieName
#         data['poster'] = result.poster
#         data['rating'] = result.rating
#         data['classfication'] = result.movieType
#         data['primaryActors'] = result.primaryActors
#         data['duration'] = result.duration
#         data['showtime'] = str(result.showtime)
#         data['description'] = result.description
#         searchResult.append(data)
#     return searchResult


if __name__ == "__main__":
    # test the moudule function
    init_movie_table()
    fuzzy_search("阿飞")
# pprint.pprint(getMovieDetail("超时空同居"))