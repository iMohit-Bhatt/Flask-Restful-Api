from app import app
from flask import request, send_file
from datetime import datetime
from model.user_model import user_model
from model.auth_model import auth_model
from flask_expects_json import expects_json
obj = user_model()
auth = auth_model()

#Get Request Method
@app.route('/getall')
@auth.token_auth()
def user_getall_connector():
    return obj.user_getall_model()


#Post Request Method
@app.route('/add', methods=['POST'])
def user_addone_connector():
    return obj.user_add_model(request.form)


#Put Request Method
@app.route('/update', methods=['PUT'])
def user_update_connector():
    return obj.user_update_model(request.form)


#Delelte Request Method
@app.route('/delete/<id>', methods=['DELETE'])
def user_delete_connector(id):
    return obj.user_delete_model(id)


#Patch Request Method
@app.route('/patch/<id>', methods=['PATCH'])
def user_patch_connector(id):
    return obj.user_patch_model(request.form, id)


# pagination
@app.route('/users/getall/<limit>/<page>')
def user_pagination_connector(limit, page):
    return obj.user_pagination_model(limit, page)


#upload images:
@app.route('/upload/avatar/<id>', methods=['PUT'])
def user_upload_avatar_connector(id):
    file = request.files['avatar']
    uniqueFileName = str(datetime.now().timestamp()).replace(".", "")
    filenameSplit = file.filename.split(".")
    ext = filenameSplit[len(filenameSplit)-1]
    path = f"upload/{uniqueFileName}.{ext}"
    file.save(path)
    return obj.user_upload_avatar_model(path, id)


#Get the uploaded Images:
@app.route('/avatar/<filename>', methods=['GET'])
def user_uploaded_image_connector(filename):
    return send_file(f"upload/{filename}")


@app.route('/login', methods=['POST'])
def user_login_controller():
    return obj.user_login_model(request.form)

@app.route('/mobile/<no>')
def getdata(no):
    return obj.get_data_model(no)