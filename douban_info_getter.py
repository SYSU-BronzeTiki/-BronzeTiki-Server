# from douban_client import DoubanClient
import requests
import pprint

# todo: 需不需要封装成一个类
# 根据电影名字获取相关的电影信息
# 只需要调用get_movie_detail（）即可

BASE_API_URL = 'https://api.douban.com'
QUERY_MOVIE_URL = BASE_API_URL + '/v2/movie/search?'
GET_MOVIE_DETAIL_URL = BASE_API_URL + '/v2/movie/subject/'

def get_movie_id(movieName):
    """ 获取电影在豆瓣上的ID
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
        if queryRes['total'] > 0 and queryRes['subjects'][0]['title'] == movieName:
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


def getMovieDetail(movieName):
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
                "duration": 101,  // 豆瓣上居然没有
                "poster": "https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2520331478.webp",
                "movieType": "喜剧|爱情|奇幻",
                "primaryActors": "苏伦(导演)/雷佳音/佟丽娅/张衣",
                "description": "来自2018年谷小焦（佟丽娅 饰）与1999年陆鸣（雷佳音 饰），两人时空重叠意外住在同一个房间。从互相嫌弃到试图“共谋大业”，阴差阳错发生了一系列好笑的事情。乐在其中的两人并不知道操控这一切的神秘人竟是想要去2037年“投机取巧”的2018年的……",
                "showtime": "2018-05-18",  // 没有
              }
    """
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

