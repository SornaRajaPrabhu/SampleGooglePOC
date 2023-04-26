from Authentication import BasicAuthentication
from getinfoanaplan import GetInfoFromAnaplan
from Configurations_info import config
from log import log_information
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello() -> str:
    config_info = config()
    userName = config_info.get_username()
    password = config_info.get_password()
    return 'Hello World!' + userName + password


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
