# 离线文件快速检索

我比较喜欢收集资源，手里移动硬盘和可拆卸硬盘有好多，其中存储的文件数量极其庞大。快速定位某个文件在哪个硬盘里的哪个路径下是一件极其困难的事情，因为需要反复地热插拔硬盘并分别进行全盘查找。本工具可以建立硬盘的文件索引，并支持离线情况下进行文件检索。

## 界面

![Snipaste_2023-03-01_15-59-04](http://image.iyzyi.com/img/202303011559044.jpg)

## 使用

先建立相关目录的索引，再进行文件检索。

其他功能可自行探索~

建立索引时可能会有卡顿，后台运行并等待即可。索引6w文件大约用时2分半。

## 下载exe

[Release 文件检索 v1.1](https://github.com/iyzyi/IndexFiles/releases/tag/v1.1)

### 打包exe

`pyinstaller -F -w App.py -i logo.ico`

## TODO

* 更新UI与更新数据线程分离