import json
import requests
import os
from dotenv import load_dotenv
from APIError import APIError

load_dotenv(".env")

debug = 0


def save_json(data, filename):
    with open(filename, "w") as json_file:
        print("Saving data to", filename)
        json.dump(data, json_file, indent=4)
        print("Data saved")


def response_data(response_data):
    if response_data.status_code == 200:
        if response_data.text:  # Check if response has content
            json_response = response_data.json()
            if debug:
                print("-" * 140)
                print("JSON data: \n", json_response)
                print("Stauts code:", response_data.status_code)
            return json_response
        else:
            # print("The response was empty")
            return None
    else:
        if debug:
            print("Error status code:", response_data.status_code)
            print("Response content:", response_data.text)
        raise APIError(
            f"API Error: Status Code {response_data.status_code} - {response_data.text}"
        )


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
    headers = headers  # make a copy of the headers
    # Endpoints
    authenticate = ["/Auth/login", "/Auth/logout"]
    users = "/Users"

    url_auth = base_url + authenticate[0]
    url_users = base_url + users

    # login as admin
    print("Logging in as admin")
    print("-" * 140, "\n")

    admin_response = POST_request(url_auth, admin_login, headers)
    if not (admin_response["success"]):
        print("No data returned")
        # get out of the function
        return

    token = admin_response["data"]["accessToken"]  # get token from response
    headers["Authorization"] = "Bearer " + token  # add token to headers

    amount_of_users = 0

    for i in range:
        user = GET_request(url_users + "/" + str(i), headers)

        if not (user["success"]):
            print("\tNo data returned")
            return
            # get out of the function
        else:
            print("\t" + user["data"]["fullName"])
            amount_of_users += 1
    print("-" * 140, f"\nTotal amount of users: {amount_of_users}")


def get_products(range, base_url, admin_login, headers):
    headers = headers  # make a copy of the headers
    # Endpoints
    authenticate = ["/Auth/login", "/Auth/logout"]
    products = "/Products"

    url_auth = base_url + authenticate[0]
    url_products = base_url + products

    # login as admin
    print("Logging in as admin")
    print("-" * 140, "\n")

    admin_response = POST_request(url_auth, admin_login, headers)
    if not (admin_response["success"]):
        print("No data returned")
        # get out of the function
        return

    token = admin_response["data"]["accessToken"]  # get token from response
    headers["Authorization"] = "Bearer " + token  # add token to headers

    amount_of_products = 0

    products = GET_request(url_products, headers)
    # save_json(products, "products.json")

    for i in range:
        product = GET_request(url_products + "/" + str(i), headers)

        if not (product["success"]):
            print("\tNo data returned")
            print("-" * 140, f"\nTotal amount of products: {amount_of_products}")
            return
            # get out of the function
        else:
            print("\tProduct " + str(i))
            print("-" * 140, "\n")
            print("\tID:\t\t" + str(product["data"]["id"]))
            print("\tName:\t\t" + product["data"]["name"])
            print("\tDescription:\t" + product["data"]["description"])
            print("\tPrice:\t\t$" + str(product["data"]["price"]))
            print("\tQuantity:\t" + str(product["data"]["quantity"]))
            print("\n")
            amount_of_products += 1
    print("-" * 140, f"\nTotal amount of products: {amount_of_products}")


def get_roles(range, base_url, admin_login, headers):
    headers = headers  # make a copy of the headers
    # Endpoints
    authenticate = ["/Auth/login", "/Auth/logout"]
    roles = "/Roles"

    url_auth = base_url + authenticate[0]
    url_roles = base_url + roles

    # login as admin
    print(f"Logging in as {admin_login['userName']}")
    print("-" * 140, "\n")

    admin_response = POST_request(url_auth, admin_login, headers)
    if not (admin_response["success"]):
        print("No data returned")
        # get out of the function
        return

    token = admin_response["data"]["accessToken"]  # get token from response
    headers["Authorization"] = "Bearer " + token  # add token to headers

    print(GET_request(url_roles, headers))

    amount_of_roles = 0

    for i in range:
        role = GET_request(url_roles + "/" + str(i), headers)

        if not (role["success"]):
            print("\tNo data returned")
            return
            # get out of the function
        else:
            print("\tRole " + str(i))
            print("\t" + role["data"]["name"])
            print
            amount_of_roles += 1
    print("-" * 140, f"\nTotal amount of roles: {amount_of_roles}")


def post_users(base_url, login, headers, full_name_array):
    headers = headers  # make a copy of the headers
    # Endpoints
    authenticate = ["/Auth/login", "/Auth/logout"]
    users = "/Users"

    url_auth = base_url + authenticate[0]
    url_logout = base_url + authenticate[1]
    url_users = base_url + users

    # login as admin
    print(f"Logging in as {login['userName']}")
    admin_response = POST_request(url_auth, login, headers)
    token = admin_response["data"]["accessToken"]  # get token from response
    headers["Authorization"] = "Bearer " + token  # add token to headers

    # Post data
    print("\n\n\n\nPOSTing data")
    method = "POST"

    user_name_array = []
    for name in full_name_array:
        user_name_array.append(username_creator(name))

    email_array = []
    for name in full_name_array:
        email_array.append(email_creator(name))
    length = len(full_name_array)

    for i in range(0, length):
        new_user = {
            "fullName": full_name_array[i],
            "userName": user_name_array[i],
            "email": email_array[i],
            "password": password_creator(),
            "roleId": 1,
        }
        user_data = POST_request(url_users, new_user, headers)
        # receive data
        print(user_data)
        if debug:
            save_json(user_data, f"user_{method}_user_data_{i}.json")

    # logout as admin
    POST_request(url_logout, {}, headers)
    print(f"Logged out as {login['userName']}")


def put_users(base_url, login, headers):
    headers = headers  # make a copy of the headers
    # Endpoints
    authenticate = ["/Auth/login", "/Auth/logout"]
    users = "/Users"

    url_auth = base_url + authenticate[0]
    url_logout = base_url + authenticate[1]
    url_users = base_url + users

    # login as admin
    print(f"Logging in as {login['userName']}")
    admin_response = POST_request(url_auth, login, headers)
    token = admin_response["data"]["accessToken"]  # get token from response
    headers["Authorization"] = "Bearer " + token  # add token to headers

    # Post data
    print("\n\n\n\nPUTing data")

    method = "PUT"

    # get all users in the system
    users_data = GET_request(url_users, headers)
    # list of all users names
    user_names = []
    for user in users_data["data"]:
        user_names.append(user["userName"])
    count = 0
    for user in user_names:
        count += 1
        print(str(count) + ".\t", user)

    # Chose user to update
    user_id = input("\nEnter the number of the user you want to update: ")

    # Get user data with the id
    user_data = GET_request(url_users + "/" + user_id, headers)
    data_of_user = user_data["data"]
    full_name = data_of_user["fullName"]
    user_name = data_of_user["userName"]
    email = data_of_user["email"]
    role = data_of_user["role"]

    print("\n\tUser data: ")
    print("\tID: ", user_id)
    print("\tFull Name: ", full_name)
    print("\tUsername: ", user_name)
    print("\tEmail: ", email)
    print("\tRole: ", role)
    print("\n")
    update_username = input("Enter the new username: ")
    print("Updating username to", update_username)

    update_user = {
        "id": user_id,
        "fullName": full_name,
        "userName": update_username,
        "email": email,
        "password": password_creator(),
        "roleId": 2,
    }

    user_update = PUT_request(url_users, update_user, headers)

    success = user_update["success"]
    message = user_update["message"]

    if success:
        print(message)

    agian = input("Do you want to update another user? (y/n): ")
    if agian == "y":
        put_users(base_url, login, headers)
    else:
        print("Logging out")
        POST_request(url_logout, {}, headers)
        print(f"Logged out as {login['userName']}")
    # logout as admin


def admin_requests(base_url, admin_login, headers):
    headers = headers  # make a copy of the headers
    # Endpoints
    authenticate = ["/Auth/login", "/Auth/logout"]
    roles = "/Roles"
    users = "/Users"
    products = "/Products"

    url_auth = base_url + authenticate[0]
    url_logout = base_url + authenticate[1]
    url_roles = base_url + roles
    url_users = base_url + users
    url_products = base_url + products

    # login as admin
    print("Logging in as admin")
    admin_response = POST_request(url_auth, admin_login, headers)

    if admin_response["success"] == False:
        print("No data returned")
        # get out of the function
        return

    token = admin_response["data"]["accessToken"]  # get token from response
    headers["Authorization"] = "Bearer " + token  # add token to headers

    # Get data
    method = "GET"
    roles_data = GET_request(url_roles, headers)
    if debug:
        save_json(roles_data, f"admin_{method}_roles_data.json")
    users_data = GET_request(url_users, headers)
    if debug:
        save_json(users_data, f"admin_{method}_users_data.json")
    for i in range(1, 26):
        user_data = GET_request(url_users + "/" + str(i), headers)
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
        "Sophia Wilson",
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
            "roleId": 1,
        }
        user_data = POST_request(url_users, new_user, headers)
        if debug:
            save_json(user_data, f"admin_{method}_user_data_{i}.json")

    # logout as admin
    POST_request(url_logout, {}, headers)
    print("Logged out as admin")


def user_requests(base_url, user_login, headers):
    headers = headers  # make a copy of the headers
    # Endpoints
    authenticate = ["/Auth/login", "/Auth/logout"]
    roles = "/Roles"
    users = "/Users"

    url_auth = base_url + authenticate[0]
    url_logout = base_url + authenticate[1]
    url_roles = base_url + roles
    url_users = base_url + users

    # login as user
    print("-" * 140)
    print("\nLogging in as user")
    user_response = POST_request(url_auth, user_login, headers)
    token = user_response["data"]["accessToken"]  # get token from response
    headers["Authorization"] = "Bearer " + token  # add token to headers

    roles_data = GET_request(url_roles, headers)
    if debug:
        save_json(roles_data, "user_roles_data.json")
    users_data = GET_request(url_users, headers)
    if debug:
        save_json(users_data, "user_users_data.json")

    # logout as user
    POST_request(url_logout, {}, headers)
    print("\n\nLogged out as user")


def main():

    base_url = "https://ccom4995-assignment2.azurewebsites.net/api/v1"

    # Authentication
    username = os.getenv("username")
    password = os.getenv("password")
    username2 = os.getenv("username2")
    password2 = os.getenv("password2")

    # load data
    admin_login = {
        "userName": username,
        "password": password,
    }
    user_login = {
        "userName": username2,
        "password": password2,
    }

    headers = {"Content-Type": "application/json"}

    # admin_requests(base_url, admin_login, headers)
    # user_requests(base_url, user_login, headers)

    full_name_array = [
        "Eliam Rodriguez",
    ]

    # get_users(range(1, 36), base_url, admin_login, headers)
    # get_products(range(1, 200), base_url, admin_login, headers)
    # get_users(range(1, 36), base_url, user_login, headers)
    # post_users(base_url, user_login, headers, full_name_array)
    # get_roles(range(1, 36), base_url, admin_login, headers)
    put_users(base_url, admin_login, headers)


if __name__ == "__main__":
    main()
