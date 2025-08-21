import configparser
import os


def load_config(path=None):
    config = configparser.ConfigParser()
    if path is None:
        # 自动找 config.ini，基于当前文件的位置
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        path = os.path.join(root_dir, 'config', 'config.ini')
    config.read(path, encoding='utf-8')
    return config
