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