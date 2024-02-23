import json
import requests
import os
from dotenv import load_dotenv

load_dotenv(".env")

debug = 0

def save_json(data, filename):
    with open(filename, 'w') as json_file:
        print("Saving data to", filename)
        json.dump(data, json_file, indent=4)
        print("Data saved")

def response_data(response_data):
    if response_data.status_code == 200:
        if response_data.text:  # Check if response has content
            json_response = response_data.json()
            if debug:
                print("-"*140)
                print("JSON data: \n", json_response)
                print("Stauts code:", response_data.status_code)
            return json_response
        else:
            print('The response was empty')
            return None
    else:
        json_data = response_data.json()
        if debug:
            print("JSON data: \n", json_data)
            print("Status code:", response_data.status_code)
        return json_data

def POST_request(url, data, headers):
    if data == {}:
        return response_data(requests.post(url, headers=headers))
    return response_data(requests.post(url, json=data, headers=headers))

def GET_request(url, headers):
    return response_data(requests.get(url, headers=headers))

def PUT_request(url, data, headers):
    return response_data(requests.put(url, json=data, headers=headers))

def DELETE_request(url, headers):
    return response_data(requests.delete(url, headers=headers))

def username_creator(full_name):
    full_name = full_name.split()
    username = full_name[0][0].lower() + full_name[1].lower()
    return username

def email_creator(full_name):
    full_name = full_name.split()
    email = full_name[0].lower() + full_name[1].lower() + "@test.com"
    return email

def password_creator():
    # Passwords must have at least one non alphanumeric character., Passwords must have at least one digit ('0'-'9')., Passwords must have at least one uppercase ('A'-'Z').
    password = "Password1!"
    return password

def get_users(range, base_url, admin_login, headers):
    headers = headers # make a copy of the headers
    # Endpoints
    authenticate = ["/Auth/login", "/Auth/logout"]
    users = "/Users"
    
    url_auth = base_url+authenticate[0]
    url_users = base_url+users

    #login as admin
    print("Logging in as admin")
    print("-"*140, "\n")

    admin_response = POST_request(url_auth, admin_login, headers)
    if admin_response["success"]==False:
        print("No data returned")
        # get out of the function
        return
    
    token = admin_response["data"]["accessToken"] # get token from response
    headers['Authorization'] = "Bearer " + token # add token to headers

    amount_of_users = 0

    for i in range:
        user = GET_request(url_users+"/"+str(i+1), headers)
    
        if not(user["success"]):
            print("\tNo data returned")
            # get out of the function
        else:
            print("\t"+user["data"]["fullName"])
            amount_of_users += 1
    print("-"*140,f"\nTotal amount of users: {amount_of_users}")
    

def admin_requests(base_url, admin_login, headers):
    headers = headers # make a copy of the headers
    # Endpoints
    authenticate = ["/Auth/login", "/Auth/logout"]
    roles = "/Roles"
    users = "/Users"
    products = "/Products"

    url_auth = base_url+authenticate[0]
    url_logout = base_url+authenticate[1]
    url_roles = base_url+roles
    url_users = base_url+users
    url_products = base_url+products

    #login as admin
    print("Logging in as admin")
    admin_response = POST_request(url_auth, admin_login, headers)
    
    if admin_response["success"] == False:
        print("No data returned")
        # get out of the function
        return
    
    token = admin_response["data"]["accessToken"] # get token from response
    headers['Authorization'] = "Bearer " + token # add token to headers

    # Get data
    method = "GET"
    roles_data = GET_request(url_roles, headers)
    if debug:
        save_json(roles_data, f"admin_{method}_roles_data.json")
    users_data = GET_request(url_users, headers)
    if debug:
        save_json(users_data, f"admin_{method}_users_data.json")
    for i in range(1, 26):
        user_data = GET_request(url_users+"/"+str(i), headers)
        if debug:
            save_json(user_data, f"admin_{method}_user_data_{i}.json")

    # Post data
    print("\n\n\n\nPOSTing data")
    method = "POST"
    full_name_array = [
    "John Smith",
    "Olivia Rodriguez",
    "Benjamin Johnson",
    "Emily Davis",
    "Muhammad Ali",
    "Isabella Martinez", 
    "Noah Brown",
    "Sophia Wilson"
] 
    user_name_array = []
    for name in full_name_array:
        user_name_array.append(username_creator(name))

    email_array = []
    for name in full_name_array:
        email_array.append(email_creator(name))
    
    


    for i in range(0, 8):
        new_user = {
            "fullName": full_name_array[i],
            "userName": user_name_array[i],
            "email": email_array[i],
            "password": password_creator(),
            "roleId": 1
        }
        user_data = POST_request(url_users, new_user, headers)
        if debug:
            save_json(user_data, f"admin_{method}_user_data_{i}.json")
    
    #logout as admin
    POST_request(url_logout, {}, headers)
    print("Logged out as admin")

def user_requests(base_url, user_login, headers):
    headers = headers # make a copy of the headers
    # Endpoints
    authenticate = ["/Auth/login", "/Auth/logout"]
    roles = "/Roles"
    users = "/Users"

    url_auth = base_url+authenticate[0]
    url_logout = base_url+authenticate[1]
    url_roles = base_url+roles
    url_users = base_url+users

    #login as user
    print("-"*140)
    print("\nLogging in as user")
    user_response = POST_request(url_auth, user_login, headers) 
    token = user_response["data"]["accessToken"] # get token from response
    headers['Authorization'] = "Bearer " + token # add token to headers

    roles_data = GET_request(url_roles, headers)
    if debug:
        save_json(roles_data, "user_roles_data.json")
    users_data=GET_request(url_users, headers)
    if debug:
        save_json(users_data, "user_users_data.json")

    #logout as user
    POST_request(url_logout, {}, headers)
    print("\n\nLogged out as user")


base_url = "https://ccom4995-assignment2.azurewebsites.net/api/v1"

# Authentication
username = os.getenv("username")
password = os.getenv("password")
username2 = os.getenv("username2")
password2 = os.getenv("password2")

# load data
admin_login ={
        "userName": username,
        "password": password,
    }
user_login ={
        "userName": username2,
        "password": password2,
    }

headers = {'Content-Type': 'application/json'}


# admin_requests(base_url, admin_login, headers)
# user_requests(base_url, user_login, headers)

get_users(range(1, 36), base_url, admin_login, headers)
