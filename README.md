# ImageMap

## 简介

- 按照地点分类你的照片。
- 显示单个照片的详细地理位置信息。
- ~~在地图上显示你的照片。~~

## 参数

```
Usage: classify.py [OPTIONS]

Options:  
  --class_ / --no-class_  是否分类图片到不同的文件夹，默认为True  
  --imgpath TEXT          存放着图片的目录，同时新的分类目录也将在这个目录下  
  --help                  Show this message and exit.  

```

## 用法

将目录下的图片按地点分类整理：

```bash
python classify.py --class_ --imgpath=your_image_directory
```

`imgpath` 是存放着你将要分类的图片的目录，同时新的分类目录也将在这个目录下。注意路径中不要包含空格，下同。

显示单个图片的详细地理信息：

```bash
python .\classify.py --no-class_ --imgpath=*your_image_full_path*
```

`imgpath` 是你的图片的完整路径。