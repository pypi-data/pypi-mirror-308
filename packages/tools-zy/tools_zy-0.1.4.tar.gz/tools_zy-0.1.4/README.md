# douyin_image [![Version][version-badge]][version-link] ![MIT License][license-badge]


使用深度学习模型过程中可能会用到的一些工具，比如数据处理相关的复制文件，划分数据集等等。

### 示例

巴拉巴拉巴拉啦

### 使用方式

```
# 划分分类数据集
import tools_zy as tz

img_folder = r"/home/wangzhiyuan/classify/data/rawData"
out_folder = r"/home/wangzhiyuan/classify/data/splitData"
tz.split_classifid_images(img_folder, out_folder, (0.8, 0.2, 0), format=".bmp")
```


### 安装

```
$ pip install tools_zy
```


### License

[MIT](https://github.com/pythonml/douyin_image/blob/master/LICENSE)


[version-badge]:   https://img.shields.io/badge/version-0.1-brightgreen.svg
[version-link]:    https://pypi.python.org/pypi/douyin_image/
[license-badge]:   https://img.shields.io/github/license/pythonml/douyin_image.svg