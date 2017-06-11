from locate import locate, get_address
import os
import logging
import click
import gmplot
from numpy import mean

logging.basicConfig(level=logging.INFO)


def only_show_address(imgpath, detail=True):
    '''只显示地址信息
    detail: bool, 是否显示详细的地址信息
    '''

    address = locate(imgpath, detail)
    # 用于绘制在地图上的坐标
    lat, lng = address.google_latlng.split(',')
    gmap = gmplot.GoogleMapPlotter(float(lat), float(lng), zoom=15)
    gmap.heatmap([float(lat)], [float(lng)], radius=15, opacity=1)
    gmap.draw('imgmap.html')
    logging.debug('address: {}, detail: {}'.format(address, detail))
    if detail:
        print(imgpath, address.formatted_address, address.sematic_description)
    else:
        print(imgpath, address.formatted_address)


@click.command()
@click.option('--class_/--no-class_', default=True, help='是否分类图片到不同的文件夹，默认为 True')
@click.option('--showmap/--no-showmap', default=True, help='将照片在地图上标注出来，默认为 False')
@click.option('--imgpath', help='存放着图片的目录，同时新的分类目录也将在这个目录下')
def classify(class_, imgpath, showmap):
    if class_ and os.path.isdir(imgpath) and showmap:
        logging.debug('class_: {}, isdir: {}'.format(
            class_, os.path.isdir(imgpath)))
        base_path = imgpath
        fileformats = ['jpg', 'jpeg']

        # 用于绘制在地图上的坐标
        lats = []
        lngs = []
        # 使用 os.scandir() 要比 os.listdir() 更有效率
        it = os.scandir(base_path)
        for entry in it:
            if entry.name.split('.')[-1] in fileformats and entry.is_file():
                logging.info(entry.name)
                address = locate(entry.path)
                # 如果没有得到GPS信息则将其分到未知地点目录
                if address is None:
                    logging.warning('{} 未知地点'.format(entry.name))
                    unknown_path = os.path.join(base_path, '未知地点')
                    os.makedirs(unknown_path, exist_ok=True)
                    os.rename(entry.path, os.path.join(
                        unknown_path, entry.name))
                    continue

                logging.debug(address)

                lat, lng = address.google_latlng.split(',')
                lats.append(float(lat))
                lngs.append(float(lng))

                if address.province == address.city:
                    # 按照国家、省份、城市、区分类，并创建目录
                    path = os.path.join(
                        base_path, address.country, address.city, address.district)
                else:
                    path = os.path.join(
                        base_path, address.city, address.district)
                os.makedirs(path, exist_ok=True)
                os.rename(entry.path, os.path.join(path, entry.name))
                logging.info('entry name: {}, address: {}, path: {}'.format(
                    entry.name, address, path))

        # 去除重复的坐标
        latlng_set = set()
        for i, j in zip(lats, lngs):
            latlng_set.add((i, j))
        lats, lngs = zip(*latlng_set)
        center_lat = (max(lats) + min(lats)) / 2
        center_lng = (max(lngs) + min(lngs)) / 2

        logging.debug('center_lat: {}, center_lng: {}'.format(
            center_lat, center_lng))
        logging.debug('lats: {}, lngs: {}'.format(lats, lngs))

        gmap = gmplot.GoogleMapPlotter(center_lat, center_lng, zoom=10)
        gmap.heatmap(lats, lngs, radius=15, opacity=1, dissipating=True)
        gmap.draw('imgmap.html')
    elif not class_ and os.path.isfile(imgpath):
        logging.debug('class_: {}, isdir: {}'.format(
            class_, os.path.isdir(imgpath)))
        only_show_address(imgpath, detail=True)
    else:
        print('请检查输入的 class_ 和 imgpath 是否匹配！class_ 是 {}，而 imgpath 是 {}'.format(
            class_, imgpath))


if __name__ == '__main__':
    classify()
