from flask import Flask, request
from server.file_manager import fm
from server.users import user

app = Flask(__name__)
app.register_blueprint(fm)
app.register_blueprint(user)



if __name__ == '__main__':
    app.run('0.0.0.0',9527)