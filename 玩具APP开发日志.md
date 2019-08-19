## 玩具APP开发日志



#### openWindow 打开新窗口

- 之前我们只是单独的使用openWindow打开新窗口：

  ```js
  mui.openWindow({
      url:new-page-url, //新窗口地址
      id:new-page-id,
      styles:{
        top:newpage-top-position,//新页面顶部位置
        bottom:newage-bottom-position,//新页面底部位置
        width:newpage-width,//新页面宽度，默认为100%
        height:newpage-height,//新页面高度，默认为100%
        ......
      },
      extras:{
        .....//自定义扩展参数，可以用来处理页面间传值
      },
      createNew:false,//是否重复创建同样id的webview，默认为false:不重复创建，直接显示
      show:{
        autoShow:true,//页面loaded事件发生后自动显示，默认为true
        aniShow:animationType,//页面显示动画，默认为”slide-in-right“；
        duration:animationTime//页面动画持续时间，Android平台默认100毫秒，iOS平台默认200毫秒；
      },
      waiting:{
        autoShow:true,//自动显示等待框，默认为true
        title:'正在加载...',//等待对话框上显示的提示内容
        options:{
          width:waiting-dialog-widht,//等待框背景区域宽度，默认根据内容自动计算合适宽度
          height:waiting-dialog-height,//等待框背景区域高度，默认根据内容自动计算合适高度
          ......
        }
      }
  })
  ```

- 需要注意的是：我们每一APP都要有自己的阿导航栏，并且index.html是APP的入口页面，所以我们可以把导航栏写在index.html中，那么后面的所有的子窗口都会继承index.html

  ```js
  mui.init({
      subpages:[{  //写在index中得第一个页面，默认打开，后面得子页面都没有创建，除非点击创建
        url:'list.html',  //表示初始化时，index入口页面显示的子页面，除了一些底部固定选项外
        id:'list.html',
        styles:{
          top:'45px',//mui标题栏默认高度为45px；
          bottom:'0px'//默认为0px，可不定义；
        }
      }]
    });
  
  //代码块激活字符:    misubpage
  ```

- extras 传递参数，会给openWindow创建的子窗口传递参数，通过在新窗口创建一个Sdata = plus.webview.currentWebview();来获取传过来的数据

  ```js
  //index.html页面
  		document.getElementById('self').addEventListener('tap', function() {
  			if(window.localStorage.getItem("user_id")) {
  				mui.openWindow({
  					url: "user_info.html",
  					id: "user_info.html",
  					styles: {
  						top: "0px",
  						bottom: "50px"
  					},
  					extras:user_info
  				})
  			} else {
  				mui.openWindow({
  					url: "login.html",
  					id: "login.html",
  					styles: {
  						top: "0px",
  						bottom: "50px"
  					}
  				})
  			}
  		})
  
  //user_info.html页面
  			mui.plusReady(function() {
  				Sdata = plus.webview.currentWebview();//可以获取到传过来的数据.出来
  				document.getElementById("avatar").src = "avatar/" + Sdata.avatar;
  				document.getElementById("username").innerText = Sdata.username;
  				document.getElementById("nickname").innerText = Sdata.nickname;
  			});
  
  ```

  

#### mui.back() 覆盖

- 之前调用mui.back() 会默认返回上一层，那么对于index.html页面来说，如果点击返回键会退出程序，而且有些页面的返回键是不想使用的，比如登陆后... ，且系统的返回键也是触发这个函数

  ```js
  mui.back = function() {
  				mui.toast('再按就给你关掉');
  			};
  ```

  

#### storage 本地储存

- 如果我们登陆成功了，必须进行记录，不然下次打开还有登陆，那么我们是不是应该在login.html页面成功登陆后进行存储，且进行判断是否登陆，来开关登陆页面/用户页面

  ```js
  //login.html
  		document.getElementById('login_btn').addEventListener('tap',function () {
  			    var username = document.getElementById("username").value;
  			    var pwd = document.getElementById("pwd").value;
  			    mui.post(window.serv + '/login',{
  			    		username:username,
  			    		password:hex_md5(pwd)
  			    	},function(data){
  			    		console.log(JSON.stringify(data));
  			    		mui.toast(data.MSG);
  			    		if(data.CODE == 0){
  			    			window.localStorage.setItem("user_id",data.DATA._id);
  			    			mui.openWindow({
  								url: 'user_info.html',
  								id: 'user_info.html',
  								styles:{
  									top:"0px",
  									bottom:"50px"
  								},
  								extras:data.DATA
  							});
  			    		}
  			    	},'json'
  			    );
  			})
  
  //index.html
  		document.getElementById('self').addEventListener('tap', function() {
  			if(window.localStorage.getItem("user_id")) {
  				mui.openWindow({
  					url: "user_info.html",
  					id: "user_info.html",
  					styles: {
  						top: "0px",
  						bottom: "50px"
  					},
  					extras:user_info
  				})
  			} else {
  				mui.openWindow({
  					url: "login.html",
  					id: "login.html",
  					styles: {
  						top: "0px",
  						bottom: "50px"
  					}
  				})
  			}
  		})
  ```

- 怎么注销登陆记录？

  ```js
  //user_info.html			
  	document.getElementById('logout_btn').addEventListener('tap', function() {
  				window.localStorage.removeItem("user_id");
  				mui.openWindow({
  					url: "login.html",
  					id: "login.html",
  					styles: {
  						top: "0px",
  						bottom: "50px"
  					}
  				})
  			});
  ```

- 存在的问题: 关闭APP后，再次打开发现登陆是登陆了，但是没有图片头像、信息，因为没有给服务器索取图片信息

  我们可以定义一个加载事件，自动在进入时去服务器拿

  ```js
  		mui.plusReady(function () {
  			if(window.localStorage.getItem("user_id")){
  				mui.post(window.serv + '/auto_login',{ //window.serv 是在mui.js中写的服务器URL
  						_id:window.localStorage.getItem("user_id")
  				},function(data){ 
  						user_info = data.DATA;
  						// console.log(JSON.stringify(user_info));
  						document.getElementById("count").innerText = user_info.chat.count;
  						create_ws(data.DATA._id);
  					},'json'
  				);
  			}		    
  		}) 
  ```

  对应得后端代码

  ```python
  @user.route('/auto_login', methods=['POST'])
  def auto_login():
      user_info = request.form.to_dict()
      user_info['_id'] = ObjectId(user_info.pop('_id'))
      user_dict = MongoDB.users.find_one(user_info)
      if user_dict:
          user_dict['_id'] = str(user_dict['_id'])
      RET['DATA'] = user_dict
  
      return jsonify(RET)
  ```

  

#### 提取公共部分到mui.js中

- 为了方便我们在子页面使用一些公共多次触发得变量，我们可以在js文件中进行全局加载，因为js文件全部子文件都会加载

  ```js
  window.serv = "http://192.168.11.42:9527";
  window.ws_serv = "ws://192.168.11.42:9528/app/";
  window.image_serv = window.serv + "/get_cover/";
  window.music_serv = window.serv + "/get_music/";
  window.chat_serv = window.serv + "/get_chat/";
  window.qr_serv = window.serv + "/get_qr/";
  ```

  

#### 自定义跨页面事件调度 mui.fire()

- 当我们想要使用其他子页面所创建的数据时，我们该如何获取/处理，其实我们完全可以发送一条指令让该子页面帮我们做了，主要用途是在：使用WebSocket对象时，因为每个APP只能创建一个WebScoket对象，所以我们一些子页面要调用ws对象时，就得拜托 创建了 WebSocket 得页面（这里我们在index.html创建得WebSocket对象，因为默认就加载index.html)

  ```js
  //index.html		
  		mui.plusReady(function () {
  			if(window.localStorage.getItem("user_id")){
  				mui.post(window.serv + '/auto_login',{
  						_id:window.localStorage.getItem("user_id")
  				},function(data){ 
  						user_info = data.DATA;
  						document.getElementById("count").innerText = user_info.chat.count;
  						create_ws(data.DATA._id);  //自动创建ws对象
  					},'json'
  				);
  			}		    
  		}) 
  
  		function create_ws(id) {
  			ws = new WebSocket(window.ws_serv + id);
  			ws.onmessage = function(eventMessage) {
  				var recv_msg = JSON.parse(eventMessage.data);
  				var chat = plus.webview.getWebviewById("chat.html");
  				mui.fire(chat,'add_chat',recv_msg);				
  				console.log(eventMessage.data);
  			};
  			ws.onclose = function() {
  				create_ws(id);
  			}
  		}
  
  		document.addEventListener("send_music", function(event) {
  			var s = JSON.stringify(event.detail);
  			ws.send(s);
  		});
  		
  		document.addEventListener("send_chat", function(event) {
  			var s = JSON.stringify(event.detail);
  			ws.send(s);
  		});
  
  
  //chat.html
  		function create_upload_task(file_path) {
  				// 上传文件~
  				var up = plus.uploader.createUpload(
  					window.serv + "/app_uploader", {},
  					function(upload, status) {
  						if(status == 200) {
  							//发送消息给WebToy
  							//upload.responseText
  							var res = JSON.parse(upload.responseText);
  							var index = plus.webview.getWebviewById("HBuilder");// index.html的默认id时HBuilder
  							mui.fire(index, 'send_chat', { //定义跨页面事件调度，触发index页面的send_chat函数，来发送消息
  								chat: res.DATA.filename,
  								to_user: Sdata.friend_id, 
  								from_user: window.localStorage.getItem("user_id")
  							})
  
  							create_chat(Sdata, file_path, "self")
  
  						}
  					});
  
  				up.addData("user_id", window.localStorage.getItem("user_id"));
  				up.addData("to_user", Sdata.friend_id);
  				up.addFile(file_path, {
  					key: "reco_file"
  				});
  				up.start();//触发up事件
  			}
  ```

  

#### 上传录音文件

- 依旧使用uploader方法，后端进行保存

  ```js
  //recoder.html 进行录音上传
  
  			mui.back = null;
  			var r = null;
  			document.getElementById('speech').addEventListener('hold', function() {
  				r = plus.audio.getRecorder();  // 打开录音
  				r.record({  //设置录音格式，和存储路径
  					format:"amr",
  					filename:"_doc/audio/"
  				},function(s){
  					// 回调函数上传录音
  					console.log(s)
  					uploader_audio(s)  
  				})
  			})
  
  			function uploader_audio(filePath){
  				var uploader = plus.uploader.createUpload(window.serv + '/upload',{method:'post'},function(upload,status){
  					if (status==200) {
  						var res = JSON.parse(upload.responseText);
  						var send_str = {
  							"sender":"app",
  							"receiver":"web",
  							'data':res.filename,
  						}
  						// 使用fire自定义事件,把这个数据发送个index窗口,且那边监听我这得事件,一有就发送
  						var index=plus.webview.getWebviewById('HBuilder') //默认index页面的id是HBuilder
  						mui.fire(index,'send_message',send_str)//跨页面事件调度				
  					} 
  				});
  				uploader.addFile(filePath,{'key':'my_audio'});
  				uploader.start();
  			}
  			document.getElementById('speech').addEventListener('release', function() {
  				r.stop();
  			})
  
  
  //index.html
  			//监听fire事件,fire那边定义了触发这里的send_message函数,那边一触发,就会触发这边的函数
  			document.addEventListener('send_message', function(eventDate) {
  				var send_str = JSON.stringify(eventDate.detail);
  				ws_client.send(send_str);
  			})
  ```

  

#### 使用WebSocket + Flask + MUI 实现多用户语音服务

- 创建webSocket，用于监听客户端的语音转发

  ```python
   #ws.py
  import json
  from flask import Flask,request
  from geventwebsocket.handler import WebSocketHandler
  from geventwebsocket.server import WSGIServer
  from geventwebsocket.websocket import WebSocket
  
  ws_app = Flask(__name__)
  
  user_socket_dict = {}
  @ws_app.route("/app_ws/<user_id>")
  def app_ws(user_id):
      user_socket = request.environ.get('wsgi.websocket') # type:WebSocket
      if user_socket:
          user_socket_dict[user_id] = user_socket  #储存id和socket连接对象
      print(user_socket_dict)
      while 1:
          user_msg=user_socket.receive()
          print(user_msg)
          user_msg_dict = json.loads(user_msg)
          receiver_id = user_msg_dict.get('receiver') # 获取接收者id
          receiver_socket = user_socket_dict.get(receiver_id) #获取到需要接收者对象，给它发送消息
          receiver_socket.send(user_msg)
  
  
  if __name__ == '__main__':
      http_serv = WSGIServer(('0.0.0.0',9528),ws_app,handler_class=WebSocketHandler)
  
      http_serv.serve_forever()
  ```

- Flask 对每个客户端进行支撑

  ```python
   #主文件
  from flask import Flask, request
  from server.file_manager import fm
  from server.users import user
  
  app = Flask(__name__)
  app.register_blueprint(fm)
  app.register_blueprint(user)
  
  if __name__ == '__main__':
      app.run('0.0.0.0',9527)
  
      
   ---------------------------------------------
   #各蓝图文件:fm蓝图问及那，进行文件上传接受
  from flask import Blueprint,request,jsonify,send_file
  from settings import AVATAR_PATH, RECO_PATH
  import os
  
  fm = Blueprint("fm",__name__)
  
  @fm.route("/upload",methods=["POST"])
  def upload(): # 对所有的上传的头像和音频进行保存
      file = request.files.get('avatar')
      if file:
          avatar_file_path = os.path.join(AVATAR_PATH, file.filename)
          file.save(avatar_file_path)
  
      elif not file:
          file = request.files.get('my_audio')
          avatar_file_path = os.path.join(RECO_PATH, file.filename)
          file.save(avatar_file_path)
          os.system(f"ffmpeg -i Reco/{file.filename} Reco/{file.filename[:-4]}.mp3")
          os.remove(f"Reco/{file.filename}")
  
      ret = {
          'code':0,
          'filename':f"{file.filename[:-4]}.mp3",
          'msg':'上传成功'
      }
      return jsonify(ret)
  
  @fm.route("/get_avatar/<filename>",methods=["GET"])
  def get_avatar(filename): #获取头像
      file_path = os.path.join(AVATAR_PATH,filename)
      return send_file(file_path)
  
  
  @fm.route("/get_chat/<filename>",methods=["GET"])
  def get_audio(filename): #获取音频
      file_path = os.path.join(RECO_PATH,filename)
      return send_file(file_path)
  
  
  --------------------------------------------------
   #用户蓝图
  from bson import ObjectId
  from flask import Blueprint,request,jsonify,send_file
  from settings import MongoDB,RET
  
  user = Blueprint("users",__name__)
  
  @user.route('/reg',methods=['POST'])
  def reg():
      user_info = request.form.to_dict()
      print(user_info)
      MongoDB.users.insert_one(user_info)
      user_dict = MongoDB.users.find_one(user_info)
      print(user_dict)
  
      RET['code'] = 0
      RET['msg'] = '注册成功'
      RET['data'] = []
  
      return jsonify(RET)
  
  @user.route("/login",methods=['post'])
  def login():
      user_info = request.form.to_dict()
      user_dict = MongoDB.users.find_one(user_info)
      user_dict['_id'] = str(user_dict.get('_id'))
      if user_dict:
          RET['code'] = 0
          RET['msg'] = '登陆成功'
          RET['data'] = user_dict
          return jsonify(RET)
      else:
          return jsonify({"code":1,'msg':'登陆失败'})
  
  
  @user.route("/auto_login",methods=['post'])
  def auto_login():
      user_info = request.form.to_dict()
      user_info['_id'] = ObjectId(user_info.pop("user_id"))
      user_dict = MongoDB.users.find_one(user_info)
  
      if user_dict:
          user_dict['_id'] = str(user_dict.get('_id'))
          RET['code'] = 0
          RET['msg'] = '登陆成功'
          RET['data'] = user_dict
          return jsonify(RET)
      else:
          return jsonify({"code":1,'msg':'登陆失败'})
  
  --------------------------------------
   #setting.py   
  AVATAR_PATH = "Avatar"
  RECO_PATH = 'Reco'
  
  from pymongo import MongoClient
  MC = MongoClient('127.0.0.1',27017)
  MongoDB = MC['APP']
  
   # 返回协议
  RET = {
      'code':0,
      'msg':'',
      'data':[]
  }
  ```

- 自定义一个消息对象，用于和APP测试，转发

  ```html
  
  </html lang="en">
  <head>
      <meta charset="UTF-8">
      <title>Title</title>
  </head>
  <body>
  <audio id="player" controls autoplay></audio>
  </body>
  <script type="application/javascript">
      var ws_client = new WebSocket("ws://192.168.12.42:9528/app_ws/web");
      ws_client.onmessage = function (eventMessage) {
          console.log(eventMessage);
          var data = JSON.parse(eventMessage.data);
          document.getElementById('player').src = 'http://192.168.12.42:9527/get_chat/'+ data.data;
      }
  </script>
  
  ```

  ##### 结合之前的语音上传，就可以形成一个语音实时对话机制

  

##### 总结

![1565880029831](C:\Users\RootUser\Desktop\知识点复习\Django\gif\1565880029831.png)





2019.3.1

## 正式的开发APP

#### 开发背景

	1.关心照顾孩子
		- 除了父母谁也做不到
		
	2.陪孩子玩儿
		- 高度拟人化
		- 玩具间产生互动
		
	3.解答十万个为什么
		- 从维基百科中获取答案(过滤敏感问题)
					
	4.帮孩子树立小小三观
		- 儿歌 
		
	5.信使服务
		- 增加家长与子女之间的沟通频率
		- App 与 Toy 之间建立实时沟通关系
		- Toy 与 Toy 之间建立实时沟通关系


#### 内容采集

首先我们需要一些儿歌数据，所以必须涉及到内容的采集，这里我们选用去喜马拉雅采集数据

- 访问儿歌 《一千零一夜》的网址，使用request模块，并携带者请求头

  ```python
  import requests
  from Config import COVER_PATH, MUSIC_PATH, MongoDB
  
  header={
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
  }
  
  res = request.get("https://www.ximalaya.com/ertong/424529/",header=header)
  print(res.text,res)
  ```

- 通过播放歌曲，来动态查看播放的数据网址

  ![1565886302148](C:\Users\RootUser\Desktop\知识点复习\Django\gif\1565886302148.png)

  通过第5步，我们可以获得30个播放列表的网址的响应，我们就可以获取里面的数据

- 获取数据，并进行整理，序列化成字典，通过拼接trackCoverpath拼接后得到图片的url；拼接src后得到歌曲的url。

  最后将数据的图片和歌曲名配对存入数据库中

  ```python
  import json
  import os
  from uuid import uuid4
  import requests # 爬虫课程
  from Config import COVER_PATH, MUSIC_PATH, MongoDB
  
  header={
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
  }
  
  DATA = '{"ret":200,"msg":"声音播放数据","data":{"uid":0,"albumId":424529,"sort":1,"pageNum":1,"pageSize":30,"tracksAudioPlay":[{"index":30,"trackId":7713678,"trackName":"新年恰恰","trackUrl":"/ertong/424529/7713678","trackCoverPath":"//imagev2.xmcdn.com/group9/M04/3B/E1/wKgDZlWcvRKwSOIMAAD3201gPxc590.jpg","albumId":424529,"albumName":"【一千零一夜】经典儿歌","albumUrl":"/ertong/424529/","anchorId":9216785,"canPlay":true,"isBaiduMusic":false,"isPaid":false,"duration":92,"src":"https://fdfs.xmcdn.com/group12/M00/3B/B2/wKgDXFWcw12y8TanAAtkIsI9320251.m4a","hasBuy":true,"albumIsSample":false,"sampleDuration":0,"updateTime":"2年前","createTime":"4年前","isLike":false,"isCopyright":true,"firstPlayStatus":true},
  ...
  {"index":1,"trackId":7713643,"trackName":"一双小小手","trackUrl":"/ertong/424529/7713643","trackCoverPath":"//imagev2.xmcdn.com/group9/M04/3B/E1/wKgDZlWcvRKwSOIMAAD3201gPxc590.jpg","albumId":424529,"albumName":"【一千零一夜】经典儿歌","albumUrl":"/ertong/424529/","anchorId":9216785,"canPlay":true,"isBaiduMusic":false,"isPaid":false,"duration":62,"src":"https://fdfs.xmcdn.com/group13/M00/3C/12/wKgDXlWcw5GzJ1NgAAfMZ7UShYY633.m4a","hasBuy":true,"albumIsSample":false,"sampleDuration":0,"updateTime":"2年前","createTime":"4年前","isLike":false,"isCopyright":true,"firstPlayStatus":true}],"hasMore":true}}'
  
  data = json.loads(DATA)  # 转换格式
  audio_list = data["data"]["tracksAudioPlay"]  #获取所有有用的数据，音频连接
  # print(audio_list)
  
  """
  trackName
  trackCoverPath 图片地址 http协议头
  albumName
  src 歌曲内容地址
  """
  
  content_list = []
  
  for content_info in audio_list:
      content = {
          "title":content_info.get("trackName"),
          "zhuanji":content_info.get("albumName"),
          "cover":"",
          "music":"",
      }
  
      file_name = uuid4()
      cover_res = requests.get("http:"+content_info.get("trackCoverPath")) #拼接图片地址
      cover_file_name = f"{file_name}.jpg"  #生成唯一名
      cover_file_path = os.path.join(COVER_PATH,cover_file_name)
      with open(cover_file_path,"wb") as fc :
          fc.write(cover_res.content)
  
      music_res = requests.get(content_info.get("src"))
      music_file_name = f"{file_name}.mp3"
      music_file_path = os.path.join(MUSIC_PATH, music_file_name)
      with open(music_file_path, "wb") as fm:
          fm.write(music_res.content)
  
      # MongoDB 很快 - json存储 - 不用原生sql语句 - 数据存储方便
      # 数据后期 非常方便 - 用户画像(用户的操作日志) == 钱
      content["cover"] = cover_file_name
      content["music"] = music_file_name
  
      content_list.append(content)
  
  MongoDB.Content.insert_many(content_list)
  # 优势 一次数据库操作 即可完成 全部内容添加
  # 劣势 在29个 断掉了 全部结束 Try Exception F
  ```
  

  
- 给后端提供content_list接口，使后端能接受到图片和音频数据名，前端再根据歌名来后端获取

  ```python
  @content.route("/content_list", methods=['POST'])
  def content_list():
      con_list = list(MongoDB.Content.find({}))
      for index, cont in enumerate(con_list):
          con_list[index]['_id'] = str(cont.get('_id'))
  
      RET['CODE'] = 0
      RET['MSG'] = '获取内容列表'
      RET['data'] = con_list
  
      return jsonify(RET)
  
  @content.route("/get_cover/<filename>", methods=['GET'])
  def cover_list(filename):
      file_path = os.path.join(COVER_PATH, filename)
      return send_file(file_path)
  
  
  @content.route("/get_music/<filename>", methods=['GET'])
  def music_list(filename):
      file_path = os.path.join(MUSIC_PATH, filename)
      return send_file(file_path)
  
  ```

- 前端向后端获取音乐

  ```js
  function create_content(content){    //添加儿歌列表
          var li = document.createElement("li");
          li.className = "mui-table-view-cell mui-media";
          var a = document.createElement("a");
          a.onclick = function(){  //点击后跳转新页面
          	mui.openWindow({
          		url:"player.html",
          		id:"player.html",
          		extras:content
          	});
          };
          var img = document.createElement("img");
          img.className = "mui-media-object mui-pull-left";
          img.src = window.image_serv+content.cover;
          var div = document.createElement("div");
          div.className = "mui-media-body";
          div.innerText=content.title;
          var p = document.createElement("p");
          p.className="mui-ellipsis";
          p.innerText = content._id;
          
          li.appendChild(a); 
          a.appendChild(img);
          a.appendChild(div);
          div.appendChild(p);
          
          document.getElementById("content_list").appendChild(li);       
      }
  ```

- 后端生成的二维码，并将二维码存入数据库中

  ```python
  import os
  import requests
  from Config import LT_URL,QRCODE_PATH,MongoDB
  from uuid import uuid4
  import time, hashlib
  
  #创建二维码，设备编号字符串
  
  def create_qr(n):
      device_list = []
      for i in range(n):
          DeviceKey = hashlib.md5(f"{uuid4()}{time.time()}{uuid4()}".encode('utf-8')).hexdigest()
          res = requests.get(LT_URL%(DeviceKey))
          qr_name = f"{DeviceKey}.jpg"
          qr_file_path = os.path.join(QRCODE_PATH,qr_name)
  
          with open(qr_file_path,'wb') as f:
              f.write(res.content)
  
          device_key = {
              "device_key":DeviceKey
          }
  
          device_list.append(device_key)
      #存放在数据库中
      MongoDB.devices.insert(device_list)
  
  create_qr(5)
  ```



#### 扫描二维码

- 前端通过toy_info.html文件打开新窗口

  ```js
  			document.getElementById('add_fri').addEventListener('tap',function () {
  			     	mui.openWindow({
  						url: "scan.html",
  						id: "scan.html",
  						extras:{type:"toy",create_toy_id:Sdata._id}
  					});
  			})
  ```

- scan.html通过调用`plus.barcode.Barcode("bcid")`开启二维码扫描，并上传、执行回调

  ```js
  			var Sdata = null;
  			function onmarked(type, result) {
  				console.log(result);
  			
  				mui.post(window.serv + '/scan_qr',{
  						device_key:result
  					},function(data){
  						mui.toast(data.MSG);
  						// 扫码成功 开启绑定流程！
  						if(data.CODE == 0){ 
  							mui.openWindow({
  								url: "bind_toy.html",
  								id: "bind_toy.html",
  								extras:data.DATA
  							})
  						}
  						// 扫码也成功，但是已经被绑定过了
  						else if(data.CODE == 2){
  							// 开启添加好友的流程
  							var s = Sdata.type; // app or toy
  							console.log(s);
  							var toy_data = {
  								toy_id: data.DATA.toy_id,
  								add_id:Sdata.create_toy_id,
  								"add_type":s,
  							}
  							mui.openWindow({
  								url: "add_req.html",
  								id: "add_req.html",
  								extras:toy_data
  							})
  							
  						}
  						// 扫描失败，请不要瞎78乱扫
  						else{
  							mui.back();
  						}
  					},'json'
  				);
  			
  			}
  
  			mui.plusReady(function() {
  				Sdata = plus.webview.currentWebview();//引用携带过来的全局数据,用于返回user_id等信息,添加好友
  				var scan = new plus.barcode.Barcode("bcid");
  				scan.start();
  				// onmarked("qr","afc59916257ae8a2b6ccdfb9fd273373");
  				scan.onmarked = onmarked;
  			})
  ```

- 后端接口进行，验证二维码结果和设备库、以注册设备表进行比对，返回不同的结果

  ```python
  @user.route('/scan_qr', methods=['POST'])
  def scan_qr():
      device = request.form.to_dict()
      toy = MongoDB.device.find_one(device)
      if toy:
          RET["CODE"] = 2
          RET["MSG"] = "设备已经绑定"
          RET["DATA"] = {
              "toy_id": str(toy['_id'])
          }
          return jsonify(RET)
  
      print(device)
      for obj in os.listdir(QRCODE_PATH):
          if obj[:-4] == device['device_key']:
              RET["CODE"] = 0
              RET["MSG"] = "二维码扫描成功"
              RET["DATA"] = device
              break
      else:
          RET["CODE"] = 1
          RET["MSG"] = "二维码扫描失败"
  
      return jsonify(RET)
  ```

  

- 通过后，前端自动获取toy_list接口

  ```python
  @user.route('/toy_list', methods=['POST'])
  def toy_list():
      # print(request.form.to_dict())
      user_id = request.form.to_dict()
      user_id['user_id'] = user_id.pop('_id')
      toy = MongoDB.device.find(user_id)
  
      if toy:
          ret = []
          print(ret)
          for toy_obj in toy:
              print(toy_obj)
              toy_obj['_id'] = str(toy_obj.pop('_id'))
              ret.append(toy_obj)
  
          RET['CODE'] = 0,
          RET['msg'] = '获取Toy列表',
          RET['DATA'] = ret
  
          return jsonify(RET)
      return jsonify(RET)
  ```

  

#### 绑定玩具信息

- 后端需要实现的接口：用于APP绑定设备，并创建Toy信息

  URL地址:	 /bind_toy
  请求方式:	POST
  请求协议:

  ```
  JSON:
  {
      "toy_name":toy_name, //toy名称
      "baby_name":baby_name, //toy所属主人名称
      "remark":remark, //toy主人对App用户的称呼
      "user_id":user_id,//绑定Toy的App用户Id
      "device_key":device_key, //设备唯一编码device_key
  }
  ```

  响应数据

  ```
  JSON:
  {
  	"code":0,
  	"msg":"绑定完成",
  	"data":{}
  }
  ```

- 分析：相应的当APP扫描通过了，就会让用户填写玩具信息，发给后端，让后端存储信息，但是有个很难的点是，怎么存储toy表，我们查看toy的存储的数据结构文档

  ```json
  toys表：
  {
  	"_id" : ObjectId("5ca17f85ea512d215cd9b079"), // 自动生成ID
  	"toy_name" : "小粪球儿", // 玩具的昵称
  	"baby_name" : "圆圆", // 玩具主人的昵称
  	"device_key" : "afc59916257ae8a2b6ccdfb9fd273373", // 玩具的设备编号
  	"avatar" : "toy.jpg", // 玩具的头像固定值 "toy.jpg"
  	"bind_user" : "5c9d8da3ea512d2048826260", // 玩具的绑定用户
  	"friend_list" : [ // 玩具通讯录信息 
  		{ // 与Users数据表 friend_list 结构相同
  			"friend_id" : "5c9d8da3ea512d2048826260",
  			"friend_nick" : "DragonFire",
  			"friend_remark" : "爸爸",
  			"friend_avatar" : "baba.jpg",
  			"friend_chat" : "5ca17f85ea512d215cd9b078",
  			"friend_type" : "app"
  		},
  		{
  			"friend_id" : "5ca17c7aea512d26281bcb8d",
  			"friend_nick" : "臭屎蛋儿",
  			"friend_remark" : "蛋蛋的忧伤",
  			"friend_avatar" : "toy.jpg",
  			"friend_chat" : "5ca5e789ea512d2e544da015",
  			"friend_type" : "toy"
  		}
  	]
  }
  ```

  - 关键点：

    ```
    1、通过user_id使用户绑定相应的用户id
    2、friend_list 字段toys和users都有，这样就可以双方进行绑定，通过friend_id和friend_type进行区分
    3、主要是friend_chat，用户和toy，或则toy和toy之间的聊天窗口，在数据库中存在chat表，每条记录生成一个聊天窗口，记录双方的聊天窗口，但是当我们要存储toy的时候，此时的阿chat记录并没有生成，所以我们需要在每次存储toy玩具的之前，就要创建一个空chat对象
    ```

- 后端接口代码

  ```python
  @devices.route('/bind_toy', methods=['POST'])
  def bind_toy():
      toy_info = request.form.to_dict()
      user_id = toy_info.pop('user_id') # 找出用户id
      user_info = MongoDB.users.find_one({'_id':ObjectId(user_id)}) #通过用户id找出用户信息
  
      chat_window = MongoDB.chats.insert_one({'user_list':[],'chat_list':[]})
      chat_id = str(chat_window.inserted_id)  # 获取插入的数据的object_id
  
      # 创建toy在friendlist的名片
      toy_add_user = {
          'friend_id': user_id,
          'friend_nick':user_info.get('username'),  # 绑定的是用户的信息
          'friend_remark':toy_info.get('remark'),
          'friend_avatar':user_info.get('avatar'),
          'friend_chat':chat_id,
          'friend_type':'app',
      }
      if not toy_info.get('friend_list'):
          toy_info['friend_list'] = []
  
      toy_info['friend_list'].append(toy_add_user)
      toy_info['bind_user'] = user_id
      toy_info['avatar'] = 'toy.jpg'
  
      # 创建玩具
      toy = MongoDB.toys.insert_one(toy_info)
      toy_id = str(toy.inserted_id)
  
  
      user_info['bind_toys'].append(toy_id)
  
      # 创建user在friend_list的名片
      user_add_toy = {
          "friend_id":toy_id,
          'friend_nick':toy_info.get('toy_name'),
          'friend_remark':toy_info.get('baby_name'),
          'friend_avatar':toy_info.get('avatar'),
          'friend_chat':chat_id,
          'friend_type':'toy',
      }
  
      user_info['friend_list'].append(user_add_toy)
  
      # 更新user
      MongoDB.users.update_one({'_id':ObjectId(user_id)},{'$set':user_info})
  
       #聊天窗口
      MongoDB.chats.update_one({'_id':ObjectId(chat_id)},{'$set':{'user_list':[toy_id,user_id]}})
  
      RET['CODE'] = 0
      RET['MSG'] = '绑定完成'
      RET['DATA'] = {}
  
      return jsonify(RET)
  ```

  

#### APP向玩具建立长连接，发送music

- 使用websocket接受连接的客户端（APP、玩具），在其中进行消息的转发

  ```python
  import json
  from flask import Flask,request
  from geventwebsocket.handler import WebSocketHandler
  from geventwebsocket.server import WSGIServer
  from geventwebsocket.websocket import WebSocket
  
  ws_app = Flask(__name__)
  
  user_socket_dict = {}
  
  @ws_app.route('/toy/<toy_id>')
  def find_toy(toy_id):
      web_toy = request.environ.get('wsgi.websocket')  #type:WebSocket
  
      if web_toy:
          user_socket_dict[toy_id] = web_toy
  
      while 1:
          print(user_socket_dict)
          user_msg = web_toy.receive()
          print(user_msg)
          user_msg_dict = json.loads(user_msg)
          to_user = user_msg_dict.get('to_user')
          reveiver = user_socket_dict.get(to_user)
          reveiver.send(user_msg)
  
  
  @ws_app.route('/app/<app_id>')
  def find_app(app_id):
      web_app = request.environ.get('wsgi.websocket')  #type:WebSocket
      # print(web_app)
      if web_app:
          user_socket_dict[app_id] = web_app
  
      while 1:
          print(user_socket_dict)
          user_msg = web_app.receive()
          print(user_msg)
          user_msg_dict = json.loads(user_msg)
          to_user = user_msg_dict.get('to_user') #APP始终会发送to_user,表示jie'shou'z
          reveiver = user_socket_dict.get(to_user)
          reveiver.send(user_msg)
  
  
  if __name__ == '__main__':
      http_serv = WSGIServer(('0.0.0.0',9528),ws_app,handler_class=WebSocketHandler)
      http_serv.serve_forever()
  
  #5faa4351b2c8770c725069cc7d1b716d
  ```

- 在Flask后端需要写toy_open接口，用于玩具端输入设备好后，玩具开机

  ```python
  @devices.route('/open_toy', methods=['post'])
  def toy_open():
      device_key = request.form.to_dict()
  
      device_toy = MongoDB.toys.find_one(device_key)
      device = MongoDB.devices.find_one(device_key)
      # print(device,device_toy,device_key)
  
      RET = {}
      if device_toy: # 正在使用的设备
          RET['code'] = 0
          RET['music'] = '182aa2e6-7c5b-45e8-9cc3-59fb3d59df29.mp3'
          RET['toy_id'] = str(device_toy['_id'])
          RET['name'] = device_toy['toy_name']
          return jsonify(RET)
  
      elif device:  # 未绑定的设备
          RET['code'] = 2
          RET['music'] = '601aa642-94a2-4e30-952c-13fbf14b0735.mp3'
          return jsonify(RET)
  
      else:  #  没有绑定的设备，且没有使用的
          RET['code'] = 1
          RET['music'] = '1045b0f3-06ea-4483-8401-f08661c572fc.mp3'
          return jsonify(RET)
  
  ```

- 玩具端的web.html模拟

  ```js
   function open_toy() {
          var device_key = document.getElementById("device_key").value;
          $.post(
              "http://127.0.0.1:9527/open_toy",
              {device_key: device_key},
              function (data) {
                  console.log(data);
                  if (data.code == 0) {
                      console.log(111)
                      document.getElementById("title").innerText = data.name;
                      toy_id = data.toy_id;
                      create_ws(toy_id);
                  }
                  document.getElementById("player").src = "http://127.0.0.1:9527/get_music/" + data.music;
              },
              "json"
          );
      }
  
  
      function create_ws(toy_id) {
          ws = new WebSocket("ws://127.0.0.1:9528/toy/" + toy_id); // 456
          ws.onmessage = function (eventMessage) { //456.onmessage
              var recv_msg = JSON.parse(eventMessage.data);
              console.log(recv_msg);
              if (recv_msg.music) {
                  document.getElementById("player").src = "http://127.0.0.1:9527/get_music/" + recv_msg.music;
              } else {
                  document.getElementById("from_user").innerText = recv_msg.from_user;
                  document.getElementById("from_user_type").innerText = recv_msg.friend_type;
                  document.getElementById("player").src = "http://127.0.0.1:9527/get_chat/" + recv_msg.chat;
              }
          };
          ws.onclose = function () {
              create_ws(toy_id);
          };
      }
  ```

  ![1566184310086](C:\Users\RootUser\Desktop\知识点复习\Django\gif\1566184310086.png)

