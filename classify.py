from locate import locate
import os
import logging
import click

@click.command()
@click.option('--imgdir', help='存放着图片的目录，同时新的分类目录也将在这个目录下')

logging.basicConfig(level=logging.ERROR)

# 存放着图片的目录，同时新的分类目录也将在这个目录下
base_path = r'C:\Users\secsi\Pictures\Saved Pictures\图片地图测试'
fileformats = ['jpg', 'jpeg']
it = os.scandir(base_path)
for entry in it:
    if entry.name.split('.')[-1] in fileformats and entry.is_file():
        logging.info(entry.name)
        address = locate(entry.path)
        if address is None:
            logging.warning('{} 未知地点'.format(entry.name))
            unknown_path = os.path.join(base_path, '未知地点')
            os.makedirs(unknown_path, exist_ok=True)
            os.rename(entry.path, os.path.join(unknown_path, entry.name))
            continue
        logging.debug(address)
        if address.province == address.city:
            # 按照国家、省份、城市、区分类，并创建目录 
            path = os.path.join(base_path, address.country, address.city, address.district)
        else:
            path = os.path.join(base_path, address.city, address.district)
        os.makedirs(path, exist_ok=True)
        os.rename(entry.path, os.path.join(path, entry.name))
        print(entry.name, address, path)