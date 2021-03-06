# ImageMap

## 简介

- 按照地点分类你的照片。
- 显示单个照片的详细地理位置信息。
- 在地图上标记你的照片。

## 参数

```
Usage: classify.py [OPTIONS]

Options:
  --class_ / --no-class_    是否分类图片到不同的文件夹，默认为 True
  --showmap / --no-showmap  将照片在地图上标注出来，默认为 True
  --imgpath TEXT            存放着图片的目录，同时新的分类目录也将在这个目录下
  --help                    Show this message and exit.

```

## 用法

将目录下的图片按地点分类整理：

```shell
$ python classify.py --class_ --imgpath=your_image_directory
```

`imgpath` 是存放着你将要分类的图片的目录，同时新的分类目录也将在这个目录下。注意路径中不要包含空格，下同。

显示单个图片的详细地理信息：

```shell
$ python classify.py --no-class_ --imgpath=your_image_full_path
```

`imgpath` 是你的图片的完整路径。

默认将会在当前目录下输出 `imgmap.html` 文件，在 Google Map 上标注了照片的位置。

![example](http://i.imgur.com/CeVdfRK.png)

## TODOs

1. 将照片按照类似 Google Photos 的类别分类
2. 可以选择在地图上只显示哪些或者哪个类别的照片
3. marker 换成图片的圆形缩略图，类似 Google MyMap
