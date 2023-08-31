import mysql.connector
import json
from flask import make_response
from datetime import datetime
from datetime import timedelta
import jwt
from config.config import dbconfig

number = ["1","2","3","4","5","6","7","8","9","0"]
mail = ["gmail.com", "outlook.com"]
user_data = ["name", "email", "phone", "password", "role_id", "secondary_no_1", "secondary_no_2"]

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
        
        
    def user_addone_model(self, data):

        print("API WANTS TO CREATE A NEW USER")
        email = data['email'].split("@")
        mobile = data['phone']
        print(len(mobile))
        not_secondary_Number = True
        both = False

        for key in data:
            if key not in user_data:
                return make_response({"message": "Please Enter all the required details only"})
            
            if key == "secondary_no_1":
                no1 = data['secondary_no_1']
                not_secondary_Number = False
                if len(no1) != 10:
                    return make_response({"message": "Secondary number should be of 10 digit"}, 202)
                
                for index in range(0, 10):
                    if no1[index] not in number:
                        return make_response({"message": "Secondary number should be a number"}, 202)

            if key == "secondary_no_2":
                no2 = data['secondary_no_2']
                both = True
                if len(no2) != 10:
                    return make_response({"message": "Secondary number should be of 10 digit"}, 202)
                
                for index in range(0, 10):
                    if no1[index] not in number:
                        return make_response({"message": "Secondary number should be a number"}, 202)

                if no1 == no2:
                    return make_response({"message": "Both secondary numbers are same"}, 202)
          

        if email[len(email)-1] not in mail:
            return make_response({"message": "Enter a valid email id"}, 202)

        if len(mobile) != 10:
            return make_response({"message": "Phone number should be of 10 digit"}, 202)


        for index in range(0, 10):
            if mobile[index] not in number:
                return make_response({"message": "Phone number should be a number"}, 202)
    
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
        print("API WANTS TO UPDATE USER USING PUT METHOD")
        if len(data) == 8:
            self.cur.execute(f"SELECT * FROM users WHERE ID = {data['ID']}")
            result = self.cur.fetchall()
            if(len(result)< 1):
                return make_response({"message" : "User Not Found"}, 202)

            else:
                no1 = data['secondary_no_1']
                no2 = data['secondary_no_2']
                email = data['email'].split("@")
                mobile = data['phone']
                print(email)
                if no1 == no2:
                    return make_response({"message": "Both secondary numbers are same"}, 202)
                
                if email[len(email)-1] not in mail:
                    return make_response({"message": "Enter a valid email id"}, 202)
                
                if len(no1) != 10 or len(no2) != 10:
                    return make_response({"message": "Secondary number should be of 10 digit"}, 202)

                if len(mobile) != 10:
                    return make_response({"message": "Phone number should be of 10 digit"}, 202)


                for index in range(0, len(no1)):
                    if no1[index] not in number:
                        return make_response({"message": "Secondary number should be a number"}, 202)

                    if no2[index] not in number:
                        return make_response({"message": "Secondary number should be a number"}, 202)

                    if mobile[index] not in number:
                        return make_response({"message": "Phone number should be a number"}, 202)

                self.cur.execute(f"UPDATE users SET name='{data['name']}', email='{data['email']}', phone='{data['phone']}', password='{data['password']}' , role_id='{data['role_id']}', secondary_number='{data['secondary_no_1']},{data['secondary_no_2']}' WHERE ID={data['ID']} ")
                if self.cur.rowcount > 0:
                    return make_response({"message" : "User Updated Successfully"}, 201)
                else:
                    return make_response({"message" : "Nothing to do"}, 202)
        else:
            return make_response({"message" : "Enter all the required fields"}, 202)


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
        
        