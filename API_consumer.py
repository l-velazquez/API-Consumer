import json
import requests
import os
from dotenv import load_dotenv

load_dotenv(".env")

debug = 1

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

def admin_requests(base_url, admin_login, headers):
    headers = headers # make a copy of the headers
    # Endpoints
    authenticate = ["/Auth/login", "/Auth/logout"]
    roles = "/Roles"
    users = "/Users"

    url_auth = base_url+authenticate[0]
    url_logout = base_url+authenticate[1]
    url_roles = base_url+roles
    url_users = base_url+users

    #login as admin
    print("Logging in as admin")
    admin_response = POST_request(url_auth, admin_login, headers) 
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
    for i in range(1, 22):
        user_data = GET_request(url_users+"/"+str(i), headers)
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
    print("Logging in as user")
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
    print("Logged out as user")


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


admin_requests(base_url, admin_login, headers)
user_requests(base_url, user_login, headers)

