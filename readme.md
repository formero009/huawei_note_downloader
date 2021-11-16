本爬虫爬取华为目录下的所有备忘录内容
华为备忘录官网地址：
https://cloud.huawei.com/home#/home

要想使用本工具前，需要自行获取华为备忘录的cookie
获取方法见下图：
https://tempt.bj.bcebos.com/111.png?authorization=bce-auth-v1/808a52ca8aa547c6b022debe8abb3d56/2021-11-16T07%3A09%3A59Z/-1/host/402a5857f91d776c2aaf420c0d3e8edb7ffc028662783af0e54a5704b8db5ac6


得到cookie后自行替换脚本中的headers中的Cookie内容，方可使用
脚本运行后，仅会爬取所有备忘录列表中的内容。

备忘录中要是存在图片会自动替换为图片的路径
需要手动根据需要替换为图片的地址。


爬取的结果会存放在D:盘的根目录下  query.txt为获取的所有备忘录目录json
dataFile.txt 存放备忘录中的标题和内容

###