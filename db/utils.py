import os.path
import configparser
from hashlib import md5
from shutil import copyfile

def hashstring(text):
    return md5(text.encode()).hexdigest()

class Config(configparser.ConfigParser):
    """
    An object for handling reading and if necessary creation of configuration file.
    """
    def __init__(self, path='', *args, **kwargs):
        configparser.ConfigParser.__init__(self)
        self.path = 'config.cfg'
        if not os.path.isfile(self.path):
            copyfile('default.cfg', 'config.cfg')
        self.read(self.path)


if __name__ == "__main__":
    config = Config()
    print(config['DATABASE']['db_url'])
