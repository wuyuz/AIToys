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

