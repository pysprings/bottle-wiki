import collections
import functools
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


class memoized(object):
    '''Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    '''
    def __init__(self, func):
       self.func = func
       self.cache = {}
    def __call__(self, *args):
        if not isinstance(args, collections.Hashable):
          # uncacheable. a list, for instance.
          # better to not cache than blow up.
          return self.func(*args)
        if args in self.cache:
          return self.cache[args]
        else:
          value = self.func(*args)
          self.cache[args] = value
          return value
    def __repr__(self):
       '''Return the function's docstring.'''
       return self.func.__doc__
    def __get__(self, obj, objtype):
       '''Support instance methods.'''
       return functools.partial(self.__call__, obj)


if __name__ == "__main__":
    config = Config()
    print(config['DATABASE']['db_url'])
