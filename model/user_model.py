import mysql.connector
import json
from flask import make_response, session, request
from datetime import datetime
from datetime import timedelta
import jwt
from config.config import dbconfig
import re

mobRegex = re.compile(r'^\d{10}$')
emailRegex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')  
user_data = [
    "name",
    "email",
    "phone",
    "password",
    "role_id",
    "secondary_no_1",
    "secondary_no_2",
    "ID"
]
token_blacklist = []


class user_model():

    def __init__(self):
        try:
            self.con = mysql.connector.connect(host=dbconfig['hostname'], user=dbconfig['username'], password=dbconfig['password'], database=dbconfig['database'])            
            self.con.autocommit = True
            self.cur = self.con.cursor(dictionary=True)
            print('Connection Succesfull')
        except:
            print('Connection Failed')


    def user_getall_model(self):
        print("API WANTS TO FETCH USER")

        self.cur.execute("select * from users")
        result = self.cur.fetchall()
        if len(result)<1:
            return make_response({"message" : "No Data Found"}, 204)
        else:
            return make_response({"payload" : result}, 200)
        
        
    def user_add_model(self, data):
        print("API WANTS TO CREATE NEW USER")
        userEmail = data['email']
        mobile = data['phone']
        not_secondary_Number = True
        both = False

        if re.fullmatch(emailRegex, userEmail):
            pass
        else:
            return make_response({"message": "Email is not valid"})

        if re.fullmatch(mobRegex, mobile):
            pass
        else:
            print("i'm here")
            return make_response({"message": "Entered mobile number is not valid"})
        
        for key in data:
            if key not in user_data:
                return make_response({"message": "Please Enter all the required details only"})
            
            if key == "secondary_no_1":
                no1 = data['secondary_no_1']
                not_secondary_Number = False
                                
                if re.fullmatch(mobRegex, no1):
                    pass
                else:
                    return make_response({"message": "Secondary number is not valid"}, 202)

            if key == "secondary_no_2":
                no2 = data['secondary_no_2']
                both = True
                
                if re.fullmatch(mobRegex, no2):
                    pass
                else:
                    return make_response({"message": "Secondary number is not valid"}, 202)

                if no1 == no2:
                    return make_response({"message": "Both secondary numbers are same"}, 202)
            
        if not_secondary_Number:
            self.cur.execute(f"SELECT * FROM users WHERE email = '{data['email']}'")
            result = self.cur.fetchall()
            if len(result)>0:
                return make_response({"message" : "User with same email id already exsist"})
            else:
                self.cur.execute(f"SELECT * FROM users WHERE phone = '{data['phone']}'") 
                result = self.cur.fetchall()
                if len(result)>0:
                    return make_response({"message" : "User with same phone number already exsist"})
                else:
                    self.cur.execute(f"INSERT INTO users (name, email, phone, password, role_id) VALUES ('{data['name']}', '{data['email']}', '{data['phone']}', '{data['password']}', '{data['role_id']}')")
                    return make_response({"message" : "User Created Successfully"}, 201)

        else:
                self.cur.execute(f'SELECT secondary_number FROM users')
                result = self.cur.fetchall()
                
                self.cur.execute(f'SELECT ID FROM users')
                allId = self.cur.fetchall();

                list=[]

                for ID in allId:
                    id = ID['ID']
                    index = 0
                    self.cur.execute(f'SELECT secondary_number FROM users WHERE ID = {id}')
                    sec_num_result = self.cur.fetchall()

                    for key in sec_num_result:
                        sec_data = sec_num_result[index]["secondary_number"].replace(" ", "")
                        index += 1
                        # print(f'this is sec data {sec_data}')
                        newData =sec_data.split(",")
                        list.extend(newData)
                
                # print(f'This is list {list}')
                if both:    
                    if no1 not in list:
                        if no2 not in list:
                            self.cur.execute(f"SELECT * FROM users WHERE email = '{data['email']}'")
                            result = self.cur.fetchall()
                            if len(result)>0:
                                return make_response({"message" : "User with same email id already exsist"})
                            else:
                                self.cur.execute(f"SELECT * FROM users WHERE phone = '{data['phone']}'") 
                                result = self.cur.fetchall()
                                if len(result)>0:
                                    return make_response({"message" : "User with same phone number already exsist"})
                                else:
                                    self.cur.execute(f"INSERT INTO users (name, email, phone, password, role_id, secondary_number) VALUES ('{data['name']}', '{data['email']}', '{data['phone']}', '{data['password']}', '{data['role_id']}', '{data['secondary_no_1']},{data['secondary_no_2']}')")
                                    return make_response({"message" : "User Created Successfully"}, 201)
                        else:
                            return make_response({"message" : "User with same secondary number already exist"}, 202)
                    else:
                        return make_response({"message" : "User with same secondary number already exist"}, 202)
                else:
                    if no1 not in list:
                        self.cur.execute(f"SELECT * FROM users WHERE email = '{data['email']}'")
                        result = self.cur.fetchall()
                        if len(result)>0:
                            return make_response({"message" : "User with same email id already exsist"})
                        else:
                            self.cur.execute(f"SELECT * FROM users WHERE phone = '{data['phone']}'") 
                            result = self.cur.fetchall()
                            if len(result)>0:
                                return make_response({"message" : "User with same phone number already exsist"})
                            else:
                                self.cur.execute(f"INSERT INTO users (name, email, phone, password, role_id, secondary_number) VALUES ('{data['name']}', '{data['email']}', '{data['phone']}', '{data['password']}', '{data['role_id']}', '{data['secondary_no_1']}')")
                                return make_response({"message" : "User Created Successfully"}, 201)
                    else:
                        return make_response({"message" : "User with same secondary number already exist"}, 202)


    def user_update_model(self, data):
        print("API WANTS TO CREATE USER")
        userEmail = data['email']
        mobile = data['phone']
        print(len(mobile))
        not_secondary_Number = True
        both = False
        email_exist = False
        phone_exist = False

        if re.fullmatch(emailRegex, userEmail):
            pass
        else:
            return make_response({"message": "Email is not valid"})

        if re.fullmatch(mobRegex, mobile):
            pass
        else:
            print("i'm here")
            return make_response({"message": "Entered mobile number is not valid"})

        self.cur.execute(f"SELECT * FROM users WHERE email='{data['email']}'")
        result = self.cur.fetchall()
        if len(result)>0:
            email_exist = True
        
        self.cur.execute(f"SELECT * FROM users WHERE phone='{data['phone']}'")
        result = self.cur.fetchall()
        if len(result)>0:
            phone_exist = True

        for key in data:
            if key not in user_data:
                return make_response({"message": "Please Enter all the required details only"})
            
            if key == "secondary_no_1":
                no1 = data['secondary_no_1']
                not_secondary_Number = False
                                
                if re.fullmatch(mobRegex, no1):
                    pass
                else:
                    return make_response({"message": "Secondary number is not valid"}, 202)

            if key == "secondary_no_2":
                no2 = data['secondary_no_2']
                both = True
                
                if re.fullmatch(mobRegex, no2):
                    pass
                else:
                    return make_response({"message": "Secondary number is not valid"}, 202)

                if no1 == no2:
                    return make_response({"message": "Both secondary numbers are same"}, 202)
              
        if not_secondary_Number:
            print("I'm here in not secondry number conditional statement")
            self.cur.execute(f"SELECT * FROM users WHERE ID = '{data['ID']}'")
            result = self.cur.fetchall()
            if len(result)>0:
                self.cur.execute(f"UPDATE users SET name='{data['name']}', email='{data['email']}', phone='{data['phone']}', password='{data['password']}' , role_id='{data['role_id']}' WHERE ID={data['ID']} ")
                return make_response({"Message": "User updated successfully"})
            else:
                if email_exist:
                    return make_response({"Error": "User with same email already exsist"}, 202)
                            
                if phone_exist:
                    return make_response({"Error": "User with same phone already exsist"}, 202)

                self.cur.execute(f"INSERT INTO users (name, email, phone, password, role_id) VALUES ('{data['name']}', '{data['email']}', '{data['phone']}', '{data['password']}', '{data['role_id']}')")
                result = self.cur.fetchall()
                return make_response({"message" : "New user created successfully!"}, 201)
        else:
            self.cur.execute(f'SELECT secondary_number FROM users')
            result = self.cur.fetchall()
            
            self.cur.execute(f'SELECT ID FROM users')
            allId = self.cur.fetchall();

            list=[]

            for ID in allId:
                id = ID['ID']
                index = 0
                self.cur.execute(f'SELECT secondary_number FROM users WHERE ID = {id}')
                sec_num_result = self.cur.fetchall()

                for key in sec_num_result:
                    sec_data = sec_num_result[index]["secondary_number"].replace(" ", "")
                    index += 1
                    # print(f'this is sec data {sec_data}')
                    newData =sec_data.split(",")
                    list.extend(newData)
            
            if both:    
                if no1 not in list:
                    if no2 not in list:
                        self.cur.execute(f"SELECT * FROM users WHERE ID = '{data['ID']}'")
                        result = self.cur.fetchall()
                        if len(result)>0:
                            self.cur.execute(f"UPDATE users SET name='{data['name']}', email='{data['email']}', phone='{data['phone']}', password='{data['password']}' , role_id='{data['role_id']}', secondary_number='{data['secondary_no_1']},{data['secondary_no_2']}' WHERE ID={data['ID']} ")
                            return make_response({"Message": "User updated successfully"})
                        else:
                            if email_exist:
                                return make_response({"Error": "User with same email already exsist"}, 202)
                            
                            if phone_exist:
                                return make_response({"Error": "User with same phone already exsist"}, 202)
                            
                            self.cur.execute(f"INSERT INTO users (name, email, phone, password, role_id, secondary_number) VALUES ('{data['name']}', '{data['email']}', '{data['phone']}', '{data['password']}', '{data['role_id']}', '{data['secondary_no_1']},{data['secondary_no_2']}')")
                            result = self.cur.fetchall()
                            return make_response({"message" : "New user created successfully!"}, 201)
            
                    else:
                        return make_response({"message" : "User with same secondary number already exist"}, 202)
                else:
                    return make_response({"message" : "User with same secondary number already exist"}, 202)
            
            else:
                if no1 not in list:
                    self.cur.execute(f"SELECT * FROM users WHERE ID = '{data['ID']}'")
                    result = self.cur.fetchall()
                    if len(result)>0:
                        self.cur.execute(f"UPDATE users SET name='{data['name']}', email='{data['email']}', phone='{data['phone']}', password='{data['password']}' , role_id='{data['role_id']}', secondary_number='{data['secondary_no_1']}' WHERE ID={data['ID']} ")
                        return make_response({"Message": "User updated successfully"})
                    else:
                        if email_exist:
                            return make_response({"Error": "User with same email already exsist"}, 202)
                        
                        if phone_exist:
                            return make_response({"Error": "User with same phone already exsist"}, 202)
                        
                        self.cur.execute(f"INSERT INTO users (name, email, phone, password, role_id, secondary_number) VALUES ('{data['name']}', '{data['email']}', '{data['phone']}', '{data['password']}', '{data['role_id']}', '{data['secondary_no_1']}')")
                        result = self.cur.fetchall()
                        return make_response({"message" : "New user created successfully!"}, 201)
                else:
                    return make_response({"message" : "User with same secondary number already exist"}, 202)


    def user_delete_model(self, id):
        print("API WANTS TO DELETE USER")
        self.cur.execute(f"DELETE FROM users WHERE ID={id}")
        if self.cur.rowcount > 0:
            return make_response({"message" : "User Deleted Successfully"}, 200)
        else:
            return make_response({"message" : "Nothing to do"}, 202)
        

    def user_patch_model(self, data, id):
        print("API WANTS TO UPDATE USER USING PUT METHOD")
        query = "UPDATE users SET "
        for key in data:
            query += f"{key}= '{data[key]}',"
        
        query = query[:-1] + f" WHERE ID={id}"

        self.cur.execute(query)  
        if self.cur.rowcount > 0:
            return make_response({"message" : "User Updated Successfully"}, 201)
        else:
            return make_response({"message" : "Nothing to do"}, 202)
      
    
    def user_pagination_model(self, limit, page):
        print("API WANTS TO FETCH USER IN A PAGINATION FORMAT")
        limit = int(limit)
        page = int(page)
        start = (page * limit) - limit
        query = f"SELECT * FROM users LIMIT {start}, {limit}"

        self.cur.execute(query)
        result = self.cur.fetchall()
        if len(result)<1:
            return make_response({"message" : "No Data Found"}, 204)
        else:
            return make_response({"payload" : result, "limit": limit, "page_no." :page}, 200)


    def user_upload_avatar_model(self, path, id):
        print("API WANTS TO UPDATE USER AVATAR USING PUT METHOD")
        self.cur.execute(f"UPDATE users SET avatar='{path}' WHERE ID={id}")
        if self.cur.rowcount > 0:
            return make_response({"message" : "File Uploaded Successfully"}, 201)
        else:
            return make_response({"message" : "Nothing to do"}, 202)


    def user_login_model(self, data):
        print("API WANTS TO GET JWT TOKEN")
        self.cur.execute(f"SELECT ID, email, phone, avatar, role_id, secondary_number FROM users WHERE email='{data['email']}' and password='{data['password']}'")
        result = self.cur.fetchall()
        session['role_id'] = result[0]['role_id']
        if len(result) > 0:
            userdata = result[0]
            exp_time = datetime.now() + timedelta(minutes=15)
            exp_epoch_time = int(exp_time.timestamp())
            payload = {
                "payload": userdata,
                "exp" : exp_epoch_time
            }
            jwtoken = jwt.encode(payload, "mohit", algorithm="HS256")
            return make_response({"token": jwtoken}, 200)
        else:
            return make_response({"Error" : "Enter Valid email id or password"}, 401)

        
    def get_data_model(self, no):
        print("API WANTS TO GET USER USING THEIR SECONDARY NUMBER")
        self.cur.execute(f'SELECT secondary_number FROM users')
        result = self.cur.fetchall()
        # print(f'all secondary no. are {result}')
        
        self.cur.execute(f'SELECT ID FROM users')
        allId = self.cur.fetchall();
        # print(f'All Ids are {allId}')

        for ID in allId:
            id = ID['ID']
            self.cur.execute(f'SELECT secondary_number FROM users WHERE ID = {id}')
            sec_num_result = self.cur.fetchall()
            for key in sec_num_result:
                list=[]
                data = sec_num_result[0]["secondary_number"].replace(" ", "")
                newData =data.split(",")
                list.extend(newData)
                
                if no in list:
                    print(id)
                    self.cur.execute(f'SELECT * FROM users WHERE ID =  {id}')
                    result = self.cur.fetchall()
                    return make_response({"payload" : result}, 200)
               
        return {"message" : "user does not exsist"}
        

    def user_logout_model(self):
        token = request.headers.get('Authorization')
        token = token.split(" ")[1]
        token_blacklist.append(token)
        print(token_blacklist)
        return make_response({"Message": "User Logout Successfull"})