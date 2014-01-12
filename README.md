naivetools
==========

Simple, straightforward Python tools for configuring, logging and other common tasks


NaiveConf
---------

NaiveConf initializes a configuration object from Python files or strings
and allows accessing parameters as attributes.

*WARNING !!!Use this only if you control all the configuration files,
since arbitraty code could be executed!!!

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