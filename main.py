import os
from flask import Flask, jsonify, request
from config import DevConfig
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)
from werkzeug.utils import secure_filename

# 初始化 Flask 類別成為 instance
app = Flask(__name__)
app.config.from_object(DevConfig)
app.config['JWT_SECRET_KEY'] = '047db533-4ea6-443d-9ecf-a44ae2d0b8fb'  # 加密私鑰
jwt = JWTManager(app)

# 測試用
@app.route('/')
def index():
    return 'Hello World!'

# 登入取得token
@app.route('/login', methods=['POST'])
def login(): 
    username = request.json.get('username', None) 
    password = request.json.get('password', None) 

    if username != 'test' or password != 'test': 
        return jsonify({"msg": "Bad username or password"}), 401

    # Use create_access_token() and create_refresh_token() to create our
    # access and refresh tokens
    ret = {
        'access_token': create_access_token(identity=username),
        'refresh_token': create_refresh_token(identity=username)
    }
    return jsonify(ret), 200

# 更新token
@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    ret = {
        'access_token': create_access_token(identity=current_user)
    }
    return jsonify(ret), 200

# 測試token是否正確
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    username = get_jwt_identity()
    return jsonify(logged_in_as=username), 200



ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 承接人臉資訊
@app.route('/facechk', methods=['POST'])
@jwt_required
def upload_image():
    if 'file' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message' : 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # 人臉辨識承接部份
        # file.save(....., filename))

        # 人臉辨識成功取得id
        if (1==2):
            resp = jsonify({'id' : filename})
            resp.status_code = 200
        # 辨識不到ID
        else:
            resp = jsonify({'message' : 'Can not found id!!'})
            resp.status_code = 404
        return resp
    else:
        resp = jsonify({'message' : 'Allowed file types are png, jpg, jpeg'})
        resp.status_code = 400
        return resp


# 判斷自己執行非被當做引入的模組，因為 __name__ 這變數若被當做模組引入使用就不會是 __main__
if __name__ == '__main__':
    app.run()