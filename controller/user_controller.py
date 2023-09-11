from app import app
from flask import request, send_file, make_response
from datetime import datetime
from model.user_model import user_model
from model.auth_model import auth_model
from flask_expects_json import expects_json
obj = user_model()
auth = auth_model()

schema = {
  "type": "object",
  "properties": {
    "name": { "type": "string" },
    "email": { "type": "string" },
    "phone": {"type": "number"},
    "secondary_number": {"type": "number"},
    "role_id" : {"type": "number"},
    "password": {"type" : "string"}
  }
}

#Get Request Method
@app.route('/getall', methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
@auth.token_auth(id="")
def user_getall_connector():
    if request.method == 'GET':
        return obj.user_getall_model()
    else:
        return make_response({"Error" : "This Method is not allowed please use the GET method"}, 405)


#Post Request Method of API
@app.route('/add',  methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
@auth.token_auth(id="")
def user_addone_connector():
    if request.method == 'POST':
        return obj.user_add_model(request.form)
    else:
        return make_response({"Error" : "This Method is not allowed please use the POST method"}, 405)


#Put Request Method
@app.route('/update',  methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
@auth.token_auth(id="")
def user_update_connector():
    if request.method == 'PUT':
        return obj.user_update_model(request.form)
    else:
        return make_response({"Error" : "This Method is not allowed please use the PUT method"}, 405)


#Delelte Request Method
@app.route('/delete/<id>',  methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
@auth.token_auth(id)
def user_delete_connector(id):
    if request.method == 'DELETE':
        return obj.user_delete_model(id)
    else:
        return make_response({"Error" : "This Method is not allowed please use the DELETE method"}, 405)



#Patch Request Method
@app.route('/patch/<id>',  methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
@auth.token_auth(id)
def user_patch_connector(id):
    if request.method == 'PATCH':
        return obj.user_patch_model(request.form, id)
    else:
        return make_response({"Error" : "This Method is not allowed please use the PATCH method"}, 405)


# pagination
@app.route('/users/getall/<limit>/<page>',  methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
@auth.token_auth(id="")
def user_pagination_connector(limit, page):
    if request.method == 'GET':
        return obj.user_pagination_model(limit, page)
    else:
        return make_response({"Error" : "This Method is not allowed please use the GET method"}, 405)



#upload images:
@app.route('/upload/avatar/<id>',  methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
@auth.token_auth(id)
def user_upload_avatar_connector(id):
    if request.method == 'PUT':
        file = request.files['avatar']
        uniqueFileName = str(datetime.now().timestamp()).replace(".", "")
        filenameSplit = file.filename.split(".")
        ext = filenameSplit[len(filenameSplit)-1]
        path = f"upload/{uniqueFileName}.{ext}"
        file.save(path)
        return obj.user_upload_avatar_model(path, id)
    else:
        return make_response({"Error" : "This Method is not allowed please use the PUT method"}, 405)


#Get the uploaded Images: 
@app.route('/avatar/<filename>',  methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
@auth.token_auth(id)
def user_uploaded_image_connector(filename):
    if request.method == 'GET':
        return send_file(f"upload/{filename}")
    else:
        return make_response({"Error" : "This Method is not allowed please use the GET method"}, 405)


#User Login to get token * > *
@app.route('/login',  methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
def user_login_controller():
    if request.method == 'POST':
        return obj.user_login_model(request.form)
    else:
        return make_response({"Error" : "This Method is not allowed please use the POST method"}, 405)

#Search by Mobile: * > *
@app.route('/mobile/<no>',  methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
def getdata(no):
    if request.method == 'GET':
        return obj.get_data_model(no)
    else:
        return make_response({"Error" : "This Method is not allowed please use the GET method"}, 405)



@app.route("/logout",  methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
def logout():
    if request.method == 'POST':
        return obj.user_logout_model()
    else:
        return make_response({"Error" : "This Method is not allowed please use the DELTET method"}, 405)
