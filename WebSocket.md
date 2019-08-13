## WebSocket



#### 轮询、长轮询、长连接

- **HTTP** ：无状态的短连接，Http是无状态连接，也就是说没有服务端不会主动想客户端发送消息，那么要达到即使通信，必须要保证客户端主动及时的访问服务端。



- ##### 制作一个聊天功能：

  ```python
      - A to B Message
  	- A to server to B Message  ~Http Find B
  	     A:{to:B,chat:"come on baby",from:A} 
  	- A Http B Http
  	- server MessageBox save B Message
  		server : [{to:B,chat:"come on baby",from:A}]
  	- B Http server MessageBox
  		B -> MessageBox -> Key=to=B -> chat
  	- B recv Message
  	
  	#核心思想是，涉及一个消息盒子，用来存储所有的信息，如果来取，自己来取自己的
  ```

- ##### 三种客户端/服务端的连接形式

  ```python
  	轮询:
  		不能保证数据实时性，有一定的时间限制
  		A B Client -> 无限循环和Server对话 有xx的消息吗
  	
  	长轮询:
  		A B Client -> Client发起请求至Server 有xx的消息吗 -> 等待消息时间 1x/s （Http连接时间）
  		-> 主动断开连接  
  		-> 收到消息主动返回
  	
  	长连接:
  		AB Client -> Server 建立连接 并保持不断开 ->
  		A to B -> Server 消息转发 -> B 建立连接的情况下 -> 可以及时准确的收到消息
  	
  ```

  

#### WebSocket

WebSocket 是 HTML5 开始提供的一种在单个 TCP 连接上进行全双工通讯的协议。

​		WebSocket 使得客户端和服务器之间的数据交换变得更加简单，允许服务端主动向客户端推送数据。在 WebSocket API 中，浏览器和服务器**只需要完成一次握手，两者之间就直接可以创建持久性的连接，并进行双向数据传输**。当你获取 Web Socket 连接后，你可以通过 **send()** 方法来向服务器发送数据，并通过 **onmessage** 事件来接收服务器返回的数据。



##### WebSocket属性

以下是 WebSocket 对象的属性。假定我们使用了以上代码创建了 Socket 对象：

| 属性                  | 描述                                                         |
| :-------------------- | :----------------------------------------------------------- |
| Socket.readyState     | 只读属性 **readyState** 表示连接状态，可以是以下值：0 - 表示连接尚未建立。1 - 表示连接已建立，可以进行通信。2 - 表示连接正在进行关闭。3 - 表示连接已经关闭或者连接不能打开。 |
| Socket.bufferedAmount | 只读属性 **bufferedAmount** 已被 send() 放入正在队列中等待传输，但是还没有发出的 UTF-8 文本字节数。 |

##### WebSocket事件

以下是 WebSocket 对象的相关事件。假定我们使用了以上代码创建了 Socket 对象：

| 事件    | 事件处理程序     | 描述                       |
| :------ | :--------------- | :------------------------- |
| open    | Socket.onopen    | 连接建立时触发             |
| message | Socket.onmessage | 客户端接收服务端数据时触发 |
| error   | Socket.onerror   | 通信发生错误时触发         |
| close   | Socket.onclose   | 连接关闭时触发             |



#### 基于 websocket 实现群聊

```
1.建立websocket 服务 + Flask web框架 + Gevent-WebSocket
2.request.environ.get("wsgi.websocket") 获取连接，将获取到的连接保持在服务器中 socket_list = []
3.基于长连接socket 接收用户传递的消息
4.将消息转发给其他用户
```

#### 基于 JavaScript 实现 Websocket 客户端

```js
var ws = new WebSocket("ws://") # ws 的路由地址
ws.onmessage = func(MessageEvent){实现逻辑}

ws.onmessage 当ws客户端收到消息时执行回调函数
ws.onopen 当ws客户端建立完成连接时 status == 1 时执行的回调函数
ws.onclose 当ws客户端关闭中或关闭时 执行的回调函数 status == 2,3
ws.onerror 当ws客户端出现错误时
```

- ##### Flask代码

  ```python
  from flask import Flask, request, render_template
  from geventwebsocket.handler import WebSocketHandler  # 请求处理 WSGI HTTP
  from geventwebsocket.server import WSGIServer  # 替换Flask原来的WSGI服务
  from geventwebsocket.websocket import WebSocket  # 语法提示
  
  app = Flask(__name__)
  
  socket_list = []  # 用于存储连接的socket对象
  
  @app.route("/ws")
  def my_ws():
      # print(request.environ)
      # 注意：type:WebSocket,是用来进行语法提示的，不然没有语法提示
      ws_socket = request.environ.get("wsgi.websocket")  # type:WebSocket
      socket_list.append(ws_socket)  # 及那个获取到的对象添加到列表中
      print(len(socket_list),socket_list)
      while True:
          msg = ws_socket.receive()  #多个线程会阻塞在这
          print(msg)
          for usocket in socket_list:
              if usocket == ws_socket:  # 不给自己发消息
                  continue
              try:
                  usocket.send(msg)
              except:
                  continue
  
  @app.route("/wechat")
  def wechat():
      return render_template("ws.html")
  
  
  if __name__ == '__main__':
      # app.run()
      http_serv = WSGIServer(("0.0.0.0", 9527), app,
                             handler_class=WebSocketHandler)  
                             # handler_class=WSGIHandler HTTPHandler
      http_serv.serve_forever()
  
  ```

- ##### HTML代码

  ```html
  <body>
  <input type="text" id="content"><button onclick="send_msg()">发送消息</button>
  <div id="content_list"></div>
  <script type="application/javascript">
      var ws = new WebSocket("ws://127.0.0.1:9527/ws");
      //ws.onmessage属性是一个当收到来自服务器的消息时将调用函数
      ws.onmessage = function (messageEvent){       
          var my_div = document.getElementById("content_list");
          var ptag = document.createElement("p");
          ptag.innerText = messageEvent.data;
          my_div.appendChild(ptag);
      };
      function send_msg() {
          var msg = document.getElementById("content").value;
          ws.send(msg);
      }
  </script>
  
  </body>
  ```

  

#### Websocket单点聊天时的转发

```
1、服务器中保存的连接方式发生变化 以字典形式储存
	存储结构 : {用户的唯一标识:Websocket连接,user1:Websocket}
2、单点消息发送时 receive data = {sender:发送方,receiver:接收方,data:数据}
	从data中找到接收方的"名字"Key
	拿着名字key 去存储结构中 找到 名字Key所对应的websocket连接
	websocket连接.send(data) # socket 传输 bytes
```

- ##### Flask代码

  ```python
  import json
  from flask import Flask, request, render_template
  from geventwebsocket.handler import WebSocketHandler  # 请求处理 WSGI HTTP
  from geventwebsocket.server import WSGIServer  # 替换Flask原来的WSGI服务
  from geventwebsocket.websocket import WebSocket  # 语法提示
  
  app = Flask(__name__)
  
  # socket_list = []
  # socket_dict = {"xiaobanghzu":akjsdlfsadkfj,"shangjia":asudhfkjasdhfkjahs}
  socket_dict = {}
  
  
  @app.route("/ws/<username>")
  def my_ws(username):
      # print(request.environ)
      ws_socket = request.environ.get("wsgi.websocket")  # type:WebSocket
      socket_dict[username] = ws_socket
      print(len(socket_dict), socket_dict)
  
      while True:
          msg = ws_socket.receive()
          msg_dict = json.loads(msg)
          receiver = msg_dict.get("receiver")  #获取接收值的值
          receiver_socket = socket_dict.get(receiver)
          receiver_socket.send(msg) #向接受者发送消息
  
  @app.route("/wechat")
  def wechat():
      return render_template("ws.html")
  
  
  if __name__ == '__main__':
      # app.run()
      http_serv = WSGIServer(("0.0.0.0", 9527), app,
                             handler_class=WebSocketHandler)  # handler_class=WSGIHandler / HTTPHandler
      http_serv.serve_forever()
  ```

  - ##### 长连接的requset和http的request的差别是多出了以下几项

    ```python
    'HTTP_CONNECTION': 'Upgrade,keep-alive'  #http
    
     ---------------------websocket的request-------------
    'HTTP_CONNECTION': 'Upgrade',  # 请求方式，表示长连接
    'HTTP_UPGRADE': 'websocket',
    'HTTP_SEC_WEBSOCKET_VERSION': '13'  #websocket版本
    'HTTP_SEC_WEBSOCKET_KEY': '+XlqBnhqwEekZTYcz4I+tg=='
    'HTTP_SEC_WEBSOCKET_EXTENSIONS': 'permessage-deflate; client_max_window_bits'
    'wsgi.websocket_version': '13'
    'wsgi.websocket': <geventwebsocket.websocket.WebSocket object at 0x00000120280E54C0>
    ```

    

- ##### HTML代码

  ```html
  \<body>
  <p>你的昵称:<input type="text" id="username"><button onclick="login()">登录聊天室</button></p>
  给<input type="text" id="receiver">发送<input type="text" id="content"><button onclick="send_msg()">发送消息</button>
  <div id="content_list" style="width: 500px;">
  </div>
  
  </body>
  <script type="application/javascript">
      var ws = null;
      function send_msg() {
          var msg = document.getElementById("content").value;
          var receiver = document.getElementById("receiver").value;
          var sender = document.getElementById("username").value;
  
          var send_str = {
            receiver:receiver,
            sender:sender,
            data:msg
          };
  
          ws.send(JSON.stringify(send_str));
          var my_div = document.getElementById("content_list");
          var ptag = document.createElement("p");
          ptag.innerText = msg + " : 我";
          ptag.style.cssText = "text-align: right";
          my_div.appendChild(ptag);
      }
  
      function login() {
          var username = document.getElementById("username").value;
          ws = new WebSocket("ws://192.168.12.87:9527/ws/"+username);
  		/接受服务器返回的数据 
          ws.onmessage = function (messageEvent) {
              console.log(messageEvent.data);
              var obj = JSON.parse(messageEvent.data);
              var my_div = document.getElementById("content_list");
              var ptag = document.createElement("p");
              ptag.innerText = obj.sender + " : " +obj.data;
              my_div.appendChild(ptag);
          };
      }
  </script>
```
  



#### WebSocket源码

- 实例化WSGIServer类

  ```python
  http_serv = WSGIServer(("0.0.0.0",9527),app,handler_class=WebSocketHandler)
  http_serv.serve_forever()
  
   # serve_forever 函数是WSGIServer类的顶级父类BaseServer(),该函数调用了自身的start() 函数：
      def start(self):
          self.init_socket()   #初始化socket
          self._stop_event.clear()
          try:
              self.start_accepting()  #开始监听
          except:
              self.close()
              raise    
  ```

- 查看WSGIServer类源码，执行初始化函数

  ```python
      def __init__(self, listener, application=None, backlog=None, spawn='default',
                   log='default', error_log='default',  # application = app
                   handler_class=None,  #请求方式
                   environ=None, **ssl_args):
          StreamServer.__init__(self, listener, backlog=backlog, spawn=spawn, **ssl_args)
          if application is not None:
              self.application = application
          if handler_class is not None:
              self.handler_class = handler_class  # 将传入的handler进行赋值
  ```

- 查看WebSocketHandler源码

  ```python
  SUPPORTED_VERSIONS = ('13', '8', '7')   #版本
  GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11" #magicstring，魔术字符串，进行加密时使用
  
   #当一个websocket创建成功后会触发run_websocket(self)函数，里面会为请求数据中添加值，并且设置websocket属性：
      self.environ.update({
                  'wsgi.websocket': None
              })
  	self.websocket = None
  ```

- upgrade_websocket(self)函数用于校验，长连接是否可用（websocket是否通过客户端的校验）

  ```python
  1、upgrade = self.environ.get('HTTP_UPGRADE', '').lower()  #获得请求中的连接方式
     if upgrade == 'websocket':
         connection = self.environ.get('HTTP_CONNECTION', '').lower()  #获取请求的连接方式，上面可看响应参数
         
  2、 判断当前版本，并执行连接更新函数   
  	if self.environ.get('HTTP_SEC_WEBSOCKET_VERSION'):
              return self.upgrade_connectionzhon()   #upgrade_connectionzhon重要
  ```

- upgrade_connection 判断连接是否通过，并更新

  ```python
  1、获取请求中传来的随机字符串，可以在headers中参考
   	key = self.environ.get("HTTP_SEC_WEBSOCKET_KEY", '').strip()
  
  2、在下面建立了长连接：
  	self.websocket = WebSocket(self.environ, Stream(self), self) #实例化websocket
      self.environ.update({  # 给请求中添加值
              'wsgi.websocket_version': version,   # 赋值版本
              'wsgi.websocket': self.websocket   #websocke对象
          })
  
  3、根据key和魔法字符串生成accept，用于返回给客户端审核是否通过
  	accept = base64.b64encode(hashlib.sha1((key + self.GUID).encode("latin-1")).digest()).decode("latin-1")  #base64 + sha1(magicstring + key)
      
  4、制作返回给客户端的相应头
      headers = [
                  ("Upgrade", "websocket"),
                  ("Connection", "Upgrade"),
                  ("Sec-WebSocket-Accept", accept) #看客户端是否能通过accept
              ]
  ```

  