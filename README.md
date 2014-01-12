naivetools
==========

Simple, straightforward Python tools for configuring, logging and other common tasks

NaiveLog
--------

NaiveLog allows you to instantly get a logger that logs to stdout or stderr
and can be reconfigured on the fly

Start your module with

```python
from naivetools import naiveLog

log = naiveLog.naiveLog()
#or
log = naiveLog.naiveLog(name='myLog', level='DEBUG', target='stderr')
```

and you can log immediately with the usual python logging commands

```python
log.debug(...)
log.info(...)
log.warning(...)
log.error(...)
log.critical(...)

try:
  ...
except:
  log.exception(...)
```

The output will look like
    2014-01-12 11:36:47,642    ERROR [ 10669             test.<module>            :   6] Something is wrong

With date, time, log level, PID, module and function, line and message

NaiveConf
---------

NaiveConf initializes a configuration object from Python files or strings
and allows accessing parameters as attributes.

*WARNING !!!Use this only if you control all the configuration files,
since arbitraty code could be executed!!!*

For example, you can define _configuration file_ as simple Python code:

```python
import datetime

def f(var):
    return str(var)

x = datetime.datetime(2013,1,1).date()
y = f(x)

L = [1,2,3, {'a': None}]
```

and then initialize and access a configuration object as

```python
from naivetools import naiveConf
conf = naiveConf.NaiveConf('/path/to/conf.py')

print conf.x
conf.e = 100

assert conf['x'] == conf.x

for key, value in conf.items():
    print key, value

conf.required('x')
conf.required('L', 'Parameter L must be defined')

conf.default('Z', 5)
#If Z is not defined yet as a parameter, set it to 5
assert conf.Z == 5

conf.defaultNones(['e', 'f'])
#define e and f ans set them to None

conf.requiredAny(['f', 'g'], 'Either f or g or both must be defined')
#At least parameter must be defined

dConf = conf.getConf()
#Get a (shallow) copy of conf

dDict = conf.getConfDict()
#Get a dictionary of conf parameters

#Other ways to initialize
aConf = naiveConf.NaiveConf()
bConf = naiveConf.NaiveConf({'x': 5, 'f': None, 'li': [1,2,3]})
assert bConf.f is None

sConf = naiveConf.NaiveConf("a=5; b='g'")
assert sConf.b == 'g'

cConf = naiveConf.NaiveConf(bConf)
bConf.li[2] = 9
assert cConf.li == [1,2,9]
```