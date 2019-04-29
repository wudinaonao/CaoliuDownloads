
# download config
DOWNLOAD_CATEGORY = [
    "image",
    "video"
]

# video dowload
# BT download category
# 亚洲无码原创区 --- AsianNotMosaic
# 亚洲有码原创区 --- AsianMosaic
# 欧美原创区    --- Europe
# 动漫原创区    --- Anime
# 国产原创区    --- MadeInChina
# 中字原创区    --- ChineseSubtitle
BT_DOWNLOAD_CATEGORY = [
    "AsianNotMosaic",
    # "AsianMosaic",
    # "Europe",
    # "Anime",
    # "MadeInChina",
    # "ChineseSubtitle",
]

# image download
# 达盖尔的旗帜 --- Daguer
IMAGE_DOWNLOAD_CATEGORY = [
    "Daguer"
]

# Save setting
# you can use to absolute path or relative path
# relative path save to current directory
# Linux use to /     example: /home/caoliu
# Windows use to \\  example: d:\\caoliu
SAVE_PATH = "CaoliuDownload"

# Tracking page count
# max value is 100
TRACKING_PAGE_COUNT = 1

# download concurrent count
# Excessive number of concurrency may result in being blocked by the site
# recommend value 4
DOWNLOAD_CONCURRENT_COUNT = 4

# Cookies
# Can be set cookies if blocked by the site
# cookies get by browser
COOKIES = {

}

# connection time out, unit second
TIME_OUT = 30

# Aria2 download config
# use to aria2 download video, you need setting
# host, port, token(is empty if nothing token), link type(default is http)
# if save path is empty, download to aria2 default directory
# directory filling method
# Linux use to /     example: /home/caoliu
# Windows use to \\  example: d:\\caoliu
ARIA2_HOST = ""
ARIA2_PORT = ""
ARIA2_TOKEN = ""
ARIA2_LINK_TYPE = ""
ARIA2_SAVE_PATH = ""

# DataBase Config
DATABASE_HOST = ""
DATABASE_PORT = ""
DATABASE_USERNAME = ""
DATABASE_PASSWORD = ""
DATABASE_NAME = ""
# database connection pool type: PooledDB, PersistentDB
DATABASE_POOL_TYPE = "PersistentDB"
# max number of single connection reuse
MAX_USAGE = 64
# mix cache connection
MIN_CACHED = 8
# max cache connection
MAX_CACHED = 8
# max connection number
MAX_CONNECTIONS = 16
# max share connection number
MAX_SHARED = 16

# Log configure
# The option are GENERAL, DETAILED, ALL
LEVEL = "ALL"
LOG_FILE = "running.log"
