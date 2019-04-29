import os
import sys
sys.path.append(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0])


from DBUtils.PooledDB import PooledDB
from DBUtils.PersistentDB import PersistentDB
import pymysql
import traceback
from Config import Config as DataBaseConfig
from Tools.Log import Log as logger

class DBUtil():
    
    
    def __init__(self):
        # create link pool
        self.pool = self.createPool(DataBaseConfig.DATABASE_POOL_TYPE)
        
    def createPool(self, typeName):
        if typeName == "PooledDB":
            pool = PooledDB(creator=pymysql,
                            mincached=DataBaseConfig.MIN_CACHED,
                            maxcached=DataBaseConfig.MAX_CACHED,
                            maxconnections=DataBaseConfig.MAX_CONNECTIONS,
                            maxshared=DataBaseConfig.MAX_SHARED,
                            blocking=True,
                            maxusage=DataBaseConfig.MAX_USAGE,
                            host=DataBaseConfig.DATABASE_HOST,
                            port=int(DataBaseConfig.DATABASE_PORT),
                            user=DataBaseConfig.DATABASE_USERNAME,
                            passwd=DataBaseConfig.DATABASE_PASSWORD,
                            db=DataBaseConfig.DATABASE_NAME,
                            charset="utf8")
        elif typeName == "PersistentDB":
            pool = PersistentDB(creator=pymysql,
                                maxusage=DataBaseConfig.MAX_USAGE,
                                host=DataBaseConfig.DATABASE_HOST,
                                port=int(DataBaseConfig.DATABASE_PORT),
                                user=DataBaseConfig.DATABASE_USERNAME,
                                passwd=DataBaseConfig.DATABASE_PASSWORD,
                                db=DataBaseConfig.DATABASE_NAME,
                                charset="utf8")
        else:
            pool = PooledDB(creator=pymysql,
                            mincached=DataBaseConfig.MIN_CACHED,
                            maxcached=DataBaseConfig.MAX_CACHED,
                            maxconnections=DataBaseConfig.MAX_CONNECTIONS,
                            maxshared=DataBaseConfig.MAX_SHARED,
                            blocking=True,
                            maxusage=DataBaseConfig.MAX_USAGE,
                            host=DataBaseConfig.DATABASE_HOST,
                            port=int(DataBaseConfig.DATABASE_PORT),
                            user=DataBaseConfig.DATABASE_USERNAME,
                            passwd=DataBaseConfig.DATABASE_PASSWORD,
                            db=DataBaseConfig.DATABASE_NAME,
                            charset="utf8")
        return pool
    
    def insert(self, tableName, info):
        '''
        insert data to tabel
        :param tableName:
        :param info: a dictionary
        :return:
        '''
        conn = self.pool.connection()
        cursor = conn.cursor()
        sql = ""
        try:
            columnList = [ column for column in info.keys() ]
            valueList = [ value for value in info.values() ]
            sql = "INSERT INTO {0} ({1}) VALUES ({2})".format(
                tableName,
                ", ".join(columnList),
                ", ".join([ "%s" for _ in range(len(valueList))])
            )
            cursor.execute(sql, valueList)
            conn.commit()
            return True
        except pymysql.err.IntegrityError:
            return True
        except BaseException:
            logger.error(traceback.format_exc())
            logger.error("error sql ---> " + sql)
            return False
        finally:
            cursor.close()
            conn.close()

    def delete(self, tableName, position=None):
        '''
        delete row from table, if position is None, clean table
        :param tableName:
        :param position:    position is a dictionary
        :return:
        '''
        conn = self.pool.connection()
        cursor = conn.cursor()
        sql = ""
        try:
            if position is not None:
                if len(position) == 1:
                    key = [key for key in position.keys()][0]
                    sql = "DELETE FROM " + str(tableName) + " WHERE " + str(key) + " = " + "'" + position[key] + "'"
                else:
                    keys = [key for key in position.keys()]
                    sql = "DELETE FROM " + str(tableName) + " WHERE "
                    for key in keys:
                        sql += str(key) + " = " + "'" + position[key] + "'" + " and "
                    sql = sql[:len(sql) - 5]
            else:
                sql = "TRUNCATE TABLE {0}".format(tableName)
            cursor.execute(sql)
            conn.commit()
            return True
        except BaseException:
            logger.error(traceback.format_exc())
            logger.error("error sql ---> " + sql)
            return False
        finally:
            cursor.close()
            conn.close()
    
    def update(self, tableName, info):
        '''
        指定表名,和更新数据更新表
        更新数据为一个字典,例如:
        {
            "key_values":{"key1":"value1","key2":"value2"...},
            "postions":{"key1":"value1","key2":"value2"...}
        }
        key_values接受多个参数,但是注意该表里是否有该keys
        postions接受多个参数,但是目前判断条件只用and,如果需要or请重写代码

        实例:
            info = {
            "key_values":{
                            "name":"naonao",
                            "age":"23",
                            "date":"940208",
                            "sex":"man"
                        },
            "postions":{
                            "sex":"man",
                            "date":"940208"
                        }
            }
        返回:     True
        '''
        conn = self.pool.connection()
        cursor = conn.cursor()
        sql = ""
        try:
            infoKeyList = [key for key in info['key_values'].keys()]
            infoValueList = [value for value in info['key_values'].values()]
            positionKeyList = [key for key in info['postions'].keys()]
            positionValueList = [value for value in info['postions'].values()]
            
            infoKeyList = list(map(lambda key: key + " = %s", infoKeyList))
            positionKeyList = list(map(lambda key: key + " = %s", positionKeyList))
            sql = "UPDATE {tableName} SET {infoKey} WHERE {positionKey}".format(tableName = tableName,
                                                                                infoKey = ", ".join(infoKeyList),
                                                                                positionKey = " AND ".join(positionKeyList))
            cursor.execute(sql, infoValueList + positionValueList)
            conn.commit()
            return True
        except BaseException:
            logger.error(traceback.format_exc())
            logger.error("error sql ---> " + sql)
            return False
        finally:
            cursor.close()
            conn.close()
            
    def query(self, tableName, position=None):
        '''
        输入表名和位置查询当前行,若位置为空则查询全部.
        如果postion存在key"query_col"则请求选择列
        例如:
        postions = {
                    "query_col":"name"
                    }
        请求name列所有内容

        postions = {
                    "name:"wen lyuzhao",
                    "age":"24"
                    }
        请求name=wen lyuzhao并且age=24的行

        返回格式为一个列表字典,例如:
        [
            {"name":"naonao","name":"mama"}
            ...
        ]
        '''
        conn = self.pool.connection()
        cursor = conn.cursor()
        sql = ""
        try:
            # judge have or not positions key
            if position is not None:
                # has postion
                # get column all values if have "query_col" key
                if "query_col" in position.keys():
                    rows = position["query_col"]
                    sql = "SELECT " + str(rows) + " FROM " + str(tableName)
                else:
                    # has postion
                    sql = "SELECT * FROM " + str(tableName) + " WHERE "
                    for key in position.keys():
                        sql += str(key) + " = " + "'" + str(position[key]) + "'" + " and "
                    sql = sql[:len(sql) - 5]
            else:
                # get all
                sql = "SELECT * FROM " + str(tableName)
            sql += " FOR UPDATE"
            cursor.execute(sql)
            conn.commit()
            resultTupleList = cursor.fetchall()
            resultDictList = []
            for result in resultTupleList:
                resultDict = {}
                resultDict.setdefault("id", result[0])
                resultDict.setdefault("category", result[1])
                resultDict.setdefault("title", result[2])
                resultDict.setdefault("detailsPageUrl", result[3])
                resultDict.setdefault("downloadPageUrl", result[4])
                resultDict.setdefault("torrentDownloadUrl", result[5])
                resultDict.setdefault("savePath", result[6])
                resultDict.setdefault("crawData", result[7])
                resultDict.setdefault("md5", result[8])
                resultDict.setdefault("magnet", result[9])
                resultDict.setdefault("downloaded", result[10])
                resultDictList.append(resultDict)
            return resultDictList
        except BaseException as e:
            logger.error(traceback.format_exc())
            logger.error("error sql ---> " + sql)
            return []
        finally:
            cursor.close()
            conn.close()
            
    def queryIsExist(self, tableName, position):
        '''
        check is exist
        :param table_name:
        :param key:    position condition     --> MD5
        :param value:  position value         --> XXX....
        :return:
        '''
        conn = self.pool.connection()
        # conn.autocommit(1)
        cursor = conn.cursor()
        sql = ""
        try:
            if len(position) == 1:
                key = [key for key in position.keys()][0]
                sql = "SELECT * FROM " + str(tableName) + " WHERE " + str(key) + " = " + "'" + position[key] + "'"
                sql += " FOR UPDATE"
            else:
                keys = [key for key in position.keys()]
                sql = "SELECT * FROM " + str(tableName) + " WHERE "
                for key in keys:
                    sql += str(key) + " = " + "'" + position[key] + "'" + " and "
                sql = sql[:len(sql) - 5]
                sql += " FOR UPDATE"
            # sql = "SELECT * FROM {0} WHERE {1} = '{2}'".format(table_name, key, value)
            cursor.execute(sql)
            conn.commit()
            resultList = cursor.fetchall()
            if len(resultList) != 0:
                return True
            else:
                return False
        except BaseException:
            logger.error(traceback.format_exc())
            logger.error("error sql ---> " + sql)
            return False
        finally:
            cursor.close()
            conn.close()

    def executeCustomSQL(self, sql):
        conn = self.pool.connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            conn.commit()
            return True
        except BaseException:
            logger.error(traceback.format_exc())
            logger.error("error sql ---> " + sql)
            return False
        finally:
            cursor.close()
            conn.close()
if __name__ == '__main__':
    
    database = DBUtil()
    print(database.queryIsExist("Verified", {"md5": "AD27BF22D6F354137A2BE88AD314B475"}))
    pass