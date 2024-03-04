# API Consumer

The link to this API is not included in this repository because it is a private API made specifically for the class API design and development. The API is a simple API that has endpoints for users and admin. The admin can create, read, update and delete users. The users can only read their own information.

This is a simple API consumer python script that will go through all the endpoints of the API and print the results.

To set this up you will need to have python installed on your machine.

## Setup

```bash
python --version
```

If you don't have python installed, you can download it from [here](https://www.python.org/downloads/)

```bash
git clone github.com/repo
cd api-consumer
```

## Set up virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Set up environment variables

```bash
touch .env
```

Use this template an fill in the values

```bash
# admin
username=your_username
password=your_password

# users
username2=your_username
password2=your_password
```

Save the file in the root of the project.

## Run the script

```bash
python API_consumer.py
```
