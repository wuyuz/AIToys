## MongDB学习和使用



#### 介绍

MongoDB 是一个基于**分布式文件存储的数据库**。由 C++ 语言编写。旨在为 WEB 应用提供可扩展的高性能数据存储解决方案。MongoDB 是一个介于关系数据库和非关系数据库之间的产品，**是非关系数据库**当中功能最丰富，最像关系数据库的。

##### MongoDB与一般关系性数据库的区别？

```
它和我们使用的关系型数据库最大的区别就是约束性,可以说文件型数据库几乎不存在约束性,理论上没有主外键约束,没有存储的数据类型约束等等

关系型数据库中有一个 "表" 的概念,有 "字段" 的概念,有 "数据条目" 的概念，MongoDB中也同样有以上的概念,但是名称发生了一些变化,严格意义上来说,两者的概念即为相似,但又有些出入,不过无所谓,我们就当是以上概念就好啦
```

##### 关系性数据中是以表来记录数据：

![1565602254341](C:\Users\RootUser\Desktop\知识点复习\Django\gif\1565602254341.png)

##### 我们再看一下MongoDB的数据结构:

```json
User = [{
		"name": "武大郎",
		"age": 14,
		"gender": "男",
	},
	{
		"name": "孙悟空",
		"age": 10000,
		"gender": "男",
	}
]
```



#### 安装

下载win版本的安装包，目前已经不支持win版本的了，一路下一步即可，注意点击custom可以自定义安装位置

- 安装完毕之后，会在安装文件下生成两个可执行文件

  ```python
  1、mongo.exe  # 客户端
  2、mongod.exe # 服务端
  ```

- 添加环境变量

  ```
  将安装MongoDB生成的bin目录，添加到环境变量中
  ```

- 在cmd中执行mongod命令报错：因为存储数据的默认文件是在 C:\data\db\；但是默认并不存在，所以需要自己配置路径

  ```python
  mongod --dbpath="D:/data/db"  #配置生成的文件位置在D盘中，会生成300m的文件，注意下次启动会默认还是c盘下的date
  mongod --port   #可指定端口，默认是27017、Mysql是3306、Redis是6379
  mongod --help  #查看帮助
  ```

- 每次启动服务器都要自己定义启动的db文件

  ```shell
  mongod --dbpath="D:/data/db"  #启动服务器
  
  
  mongo   #另一个窗口启动，是哟个mogo可以开启一个客户端
  2019-08-12T02:21:12.548-0700 I CONTROL  [initandlisten]
  >
  
  ```



#### MongoDB的简单使用

- 基本命令

  ```shell
  1、mongo  #启动客户端
  
  2、show databases	#查看当前服务器中的数据库
  > show databases
  admin  0.000GB
  local  0.000GB
  
  3、use dbname	#切换当前使用的数据库，当dbname是不存在的库时，就会新建一个dbname库
  > use local
  switched to db local
  
  4、db		#查看当前使用的数据库 代指当前数据库名；创建表
  > db
  local
  
  5、show tables  #查看当前数据库活动的数据表
  > show tables
  startup_log  #日志表
  
  6、use 不存在的数据库名 居然切换成功了 db 查看到了当前错误的数据库名 ?
  > use test
  switched to db test
  > db
  test  #表示已经创建了一个新的数据库，并处于test库中
  > show databases
  admin  0.000GB
  local  0.000GB  #发现并没有test库，因为现在test库中并没有数据，所以只是存在于内存中的
  
  7、db.users 在一个不知道存在不存在的数据库中创建了一个不知道存在不存在的users表
  > db.users  
  test.users #创建以张users的表
  > show tables
  >       #但是却看不到，因为没有数据，就不会写入文件，所以看不见
  
  ------------------------------------------------
   # 总结
  use dbname 在内存中创建数据库空间  #没有数据只能在内存中，除非有数据
  show databases 查看当前磁盘中的数据库  #只能查看磁盘上的
  db(内存中的).tablename 在内存中创建数据表空间  
  show tables	查看在当前数据库中磁盘上的数据表 #当数据表中存在数据,数据库及数据表均会写入到磁盘中
  ```

  

#### MongoDB的简单使用

- ##### 增

  ```shell
  > show tables
  > 
  > db.users.insert({})  #插入一个空字典
  WriteResult({ "nInserted" : 1 })
  > show tables
  users
  > show databases
  admin  0.000GB
  local  0.000GB
  test   0.000GB  #立即生成库和表
  ```

- ##### 简单查

  ```shell
  > db.users.find()
  { "_id" : ObjectId("5d51377fd705cdf6f3412dee") }
  
  > db.users.insert({name:"Mr.wang"})  #在插入一条数据，然后查询
  WriteResult({ "nInserted" : 1 })
  > db.users.find()
  { "_id" : ObjectId("5d51377fd705cdf6f3412dee") }
  { "_id" : ObjectId("5d51386dd705cdf6f3412def"), "name" : "Mr.wang" }
  ```

  

#### 数据类型

	ObjectID：   Documents 自生成的 _id # 自增ID 全世界唯一的计数ID
	String：     字符串，必须是utf-8
	Boolean：    布尔值，true 或者false (这里有坑哦~在我们大Python中 True False 首字母大写)
	Integer：    整数 (Int32 Int64 你们就知道有个Int就行了,一般我们用Int32)
	Double：     浮点数 (没有float类型,所有小数都是Double)
	Arrays：     数组或者列表，多个值存储到一个键 (list哦,大Python中的List哦)
	Object：     如果你学过Python的话,那么这个概念特别好理解,就是Python中的字典,这个数据类型就是字典
	Null：       空数据类型 , 一个特殊的概念,None Null
	Timestamp：  时间戳
	Date：       存储当前日期或时间unix时间格式 (我们一般不用这个Date类型,时间戳可以秒杀一切时间类型)
	看着挺多的,但是真要是用的话,没那么复杂,很简单的哦


##### Mysql与MongoDB比较：

   Mysql 					MongoDB

​	database				database     数据库
​	Tables					 Collections   数据表
​	Colum					 Field              字段
​	Row						 Documents   记录

- ##### Object ID :

  ```shell
  {"_id" : ObjectId("5b151f8536409809ab2e6b26"),...}
  
      #"5b151f85" 代指的是时间戳,这条数据的产生时间
      #"364098" 代指某台机器的机器码,存储这条数据时的机器编号
      #"09ab" 代指进程ID,多进程存储数据的时候,非常有用的
      #"2e6b26"代指计数器,这里要注意的是,计数器的数字可能会出现重复,不是唯一的，是服务器的上的进程计数
      #以上四种标识符拼凑成世界上唯一的ObjectID
      #只要是支持MongoDB的语言,都会有一个或多个方法,对ObjectID进行转换
      #可以得到以上四种信息
  
   #注意:这个类型是不可以被JSON序列化的,但可以调用str方法
  ```

- ##### String :

  ```shell
  { "_id" : ObjectId("5d51386dd705cdf6f3412def"), "name" : "Mr.wang" } # 支持都是字符串
  ```

- ##### Boolean:

  ```shell
  > db.users.insert({sex:true})
  WriteResult({ "nInserted" : 1 })
  > db.users.find()
  { "_id" : ObjectId("5d513b59d705cdf6f3412df0"), "sex" : true } #支持布尔类型
  ```

- ##### Integer :

  ```shell
  > db.users.insert({age:12})
  WriteResult({ "nInserted" : 1 })
  > db.users.find()
  { "_id" : ObjectId("5d513b9bd705cdf6f3412df1"), "age" : 12 } #支持到整数
  ```

- ##### Double :

  ```shell
  > db.users.insert({money:1.22})
  WriteResult({ "nInserted" : 1 })
  > db.users.find()
  { "_id" : ObjectId("5d513bd7d705cdf6f3412df2"), "money" : 1.22 }  #支持到小数
  ```

- ##### Arrays :

  ```shell
  > db.users.insert({teacher:["Mr.wang","Mrs.Wu"]})
  WriteResult({ "nInserted" : 1 })
  > db.users.find()
  { "_id" : ObjectId("5d513c26d705cdf6f3412df3"), "teacher" : [ "Mr.wang", "Mrs.Wu" ] }
  ```

- ##### Object :

  ```shell
  > db.users.insert({course:{name:"Python",price:"12000"}})
  WriteResult({ "nInserted" : 1 })
  > db.users.find()
  { "_id" : ObjectId("5d513c99d705cdf6f3412df4"), "course" : { "name" : "Python", "price" : "12000" } }  #字典
  
  >db.users.insert({package:[{name:"98k"},{name:"31"}]})
  
  >db.users.find({"_id":ObjectId("5d515df968da7313e10fed46")}) #可通过objectid来查询
  ```

- ##### Null:

  ```shell
  > db.users.insert({course:null})
  WriteResult({ "nInserted" : 1 })
  > db.users.find()
  { "_id" : ObjectId("5d513cdad705cdf6f3412df5"), "course" : null } #支持None Null
  ```

- ##### Timestamp :时间戳

- ##### Date:时间

  ```shell
  >db.users.insert([{datetime:ISODate()}])
  > db.users.find()
  {
  	"_id" : ObjectId("5d51435228159f1e3862957c"),
  	"datetime" : ISODate("2019-08-12T18:45:38.662+08:00")
  }
  ```

  

#### Nosqlboot 软件使用

- 安装，直接点击安装即可，没有其他操作

- 连接和使用：

  ![1565605506346](C:\Users\RootUser\Desktop\知识点复习\Django\gif\1565605506346.png)

- ![1565605981805](C:\Users\RootUser\Desktop\知识点复习\Django\gif\1565605981805.png)



#### MongoDB的高级使用

- #####  增

  ```shell
   1、同时插入多条数据,使用[]
  >db.users.insert([{age:999},{age:222}])  #同时插入两条数据
  
  官方推荐 :
      >db.tablename.insertOne({name:"alexander.dsb.li"}) #增加一条数据
  	>db.tablename.insertMany([{name:"alexander.dsb.li"},{name:"alexander.dsb.li"}]) #增加多条数据
  ```

  

- ##### 删除

  ```shell
  >db.Tables.remove({条件})  #删除所有符合条件的数据
  >db.Tables.remove({})    #删除所有的数据
  
  官方推荐	
      >db.tablename.deleteOne({查询条件})	#删除符合条件的第一条数据
      >db.tablename.deleteMany({查询条件}) #删除所有符合条件的数据
  ```

  #####  

- ##### 改 

  ```shell
  单个字段的修改：
  1、update修改数据，单个字段 进行修改，$set 强制将谋值修改覆盖
  	db.users.update({name:"alexander.dsb.li"},{"$set":{name:"DSB"}})
  	语法：
  		db.tablename.update({查询符合条件的数据},{$修改器:{修改的内容}})
  		修改符合查询条件的第一条数据，可指定multi来多条数据修改
  
  	>db.users.find({name:"Mr.Wang"})
          {
              "_id" : ObjectId("5d51479f28159f1e3862957f"),
              "age" : 999,
              "name" : "Mr.Wang"
          }
  	>db.users.update({name:"Mr.Wang"}, 
          {$set:{name:"wang"}},  # {$set:{name:"wang",gender:1}}, #可强制添加gender属性，没有的话
          { multi: false, upsert: false} #multi:true表示一次修改全部符合要求的值
  	 )
      >db.users.find({name:"wang"})
          {
              "_id" : ObjectId("5d51479f28159f1e3862957f"),
              "age" : 999,
              "name" : "wang"
          }
          
  2、$unset 强制删除一个字段
      >db.users.update({age:999}, 
              {$unset: {gender: 0 }},  #无论写几都会删除gender
              { multi: false, upsert: false}
      	)
      >db.users.find({name:"wang"})
      /* 1 createdAt:2019/8/12 下午7:03:59*/
      {
          "_id" : ObjectId("5d51479f28159f1e3862957f"),
          "age" : 999,
          "name" : "wang"
      },
  
      /* 2 createdAt:2019/8/12 下午7:46:28*/
      {
          "_id" : ObjectId("5d51519428159f1e38629585"),
          "age" : 999,
          "name" : "wang"
      }
      
  3、$inc 引用增加
  	>db.users.update({name:"wang"},{"$inc":{age:1}})
  	>db.users.find({name:"wang"})
  	/* 1 createdAt:2019/8/12 下午7:03:59*/
      {
          "_id" : ObjectId("5d51479f28159f1e3862957f"),
          "age" : 1000,
          "name" : "wang"
      },
  
  官方推荐:
  	>db.tablename.updateOne({},{}) # 修改符合条件的第一条数据
  	>db.tablename.updateMany({},{}) # 修改符合条件的所有数据
  	>db.users.updateMany({},{$set:{$inc:{age:1}}}) #给每个人年纪自增1
  ```

- ##### 针对$array的修改器 以及 $关键字的用法和特殊性

  ```shell
  Array是list 列表类型：
  	list -> append remove pop extends
  	Array -> $push $pull  $pop $pushAll $pullAll
  	
  1、$push 在array中追加数据 
  	>db.users.insert({name:"MJJ",hobby:[1,2,3,4]})
      >db.users.update({name:"MJJ"},{"$push":{"hobby":"抽烟"}}) #追加数据
      >db.users.find({name:"MJJ"})
      {
          "_id" : ObjectId("5d51558a28159f1e38629589"),
          "name" : "MJJ",
          "hobby" : [
              1,
              2,
              3,
              4,
              "抽烟"
          ]
      }
      
      >db.users.update({name:"MJJ"},{"$push":{"hobby":["抽烟","烫头"]}}) #插入一个列表
  
  2、$pushAll 在Array中批量增加数据 [] == list.extends
  	db.users.update({name:"MJJ"},{"$pushAll":{"hobby":["喝酒","烫头"]}})
  	
  3、$pull 删除符合条件的所有元素
  	db.users.update({name:"MJJ"},{"$pull":{"hobby":"烫头"}})
  	
  4、$pop 删除array中第一条或最后一条数据
  	db.users.update({name:"MJJ"},{"$pop":{"hobby":1}}) 正整数为 删除最后一条数据
  	db.users.update({name:"MJJ"},{"$pop":{"hobby":-1}}) 负整数为 删除第一条数据
  	
  5、$pullAll 批量删除符合条件的元素 []
  	db.users.update({name:"MJJ"},{"$pullAll":{"hobby":[3,4,5]}})
  	
  6、$关键字 的特殊用法
  	#储存符合条件的元素下标索引 - 只能存储一层遍历的索引位置
  	$ = 9 #储存符合条件的元素的下标索引
  	>db.users.update({"hobby":10},{"$set":{"hobby.$":0}}) #.$表示前面匹配的的记录的下标
  ```

  

- ##### 查

  ```shell
  1、简单查:
  >db.tablename.find()  #查找当前数据表中的所有数据
  { "_id" : ObjectId("5d50bdd1399ab50efdf765de") }
  { "_id" : ObjectId("5d50be7c399ab50efdf765df"), "name" : "alexander.dsb.li" }
  
  2、高级查:
  db.users.find({age:999})  #查询所有age=999的数据
      >db.users.insert({age:999})
      >db.users.insert({age:999})  # 插入两条
      >db.users.find({age:999})    # 会查询除所有满足条件的数据
      >db.users.insert({age:999,name:"Mr.Wang"})
      /* 1 createdAt:2019/8/12 下午6:53:14*/
      {
          "_id" : ObjectId("5d51451a28159f1e3862957d"),
          "age" : 999
      },
  
      /* 2 createdAt:2019/8/12 下午6:53:14*/
      {
          "_id" : ObjectId("5d51451a28159f1e3862957e"),
          "age" : 999
      }
      /* 3 createdAt:2019/8/12 下午7:03:59*/
      {
          "_id" : ObjectId("5d51479f28159f1e3862957f"),
          "age" : 999,
          "name" : "Mr.Wang"
      }
      
  3、并列条件查询，之前的条件只要符合age=999就会被查询出来，
      >db.users.insert({age:999,name:"Mr.Wang"})   # 这样就只能查出一条数据了
      {
          "_id" : ObjectId("5d51479f28159f1e3862957f"),
          "age" : 999,
          "name" : "Mr.Wang"
      }
      
  4、结合比较符：
  	>db.users.find({age:{"$gt":99},name:"Mr.Wang"})  #age大于99,且名字为wang的
  	{
          "_id" : ObjectId("5d51479f28159f1e3862957f"),
          "age" : 999,
          "name" : "Mr.Wang"
  	}
  	
  	>db.users.find({age:{"$lt":9999}})  #age小于9999
  	>db.users.find({age:{"$lte":9999}})  #age小于等于9999
  	>db.users.find({age:{"$eq":999}})  #等于999
  	
  5、$or  或则条件，注意or后面是列表
  	>db.users.find({"$or":[{age:1000},{name:"Mr.Wang"}]}) #要么age=1000、要么name=wang
  	
  6、$in  包含或者， 同一字段 或者条件 
  	>db.users.find({"age":{"$in":[99,999]}})  #age可不加引号，表示age字段的出现情况
  	
  7、$all 子集包含，子集或者 必须是子集 绝对不可以超集 交集是不可查询的
      >db.users.insert([{hobby:[1,2,3,4,5]}])
      >db.users.find({hobby:[1,2,3,4,5]})  #方式一
      >db.users.find({hobby:{"$all":[5,1,3]}})  #方式二，表示只要包含了[5,3,1]的都符合
      
  8、$and
  	>db.users.find({"$and":[{name:"Mr.Wang"},{age:999}]})  #表示都要满足，和，号用法类似
  
  
  >db.tablename.findOne({}) #查询符合条件的第一条数据
  >db.tablename.find({})  #查询符合条件的所有数据
  ```

  - ##### 数学比较符

    ```shell
    $gt		大于
    $lt		小于
    $gte	大于等于
    $lte	小于等于
    $eq		等于 : 是用在 "并列" "或者" 等条件中
    $ne		不等于 不存在和不等于 都是 不等于
    ```

- ##### 高级查询

  ```shell
  1、可以通过.来深度查询，Object查询时可以直接使用 对象.属性 的方式作为Key
  	#当Array中出现了Object 会自动遍历 Object中的属性 
  	
      >db.users.insert([{package:{"name":"98k"}},{package:[{name:"98k",act:99},{name:"3T",def:99}]}])  #两层都会被查出来，数组的也会被查出来，且是全部数组
  
      >db.users.find({"package.name":"98k"})
      /* 1 createdAt:2019/8/12 下午7:36:12*/
      {
          "_id" : ObjectId("5d514f2c28159f1e38629583"),
          "package" : {
              "name" : "98k"
          }
      },
  
      /* 2 createdAt:2019/8/12 下午7:36:12*/
      {
          "_id" : ObjectId("5d514f2c28159f1e38629584"),
          "package" : [
              {
                  "name" : "98k",
                  "act" : 99
              },
              {
                  "name" : "3T",
                  "def" : 99
              }
          ]
      }
  ```

  

#### 高级函数

​	排序     筛选      跳过
​	sort     limit      skip

- ##### 排序

  ```shell
  >db.users.find({}).sort({age:-1})  #依照age字段进行倒序
  >db.users.find({}).sort({age:1})  #依照age字段进行正序
  ```

- ##### 筛选

  ```shell
  >db.users.find({}).limit(4) #筛选前4条数据
  ```

- ##### 跳过

  ```shell
  >db.users.find({}).skip(3) #跳过前3条数据 显示之后的所有数据
  ```

- ##### 使用三个高级函数连接使用

  ```shell
  三个高级函数的执行顺序：1.排序 2.跳过 3.筛选
  
  	page = 页码 = 1
  	count = 条目 = 2	
  	db.users.find({}).limit(2).skip(2).sort({ age:-1 })
  
   #总结：分页
  	limit = count
  	skip = (page-1) * count
  	db.users.find({}).limit(count).skip((page-1)*count).sort({ age:-1 }) #选筛选多少条数据，跳过多少条，再排序
  ```

  

#### 在Python中使用MongoDB

- ##### 安装pymongo

  ```python
  pip3 install pymongo
  ```

- ##### 简单使用pymongo模块

  ```python
  from pymongo import MongoClient
  from bson import ObjectId
  
  MC = MongoClient("127.0.0.1",27017)
  
  MongoDB = MC["Day93"] # 创建一个新的数据库，且没有生成数据库，因为没有数据
  
   #插入
  res = MongoDB.Users.insert_one({"name":"ywb","age":99}) # 单个插入
  print(res.inserted_id,type(res.inserted_id)) #5d515df968da7313e10fed46 <class 'bson.objectid.ObjectId'>
  
  res = MongoDB.Users.insert_many([{"name":"wang","age":22},{"name":"wu","age":20}]) #多个插入
  print(res.inserted_ids,type(res.inserted_ids))  #注意：这里要加s，因为是list，不会触发每个对象的str，单个就会打印具体指
      [ObjectId('5d5160749d1fec33df7b6400'), ObjectId('5d5160749d1fec33df7b6401')] <class 'list'>
  
   #查询
  res = MongoDB.Users.find_one({"name":"ywb"})
  print(res) #{'_id': ObjectId('5d515df968da7313e10fed46'), 'name': 'ywb', 'age': 99}
  
  res = MongoDB.Users.find_one({"_id":ObjectId("5d515df968da7313e10fed46")})
  print(res) #{'_id': ObjectId('5d515df968da7313e10fed46'), 'name': 'ywb', 'age': 99}
  
  res = MongoDB.Users.find({"name":"ywb"}) # 得到一个生成器
  for raw in res:
      print(raw)
  
   #改
  MongoDB.Users.update_one({},{"$inc":{"age":1}})  # 第一个对象age+1
  MongoDB.Users.update_many({},{"$inc":{"age":1}})  # 第一个对象age+1
  
   #删除
  MongoDB.Users.delete_one({})  # 删除第一条数据，可写入条件
  MongoDB.Users.delete_many({})  # 删除第一条数据，可写入条件
  
   #高级函数
  from pymongo import DESCENDING,ASCENDING  # 正序，倒叙
  res = MongoDB.Users.find({}).skip(2).sort("age",DESCENDING)  # 还可以填-1正序
  for row in res:
      print(row)
  ```

  

#### Flask 和 MongoDB 结合

- 实现登陆注册

  ```python
  from flask import Flask, request, render_template
  from setting import MongoDB
  app = Flask(__name__)
  
  @app.route("/reg",methods=["gEt","pOSt"])
  def reg():
     if request.method == "GET":
         return render_template("reg.html")
     else:
         # username = request.form.get("username")
         # MongoDB.users.insert_one({"username":username})
  
         user_info = request.form.to_dict() #将用户信息转换成字典
         MongoDB.users.insert_one(user_info)  #插入一条数据
  
         return "注册成功"
  
  
  @app.route("/login",methods=["gEt","pOSt"])
  def login():
     if request.method == "GET":
         return render_template("login.html")
     else: 
         res = MongoDB.users.find_one(request.form.to_dict()) #查找数据
         if res:
             return f"登陆成功 {res.get('username')}"
         else:
             return "用户名密码错误"
  
  if __name__ == '__main__':
      app.run("0.0.0.0",9527)
      
   ---------------------------------------------------
   # setting.py文件中
  from pymongo import MongoClient
  MC = MongoClient("127.0.0.1",27017)
  MongoDB = MC["S21DAY93"]
  ```

  