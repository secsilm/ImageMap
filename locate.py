from PIL import Image, ExifTags
import requests
import json
import sys
import logging
from collections import namedtuple


def get_latlng(exif):
    '''由 exif 信息得到 WGS84 经纬度坐标，纬度在前，经度在后'''
    if 'GPSInfo' in exif and 1 in exif['GPSInfo']:
        gps_info = exif['GPSInfo']
    else:
        logging.error('没有 GPS 信息！')
        return None
    
    first_element = lambda t: t[0]

    # 纬度 latitude
    lat_list = [first_element(t) for t in gps_info[2]]
    lat = lat_list[0] + lat_list[1] / 60 + lat_list[2] / 36000000
    if gps_info[1] == 'S':
        lat = -lat

    # 经度 longitude
    lng_list = [first_element(t) for t in gps_info[4]]
    lng = lng_list[0] + lng_list[1] / 60 + lng_list[2] / 36000000
    if gps_info[3] == 'W':
        lng = -lng
    return str(lat) + ',' + str(lng)


def get_address(location, coordtype='wgs84ll', output='json', ak='v1yu84f4aLIL0em89zmYxRiLydvBqGgw', detail=False):
    '''由坐标得到实际地址，精确到区，输出格式默认为 json'''
    
    geo_url = 'http://api.map.baidu.com/geocoder/v2/?'
    params = {'coordtype': coordtype, 
              'location': location, 
              'output': output,
              'ak': ak}
    res = requests.get(geo_url, params=params)
    res_dict = json.loads(res.text)
    if res_dict['status'] == 0:
        country = res_dict['result']['addressComponent']['country']
        province = res_dict['result']['addressComponent']['province']
        city = res_dict['result']['addressComponent']['city']
        district = res_dict['result']['addressComponent']['district']
        # 百度所使用的 bd09ll 经纬度坐标
        baidu_lat = res_dict['result']['location']['lat']
        baidu_lng = res_dict['result']['location']['lng']
        baidu_latlng = str(baidu_lat) + ',' + str(baidu_lng)
        logging.debug(detail)
        if detail:
            formatted_address = res_dict['result']['formatted_address']
            sematic_description = res_dict['result']['sematic_description']
            return namedtuple('Location', ['country', 'province', 'city', 'district', 'formatted_address', 'sematic_description', 'google_latlng', 'baidu_latlng'])(country, province, city, district, formatted_address, sematic_description, location, baidu_latlng)
        else:
            return namedtuple('Location', ['country', 'province', 'city', 'district', 'google_latlng', 'baidu_latlng'])(country, province, city, district, location, baidu_latlng)
    return None


def locate(filename, detail=False):
    '''定位图片拍摄地址
    输入：文件名，
    输出：精确到区的地址'''

    img = Image.open(filename)
    # 如果没有 _getexif 属性则直接返回 None
    if hasattr(img, '_getexif'):
        if img._getexif() is None:
            logging.error('没有 EXIF 信息！')
            return None
        else:
            exif = {ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS}
    else:
        return None

    latlng = get_latlng(exif)
    logging.debug(detail)
    address = get_address(latlng, detail=detail)

    return address


if __name__ == '__main__':
    print(locate(r'C:\Users\secsi\Pictures\Saved Pictures\图片地图测试\645405576977308572.jpg'))