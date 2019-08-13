## MongoDB实现Q宠大乐斗

```python
 #imp.py文件
 --------------------------
from bson import ObjectId
from pymongo import MongoClient

MC = MongoClient("127.0.0.1",27017,)
MongoDB = MC["Qfight"]#选择一个数据库


def finght_equipment(py1):
    py1_package = py1.get("Package")

    # 攻击者配备装备

    if py1_package:
        choice_one_Equip = random.choice(py1_package)
        py1["Package"].remove(choice_one_Equip)
        py1["ATC"] += choice_one_Equip["act"]
        py1["DEF"] += choice_one_Equip["def"]
        py1["LIFE"] += choice_one_Equip["life"]
        py1["Equip"].append(choice_one_Equip)

----------------------------------------------
 #主文件
from imp import MongoDB
import time,random

#一个开关键表示状态
#   0 ：player2打player1  ,1:player1打player2
dic = {"statu":0}

#记录打斗几个回合
c = {"count":0}

def crit(act):
    """
    暴击伤害 10%触发2倍暴击，20%触发1.5倍暴击
    :param act: 攻击力
    :return: 攻击力*倍数
    """
    timezones = time.time()
    crit_num = int(timezones%5//1)

    if crit_num == 0:
        act = act*2#2倍暴击

    if crit_num == 1 or crit_num == 2:
        act = act*1.5#1.5倍暴击

    return act


def get_blank_log():
    """
    获取战斗日志
    :return: 一个空的战斗日志
    """
    from pymongo import MongoClient

    MC = MongoClient("127.0.0.1", 27017, )
    MongoDB = MC["Qfight"]  # 选择一个数据库
    try:
        fit_log = MongoDB.Player.find_one({'PlayList':["play1","play2"]})
    except Exception:
        fit_log = MongoDB.Player.insert({'PlayList': ["play1", "play2"],"PK_list":[]})

    return fit_log


def finght(play1,play2):
    """
    :param play1: 攻击方
    :param play2: 防御方
    :return: 当一方血量小于等于0，死亡
    """
    c["count"] +=1
    dic["statu"] = 0

    #获取一个战斗日志
    fit_log = get_blank_log()

    #从数据库获取攻击者和防御者
    py1 = MongoDB.Player.find_one({"username":play1})
    py2 = MongoDB.Player.find_one({"username":play2})


    py2_name = py2["username"]
    def finght_equipment(py1):
        """
        :param py1: 攻击者
        :return: 返回带装备攻击者
        """
        py1_package = py1.get("Package")
        py1_name = py1["username"]
        if py1_package:
            choice_one_Equip = random.choice(py1_package)
            py1["Package"].remove(choice_one_Equip)
            py1["ATC"] += choice_one_Equip["act"]
            py1["DEF"] += choice_one_Equip["def"]
            py1["LIFE"] += choice_one_Equip["life"]
            py1["Equip"].append(choice_one_Equip)
        return py1,py1_name


    #返回攻击者对象和攻击者姓名
    py1,py1_name = finght_equipment(py1)

    #随机获取暴击
    atc = crit(py1["ATC"])

    #进行攻击，防御者掉血操作
    if atc > py2["DEF"]:
        atc_life = atc - py2["DEF"]
    else:
        atc_life = 0
    py2["LIFE"] -= atc_life
    if py2["LIFE"] <= 0:
        #打印PK回合数，和获胜者
        print("{}与{}大战了{}回合，{}获得胜利！".format(py1_name,py2_name,c["count"]//2,py1_name))
        py2["LIFE"] = 0
        MongoDB.Player.update({'username':py2_name},{"$set":py2})
        return


    def defense_equipment(py2):
        """
        :param py2: 防御者
        :return: 返回脱下装备的防御者
        """
        py2_Equip = py2.get("Equip")
        if py2_Equip:
            py2_one_Equip = py2_Equip.pop()
            py2["ATC"] -= py2_one_Equip["act"]
            py2["DEF"] -= py2_one_Equip["def"]
            if py2_one_Equip["life"] >= atc_life:
                py2["LIFE"] += atc_life
                py2["LIFE"] -= py2_one_Equip["life"]
            else:
                pass
        return py2

    #获取脱下装备防御者
    py2 = defense_equipment(py2)

    #记录攻击完掉血量记录
    result = "%s atc %s,%s life %s" % (py1_name, py2_name, py2_name, atc_life)
    print(result)

    #生成记录
    one_fit_log = {"atcplayer":play1,"defplayer":play2,"info":result}
    fit_list = fit_log['PK_list']
    fit_list.append(one_fit_log)
    fit_dict = {'PlayList': ["play1", "play2"],"PK_list":fit_list}
    #添加战斗记录
    MongoDB.Player.update({'PlayList':["play1","play2"]},fit_dict)

    #将攻击者，防御者状态记录
    MongoDB.Player.update({"username":py1_name}, {"$set": py1})
    MongoDB.Player.update({"username":py2_name}, {"$set": py2})

    #模拟战斗耗时过程
    time.sleep(random.randint(1,3))

    #递归重新调用，开关控制
    if dic["statu"] == 1:
        finght(py1_name, py2_name)
    else:
        dic["statu"] = 1
        finght(py2_name, py1_name)

#启动函数
finght("player1","player2")
```