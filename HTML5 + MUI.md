## HTML5 + MUI



#### 准备工作

- **工具**：HBuilder X  +  夜神模拟器

- 真机开发：安卓版本需要点击多次系统版本 + 打开开发者选项 + 打开USB调试 + USB安装允许

- 搭建一个小Demo

  ![1565700353251](C:\Users\RootUser\Desktop\知识点复习\Django\gif\1565700353251.png)

- **配置模拟器**：根据夜神模拟器更改的Android模拟器端口（其他模拟器不一致）：改为62001

- 运行Demo，模拟器上就会出现响应的效果

  ![1565700741151](C:\Users\RootUser\Desktop\知识点复习\Django\gif\1565700741151.png)

- HTML5+ 规范用法网址：http://www.html5plus.org/doc/h5p.html



#### 搭建MyApp

上面只是一个小小的Demo，下面我们将创建一个新的App，快速的搭建

- 在index.html文件中，清空自带的代码，输入：dmo +回车 -->会生成提示，从而生成html代码主干部分，也叫Document元素，将css更改为mui.css

  ```
  <!doctype html>
  <html lang="en">
  <head>
  	<meta charset="UTF-8" />
  	<title>Document</title>
  	<meta name="viewport" content="width=device-width,initial-scale=1,minimum-scale=1,maximum-scale=1,user-scalable=no" />
  	<link rel="stylesheet" type="text/css" href="css/mui.css"/>
  </head>
  <body>
  	
  	<script src="js\" type="text/javascript" charset="utf-8"></script>
  	<script type="text/javascript">
  	mui.init()
  	</script>
  </body>
  </html>
  ```

- header 表示标题栏、mui-content 表示主体内容（快捷键 mbo）、mtb生成底部选项卡

  ```html
  <div class="mui-content">
  	中间的主题内容
  </div>
  ```

- 在body标签中使用 dhe + 回车 --> 生成标题栏

- 使用 msl + 回车 --> 生成轮播图

- 使用 mg + 回车 --> 生成九宫格

- 使用 mta  + 回车 --> 生成底部菜单

  ![1565702224151](C:\Users\RootUser\Desktop\知识点复习\Django\gif\1565702224151.png)

**注意**：

```css
1、图片轮播中的图片地址使用了反斜杠，所以在插入其他部件时会没有提示
2、当使用到css内联样式时，要注意type="text/css"
```

**MUI帮助网站**：http://dev.dcloud.net.cn/mui/ui/



#### 实现拍照取证

- 配置全MUI事件监听，mui默认会监听部分手势事件，如点击、滑动事件；为了开发出更高性能的moble App，mui支持用户根据实际业务需求，通过mui.init方法中的gestureConfig参数，配置具体需要监听的手势事件。

  ```js
  mui.init({  // 可查看官网
    gestureConfig:{
     tap: true, //默认为true,单击屏幕
     doubletap: true, //默认为false,双击
     longtap: true, //默认为false
     swipe: true, //默认为true
     drag: true, //默认为true
     hold:false,//默认为false，不监听
     release:false//默认为false，不监听
    }
  });
  ```

  

- 使用 mbt + 回车 --> 选择一个按钮，触发可以打开摄像头

  ```html
  <button type="button" class="mui-btn mui-btn-blue mui-btn-outlined" id="open">摄像头</button>	
  ```

- 添加js事件：（快捷方式：dga）

  ```js
  document.getElementById("open").addEventListener("tap",function(){
  			console.log("点击")
  })
  ```

- 消失的消息：mdt + 回车 

  ```js
  document.getElementById("open").addEventListener("tap",function(){
  			mui.toast('开启摄像头')
  })
  ```

- 在HTML5 的开发者网站中查看如何调用摄像机

  ```js
  	<script type="text/javascript">
  		mui.init({
  		  gestureConfig:{
  			   tap: true, //默认为true,单击屏幕
  			   doubletap: true, //默认为false,双击
  			   longtap: true, //默认为false,
  			   swipe: true, //默认为true
  			   drag: true, //默认为true
  			   hold:false,//默认为false，不监听
  			   release:false//默认为false，不监听
  			}
  		});
  		document.getElementById("open").addEventListener("tap",function(){
  			mui.toast('开启摄像头')
  			var cmr = plus.camera.getCamera(1) //1表示开启主摄像头
  			var fbl = cmr.supportedImageResolutions[0] //设置分辨率
  			var gs = cmr.supportedImageFormats[0] //格式
  			cmr.captureImage(
  				function(path){
  					mui.toast(path);
  					},
  				function(err){
  					mui.toast(err);
  					},
  					{resolution:fbl,format:gs});	
  		})
  	</script>
  ```

- 那么就可以拍照了，文件会保存在响应的文件中



#### 创建login页面

- 使用 mdo + 回车创建html主干

- 打开新窗口 mop  + 回车创建新窗口，给“设置”选项卡设置login事件，绑定id

  ```js
  document.getElementById('login').addEventListener('tap',function () {
  		        mui.toast('login');
  				mui.openWindow({
  						url:'login.html',
  						id:'login'});
  		})
  ```

- 在login.html中写入输入框代码，可在官网MUI组件中找

  ```html
  <form class="mui-input-group">
      <div class="mui-input-row">
          <label>用户名</label>
      <input type="text" class="mui-input-clear" placeholder="请输入用户名">
      </div>
      <div class="mui-input-row">
          <label>密码</label>
          <input type="password" class="mui-input-password" placeholder="请输入密码">
      </div>
      <div class="mui-button-row">
          <button type="button" class="mui-btn mui-btn-primary" >确认</button>
          <button type="button" class="mui-btn mui-btn-danger" >取消</button>
      </div>
  </form>
  ```

- 完成注册页面

  ```html
  <div class="mui-content">
  	<form class="mui-input-group">
  		<div class="mui-input-row">
  			<label>用户名</label>
  			<input type="text"  id="username" class="mui-input-clear" placeholder="请输入用户名">
  		</div>
  		<div class="mui-input-row">
  			<label>密码</label>
  			<input type="password" id="pwd" class="mui-input-password" placeholder="请输入密码">
  		</div>
  		<div class="mui-input-row">
  			<label>确认密码</label>
  			<input type="password" id="re_pwd" class="mui-input-password" placeholder="再次输入密码">
  		</div>
  		<div class="mui-button-row">
  			<button type="button" class="mui-btn mui-btn-primary" id='reg_btn'>注册</button>
  			<button type="button" class="mui-btn mui-btn-danger mui-action-back">返回</button>
  		</div>
  	</form>
  </div>
  
  
   #js部分
  <script type="text/javascript">
  			mui.init()
  			document.getElementById('reg_btn').addEventListener('tap',function () {
  			       var username = document.getElementById("username").value;
  				   var pwd = document.getElementById("pwd").value;
  				   var repwd = document.getElementById("re_pwd").value;
  				   if (pwd!=repwd) {
  						mui.toast('两次密码不一致')
  				   } else{
  					mui.post('http://192.168.12.42:9527/reg,{
  							username:username,
  							password:pwd
  						},function(data){
  							console.log(data)
  						},'json'
  					);
  				   }
  			})
  </script>
  ```

  

#### 结合Flask存储数据

- 使用Flask创建一个应用

  ```python
  from flask import Flask,request
  
  app = Flask(__name__)
  
  @app.route("/reg",methods=['post'])
  def reg():
      user_info = request.form.to_dict()
      print(user_info)
  
      return "200"
  
  if __name__ == "__main__":
      app.run("0.0.0.0",9527)  #必须写0.0.0.0 否则访问不到，且请求的手机模拟器和电脑不是一个回环地址，必须使用本机的IP地址才能连接
  ```

- 结合MongoDB存储数据，以及前端的post

  ```python
  from flask import Flask,request,jsonify
  from pymongo import MongoClient
  
  MC = MongoClient("127.0.0.1",27017)
  MongoDB = MC['MyApp']
  
  app = Flask(__name__)
  app.debug = True
  
  @app.route("/reg",methods=['post'])
  def reg():
      user_info = request.form.to_dict()
      MongoDB.usertest.insert_one(user_info)
      print(user_info)
  
      return jsonify({"code":0,'msg':'注册成功'})
  
  if __name__ == "__main__":
      app.run("0.0.0.0",9527)
  ```

- 桌面的post请求

  ```js
  		<script type="text/javascript">
  			mui.init()
  			document.getElementById('reg_btn').addEventListener('tap',function () {
  			       var username = document.getElementById("username").value;
  				   var pwd = document.getElementById("pwd").value;
  				   var repwd = document.getElementById("re_pwd").value;
  				   if (pwd!=repwd) {
  						mui.toast('两次密码不一致')
  				   } else{
  					mui.post('http://192.168.12.42:9527/reg',{
  							username:username,
  							password:pwd
  						},function(data){
  							console.log(JSON.stringify(data))
  							if (data.code==0) {
  								mui.toast(data.msg)
  								mui.back();// 返回上一页
  							} else{
  								mui.toast('注册失败')
  							}
  						},'json'
  					);
  				   }
  			})
  	 </script>
  ```

- 实现登陆

  ```python
  from flask import Flask,request,jsonify
  from pymongo import MongoClient
  
  MC = MongoClient("127.0.0.1",27017)
  MongoDB = MC['MyApp']
  
  app = Flask(__name__)
  app.debug = True
  
  @app.route("/reg",methods=['post'])
  def reg():
      user_info = request.form.to_dict()
      MongoDB.usertest.insert_one(user_info)
      print(user_info)
  
      return jsonify({"code":0,'msg':'注册成功'})
  
  @app.route("/login",methods=['post'])
  def login():
      user_info = request.form.to_dict()
      user_dict = MongoDB.usertest.find_one(user_info)
      print(user_info)
      if user_dict:
          return jsonify({"code":0,'msg':'登陆成功'})
      else:
          return jsonify({"code":1,'msg':'登陆失败'})
  
  
  if __name__ == "__main__":
      app.run("0.0.0.0",9527)
  ```

- 响应的前端

  ```js
  		<script type="text/javascript">
  			mui.init()
  			document.getElementById('reg').addEventListener('tap',function () {
  			      mui.openWindow({
  					  url:"reg.html",
  					  id:'reg',
  				  })  
  			})
  			document.getElementById('login').addEventListener('tap',function () {
  			        var username = document.getElementById("username").value;
  					var password = document.getElementById("pwd").value;
  					mui.post('http://192.168.12.42:9527/login',{
  							username:username,
  							password:password
  						},function(data){
  							console.log(JSON.stringify(data))
  						},'json'
  					);
  			})
  		</script>
  ```



#### 实现上传图片

- ##### 前端对密码加密

  ```js
  		<script src="http://cdn.bootcss.com/blueimp-md5/1.1.0/js/md5.js"></script> //导入包
  		<script type="text/javascript">
  			mui.init()
  			document.getElementById('reg_btn').addEventListener('tap',function () {
  			       var username = document.getElementById("username").value;
  				   var pwd = document.getElementById("pwd").value;
  				   var repwd = document.getElementById("re_pwd").value;
  				   if (pwd!=repwd) {
  						mui.toast('两次密码不一致')
  				   } else{
  					mui.post('http://192.168.12.42:9527/reg',{
  							username:username,
  							password:md5(pwd)  //必须导入了包才能实现，响应的login也要加密验证
  						},function(data){
  							console.log(JSON.stringify(data))
  							if (data.code==0) {
  								mui.toast(data.msg)
  								mui.back();// 返回上一页
  							} else{
  								mui.toast('注册失败')
  							}
  						},'json'
  					);
  				   }
  			})
  		</script>
  ```

- 注册和上传头像

  ```python
  from flask import Flask,request,jsonify,send_file
  from pymongo import MongoClient
  
  MC = MongoClient("127.0.0.1",27017)
  MongoDB = MC['MyApp']
  
  app = Flask(__name__)
  app.debug = True
  
  @app.route("/reg",methods=['post'])
  def reg():
      user_info = request.form.to_dict()
      MongoDB.usertest.insert_one(user_info)
      print(user_info)
  
      return jsonify({"code":0,'msg':'注册成功'})
  
  @app.route("/login",methods=['post'])
  def login():
      user_info = request.form.to_dict()
      user_dict = MongoDB.usertest.find_one(user_info)
      print(user_info)
      if user_dict:
          return jsonify({"code":0,'msg':'登陆成功'})
      else:
          return jsonify({"code":1,'msg':'登陆失败'})
  
  @app.route("/uploader",methods=['post'])
  def uploader():
      file = request.files.get('my_tt')
      print(file)  #<FileStorage: '1565714967245.jpg' ('image/jpeg')> 里面有filename属性
      file.save(file.filename)
  
      ret = {
          "code":0,
          "filename":file.filename,
          "msg":"上传成功"
      }
      return jsonify(ret)
  
  @app.route('/get_avatar/<tt_name>',methods=["GET"])
  def get_tt(tt_name):
      return send_file(tt_name)
  
  if __name__ == "__main__":
      app.run("0.0.0.0",9527)
  ```

- 前端的reg.html

  ```html
  	<body>
  		<header class="mui-bar mui-bar-nav">
  			<h1 class="mui-title">注册</h1>
  		</header>
  		<div class="mui-content">
  			<form class="mui-input-group">
  				<div class="mui-input-row">
  					<label>用户名</label>
  					<input type="text" id="username" class="mui-input-clear" placeholder="请输入用户名">
  				</div>
  				<div class="mui-input-row">
  					<label>密码</label>
  					<input type="password" id="pwd" class="mui-input-password" placeholder="请输入密码">
  				</div>
  				<div class="mui-input-row">
  					<label>确认密码</label>
  					<input type="password" id="re_pwd" class="mui-input-password" placeholder="再次输入密码">
  				</div>
  				<div class="mui-input-row">
  					<label>用户昵称</label>
  					<input type="text" id='nickname' class="mui-input-clear" placeholder="用户昵称">
  				</div>
  				<div class="mui-input-row">
  					<label>用户头像</label>
  					<button type="button" class="mui-btn mui-btn-outlined" id="xc">上传头像</button>
  					<button type="button" class="mui-btn mui-btn-blue" id='xj'>打开相机</button>
  				</div>
  
  				<div class="mui-button-row">
  					<button type="button" class="mui-btn mui-btn-primary" id='reg_btn'>注册</button>
  					<button type="button" class="mui-btn mui-btn-danger mui-action-back">返回</button>
  				</div>
  			</form>
  			<img id='ttt'>
  		</div>
  		<script src="js/mui.js" type="text/javascript" charset="utf-8"></script>
  		<script src="http://cdn.bootcss.com/blueimp-md5/1.1.0/js/md5.js"></script>
  		<script type="text/javascript">
  			mui.init();
  			var ttt1 = null;
  			document.getElementById('reg_btn').addEventListener('tap', function() {
  				var username = document.getElementById("username").value;
  				var pwd = document.getElementById("pwd").value;
  				var repwd = document.getElementById("re_pwd").value;
  				var nick = document.getElementById("nickname").value;
  				if (pwd != repwd) {
  					mui.toast('两次密码不一致')
  				} else {
  					mui.post('http://192.168.12.42:9527/reg', {
  						username: username,
  						password: md5(pwd),
  						nickname:nick,
  						ttt1 : ttt1
  					}, function(data) {
  						console.log(JSON.stringify(data))
  						if (data.code == 0) {
  							mui.toast(data.msg)
  							mui.back(); // 返回上一页
  						} else {
  							mui.toast('注册失败')
  						}
  					}, 'json');
  				}
  			})
  			document.getElementById('xj').addEventListener('tap', function() {
  				var cmr = plus.camera.getCamera(1);
  				var fbl = cmr.supportedImageResolutions[0]
  				var gs = cmr.supportedImageFormats[0]
  				cmr.captureImage(function(s) {
  						//s 拍照成功之后的保存路径
  						//上传照片,拍了就上传
  						console.log('12')
  						var task = plus.uploader.createUpload("http://192.168.12.42:9527/uploader", {
  								method: "POST",
  							},
  							function(t, status) {
  								// 上传完成
  								console.log(status,t)
  								if (status == 200) {
  									console.log(JSON.stringify(t))
  									var res = JSON.parse(t.responseText)
  									console.log(res)
  									document.getElementById("ttt").src = "http://192.168.12.42:9527/get_avatar/"+res.filename
  									ttt1 = res.filename;
  								} else {
  
  								}
  							}
  						);
  						task.addFile(s,{key:"my_tt"}) //服务端接受的的key是 my_tt
  						task.start();
  					},
  					function(err) {}, {
  						format: gs,
  						resolution: fbl,
  					})
  			})
  
  			document.getElementById('xc').addEventListener('tap', function() {
  				plus.gallery.pick(
  					function(s) {
  						document.getElementById("ttt").src = s
  					},
  					function(err) {}, {}
  				)
  			})
  		</script>
  	</body>
  ```

- 前端的登陆login.html

  ```html
  	<body>
  		<header class="mui-bar mui-bar-nav">
  			<a class="mui-action-back mui-icon mui-icon-left-nav mui-pull-left"></a>
  			<h1 class="mui-title">登陆</h1>
  		</header>
  		<div class="mui-content">
  			欢迎来到Login
  			<form class="mui-input-group">
  				<div class="mui-input-row">
  					<label>用户名</label>
  					<input type="text" id='username' class="mui-input-clear" placeholder="请输入用户名">
  				</div>
  				<div class="mui-input-row">
  					<label>密码</label>
  					<input type="password" id='pwd' class="mui-input-password" placeholder="请输入密码">
  				</div>
  
  				<div class="mui-button-row">
  					<button type="button" class="mui-btn mui-btn-primary" id='login'>Login</button>
  					<button type="button" class="mui-btn mui-btn-danger" id='reg'>Register</button>
  				</div>
  			</form>
  		</div>
  
  		<script src="js/mui.js" type="text/javascript" charset="utf-8"></script>
  		<script src="http://cdn.bootcss.com/blueimp-md5/1.1.0/js/md5.js"></script>
  		<script type="text/javascript">
  			mui.init()
  			document.getElementById('reg').addEventListener('tap', function() {
  				mui.openWindow({
  					url: "reg.html",
  					id: 'reg',
  				})
  			})
  			document.getElementById('login').addEventListener('tap', function() {
  				var username = document.getElementById("username").value;
  				var password = document.getElementById("pwd").value;
  				mui.post('http://192.168.12.42:9527/login', {
  					username: username,
  					password: md5(password)
  				}, function(data) {
  					console.log(JSON.stringify(data))
  				}, 'json');
  			})
  		</script>
  	</body>
  ```

- 实现效果

  ![1565716474107](C:\Users\RootUser\Desktop\知识点复习\Django\gif\1565716474107.png)





##### 错误事项：

```js
1、upload 后面没有/，否则后端一直抛错404
function img_uploader(filePath){
				var task = plus.uploader.createUpload("http://192.168.12.42:9527/upload",{},
				function(t,status){
					if (status==200) {
						data_obj = JSON.parse(task.responseText);
						document.getElementById("avatar").style.width="200px";
						document.getElementById("avatar").style.height="200px";
						document.getElementById("avatar").src = 'http://192.168.12.42:9527/get_avatar/'+ data_obj.filename
					} else{
						
					}
				})
				task.addFile(filePath,{key:"avatar"})
				task.start()
			}

```

