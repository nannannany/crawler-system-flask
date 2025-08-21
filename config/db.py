from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import configparser
import os

# 读取配置文件
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

user = config.get('database', 'user')
password = config.get('database', 'password')
host = config.get('database', 'host')
port = config.get('database', 'port')
dbname = config.get('database', 'dbname')

# 组装数据库 URI
DB_URI = f'postgresql://{user}:{password}@{host}:{port}/{dbname}?options=-c%20timezone=Asia/Shanghai'


# 初始化 SQLAlchemy 对象
db = SQLAlchemy()
