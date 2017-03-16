from PIL import Image, ExifTags
import requests
import json


def google_latlng(exif):
    '''由 exif 信息得到 WGS84 经纬度坐标，纬度在前，经度在后'''
    gps_info = exif['GPSInfo']
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


def get_address(location, coordtype='wgs84ll', output='json', ak='v1yu84f4aLIL0em89zmYxRiLydvBqGgw'):
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
        # 如果是直辖市直接将 city 置为空，避免输出重复
        if province == city:
            city = ''
        return country + province + city + district
    return None


def locate(filename):
    '''定位图片拍摄地址
    输入：文件名，
    输出：精确到区的地址'''

    img = Image.open(filename)
    exif = {ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS}

    latlng = google_latlng(exif)

    address = get_address(latlng)
    return address


if __name__ == '__main__':
    print(locate(r'C:\Users\secsi\Pictures\Saved Pictures\9.jpg'))