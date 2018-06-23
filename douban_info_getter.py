# from douban_client import DoubanClient
import requests
import pprint

# todo: 需不需要封装成一个类
# 根据电影名字获取相关的电影信息
BASE_API_URL = 'https://api.douban.com'
QUERY_MOVIE_URL = BASE_API_URL + '/v2/movie/search?'
GET_MOVIE_DETAIL_URL = BASE_API_URL + '/v2/movie/subject/'

# 确定是否有该电影
def get_movie_id(movieName):
    query_params = {"q": movieName}
    tmpRes = requests.get(QUERY_MOVIE_URL, params=query_params)
    if tmpRes.status_code == 200:
        queryRes = tmpRes.json()
        # pprint.pprint(queryRes)
        if queryRes['total'] > 0 and queryRes['subjects'][0]['title'] == movieName:
            return str(queryRes['subjects'][0]['id'])
    return -1

def get_cast_name(cast_arr, director_arr):
    namesArr = []
    for actor in cast_arr:
        namesArr.append(actor['name'])
    for director in director_arr:
        namesArr.insert(0, str(director["name"] + "（导演）"))
    return "|".join(namesArr)

def getMovieDetail(movieName):
    tar_movie_id = get_movie_id(movieName)
    finRes = {}
    if tar_movie_id != -1 :
        tmpRes = requests.get(GET_MOVIE_DETAIL_URL + str(tar_movie_id)).json()
        finRes.update({'movieType': '|'.join(tmpRes['genres'])})
        finRes.update({'movieName': tmpRes['title']})
        # poster_url
        finRes.update({'poster': tmpRes['images']['small']})
        # finRes.update({'duration': '|'.join(tmpRes['duration'])})
        finRes.update({'primaryActors': get_cast_name(tmpRes['casts'], tmpRes['directors'])})
        finRes.update({'rating': tmpRes['rating']['average']})
        finRes.update({'description': tmpRes['summary']})
        # pprint.pprint(tmpRes)
    return finRes

# pprint.pprint(getMovieDetail("超时空同居"))

