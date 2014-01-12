##############
# NaiveConf is a simple way to pass a configuration
# to your app. The config file is a python file
# with configuration parameters assigned to variables
# The config file can contain executable Python code
#
# WARNING Use this only if you control all the config files
# Since they may contain executable code
#
##############

import copy
import os.path
import types

class NaiveConf(object):

    def __init__(self, src=None):

        if src is None:
            pass
        elif type(src) == str:
            #See if it could be a string containing code/configuration
            if src.find("=") > -1:
                self.initFromString(src)
            else:
                self.initFromFile(src)
        elif type(src) == dict:
            self.__dict__.update(src)
        elif hasattr(src, 'getConfDict'):
            self.__dict__.update(src.getConfDict())
        else:
            raise NotImplementedError(
                'Conf must be initialized with None, %s, filename, string or dict, not %s' %
                (self.__class__.__name__, type(src)))

        #We don't want to keep imports, class definitions
        # and functions around
        for k in self.__dict__.keys():
            if type(self.__dict__[k]) in [types.ModuleType,
                                          types.ClassType,
                                          types.FunctionType]:
                del self.__dict__[k]

    def initFromString(self, srcString):
        exec srcString in self.__dict__


    def initFromFile(self, filename):
        with file(filename) as inFile:
            srcString = "".join(inFile.readlines())
        self.initFromString(srcString)


    def default(self, name, value=None):
        """Define a default value for a variable that has not been set
        """
        if name not in self.__dict__:
            self.__dict__[name] = value


    def defaultNones(self, names):
        """Define all values in name slist as None
        """
        for name in names:
            self.default(name)


    def required(self, name, errorString=''):
        """Check that a required variable has been configured
        """
        if name not in self.__dict__:
            if not errorString:
                errorString = 'Required variable %s not defined' % name
            raise ValueError(errorString)


    def requireAny(self, names, errorString=''):
        """Check that at least one required variable has been configured
        """

        if not any([name in self.__dict__ for name in names]):
            if not errorString:
                errorString = 'At least variable from %s must be defined' % names
            raise ValueError(errorString)


    def __copy__(self):
        confDict = self.__dict__.copy()
        if '__builtins__' in confDict:
            confDict.pop('__builtins__')
        return confDict

    def getConfDict(self):
        return self.__copy__()

    def getConf(self):
        return NaiveConf(self.__copy__())

    def __repr__(self):
        def shortenValue(v):
            v = repr(v)
            if len(v)>97:
                v = v[:45] + " (...) " + v[-45:]
            return v
        confDict = self.getConfDict()
        return "{" + "\n".join("%s: %s" % (k, shortenValue(v))
                               for k, v in sorted(confDict.items())) + "}"

    def __contains__(self, x):
        return x in self.__dict__

    def __setitem__(self, key, value, **args):
        self.__dict__.__setitem__(key, value, **args)

    def __getitem__(self, key, **args):
        return self.__dict__.__getitem__(key, **args)

    def __delitem__(self, key):
        del self.__dict__[key]

    def __eq__(self, other):
        if type(other) != NaiveConf:
            return False
        for key, value in self.__dict__.items():
            if key == '__builtins__':
                continue
            if key not in other or \
              value != other[key]:
              return False
        return True

    def __iter__(self):
        return self.__dict__.__iter__()

    def __len__(self):
        return len(self.__dict__) - 1 #ignore __builtins__

    def __getattr__(self, attr):
        if attr in ['items', 'keys', 'values', 'update']:
            return getattr(self.__dict__, attr)
        else:
            return self.__getitem__(attr)
