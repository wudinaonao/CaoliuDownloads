import requests
from bs4 import BeautifulSoup as bs
from Tools.GeneralTool import GeneralTool

# # _baseUrl = "https://www.t66y.com/thread0806.php?fid=5&search=&page=1"
# # _baseUrl = "http://www.rmdown.com/link.php?hash=191616ccc5300401f8c4b657b0b26adbdf6497c6d0c"
# _baseUrl = "https://www.t66y.com/htm_data/16/1904/3509200.html"
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36"
# }
# req = requests.get(_baseUrl, headers=headers)
# req.encoding = "gbk"
# # req.encoding = "utf-8"
# # print(req.text)
# soup = bs(req.text, "lxml")
# inputTagList = soup.find_all("input")
# for inputTag in inputTagList:
#     print(inputTag['data-src'])

# reff = ""
# ref = ""
# torrentDownloadUrl = ""
# for inputTag in inputTagList:
#     if inputTag["name"] == "reff":
#         reff = str(inputTag["value"])
#     elif inputTag["name"] == "ref":
#         ref = str(inputTag["value"])
# if reff and ref:
#     torrentDownloadUrl = "http://www.rmdown.com/download.php?reff={0}&ref={1}".format(reff, ref)

# torrentResponse = requests.get(torrentDownloadUrl)
#
# md5 = GeneralTool.computeMD5ByFile(torrentResponse.content)
# metalink = GeneralTool.torrentToMetalink(torrentResponse.content)
# print(md5)
# print(metalink)
#
# a = "a:{a: <10}".format(a="2") + \
#     "b:{b}".format(b="1")
# print(a)

# excludeUrlList = [
#     'read.php?tid=5877',
#     'htm_data/2/1111/30611.html',
#     'htm_data/4/1106/524586.html',
#     'htm_data/4/1206/756654.html',
#     'htm_data/5/1707/2519502.html',
#     'htm_data/5/1106/517566.html',
#     'read.php?tid=5877',
#     'htm_data/16/1106/524942.html',
#     'htm_data/16/1707/2519480.html',
#     'htm_data/16/1110/622028.html',
#     'htm_data/16/1808/344501.html',
#     'htm_data/16/0805/136474.html',
#     'htm_data/16/1109/594741.html',
#     'htm_data/16/1706/2424348.html'
# ]

# excludeUrlList = [
#     'htm_data/16/1106/524942.html',
#     'htm_data/16/1808/344501.html',
#     'htm_data/16/1707/2519480.html',
#     'htm_data/2/1111/30611.html',
#     'htm_data/16/1706/2424348.html',
#     'htm_data/16/1110/622028.html',
#     'htm_data/16/0805/136474.html',
#     'htm_data/16/1109/594741.html',
#     'read.php?tid=5877',
#     'htm_data/4/1106/524586.html',
#     'htm_data/5/1707/2519502.html',
#     'htm_data/5/1106/517566.html',
#     'htm_data/4/1206/756654.html'
# ]

# print(list(set(excludeUrlList)))

import random



def generatorElement():
    bigList = [random.randint(0, 100) for _ in range(random.randint(1000, 100000))]
    print("big list lenght is :{0}".format(len(bigList)))
    for element in bigList:
        yield element

generator = generatorElement()
i = 0
# while True:
#     try:
#         print(generator.__next__())
#         i += 1
#     except StopIteration:
#         print("total print:{0}".format(i))
#         break
for i, element in enumerate(generatorElement()):
    print(i, element)