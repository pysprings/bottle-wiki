from hashlib import md5
import os.path
import json

def hashstring(text):
    return md5(text.encode()).hexdigest()

class Config(object):

        def __init__(self, path='config.json'):
            self.defaultconfig = {'db_url':'sqlite:///:memory:', 'debug':True}

            if not os.path.isfile(path):
                print("No config.json found, creating default config.")
                with open(path, 'w') as conf:
                    conf.write(json.dumps(self.defaultconfig))
            with open(path, 'r') as conf:
                self.config = json.loads(conf.read())
        
        def getconfig(self, handle):
                return self.config.get(handle)

if __name__ == "__main__":
    config = Config()
    print(config.config)
    print(config.getconfig('db_url'))

    context = 'something else'
    x = lambda context:hashstring(context)
    print(x(context))
