import datetime
import inspect
import os
import pytest
import datetime
from naivetools import naiveConf

exampleConfFname = os.path.join(
    os.path.split(inspect.getfile(inspect.currentframe()))[0], "exampleConf.py")

def testInitConfFromFile():
    """Initialize configuration from a file
    """

    conf = naiveConf.NaiveConf(exampleConfFname)
    assert type(conf.x) == datetime.date
    assert type(conf.y) == str
    dt = datetime.datetime(2013,1,1)
    assert conf.x == dt.date()
    assert conf.y == str(dt.date())

    assert type(conf.L) == list
    assert conf.L[-1]['a'] is None

    assert conf.x == conf['x']

def testInitConfFromString():
    """Initialize from a string
    """

    testString = "x=5;b='hallo'"
    conf = naiveConf.NaiveConf(testString)

    assert conf.x == 5
    assert conf.b == 'hallo'

def testInitFromDict():
    """Test initialization from a dictionary
    """
    conf = naiveConf.NaiveConf({})
    conf = naiveConf.NaiveConf({'a':5})
    assert conf.a == 5

def testInitEmpty():
    """Build an empty configuration
    """
    conf = naiveConf.NaiveConf()
    with pytest.raises(KeyError):
        print conf.x
    conf.x = 5
    assert conf.x == 5

def testInitFail():
    """Testing building a config with an invalid object
    """
    with pytest.raises(NotImplementedError):
        naiveConf.NaiveConf([1,2,3])
    with pytest.raises(NotImplementedError):
        naiveConf.NaiveConf(0)

def testInitFromNaiveConf():
    """Testing building a conf from another conf
    """
    conf = naiveConf.NaiveConf(exampleConfFname)
    dConf = naiveConf.NaiveConf(conf)
    assert conf == dConf
    conf['x'] = None
    assert type(dConf.x) == datetime.date

def testDefault():
    """The default function assigns a parameter
    if it hasn't been defined
    """

    conf = naiveConf.NaiveConf(exampleConfFname)
    oldX = conf.x
    conf.default('x', None)
    conf.default('Z', 5)

    assert conf.x == oldX
    assert conf.Z == 5

def testDefaultNones():
    """The defaultNones function calles default
    on a list of parameters and sets them to None
    """

    conf = naiveConf.NaiveConf(exampleConfFname)
    conf.defaultNones(['x', 'Z'])
    assert type(conf.x) == datetime.date
    assert conf.Z is None

def testRequired():
    """The required function defines parameters that must be
    specified by the user
    """

    conf = naiveConf.NaiveConf(exampleConfFname)
    conf.required('x')
    with pytest.raises(ValueError):
        conf.required('Z')
    try:
        testMessage = 'This went wrong'
        conf.required('Z', testMessage)
    except ValueError as e:
        assert e.message == testMessage

def testRequireAny():
    """"Check if at least one of the variables in a list
    has been defined
    """
    conf = naiveConf.NaiveConf(exampleConfFname)
    conf.requireAny(['x', 'Z', 'abcdf'])
    with pytest.raises(ValueError):
        conf.requireAny(['Z'])

def testAssignment():
    """Testing getting and setting items
    """

    conf = naiveConf.NaiveConf(exampleConfFname)
    conf.x1 = conf.x
    conf['x2'] = conf.x
    conf.x3 = conf['x']
    conf['x4'] = conf['x']

    assert conf.x == conf['x']
    assert conf.x1 == conf['x1']
    assert conf.x2 == conf['x2']
    assert conf.x3 == conf['x3']
    assert conf.x4 == conf['x4']
    assert conf.x1 == conf.x
    assert conf['x1'] == conf['x']
    assert conf.x2 == conf.x
    assert conf.x3 == conf.x
    assert conf.x4 == conf.x

    del conf.x4
    with pytest.raises(KeyError):
        print conf.x4

def testGetConf():
    """Test that getConf returns a (shallow) copy
    of the Conf
    """

    conf = naiveConf.NaiveConf(exampleConfFname)

    copyConf = conf.getConf()
    assert conf == copyConf

    copyConf.x = None
    assert copyConf.x is None

def testGetConfDict():
    """getConfDict returns a dictionary of the
    configuration
    """

    conf = naiveConf.NaiveConf(exampleConfFname)
    confDict = conf.getConfDict()
    assert type(confDict) == dict
    assert confDict['x'] == conf.x
    assert confDict['y'] == conf.y
    assert confDict['L'] == conf.L

def testIterate():
    """Test dictionary iterations on NaiveConf
    """
    conf = naiveConf.NaiveConf(exampleConfFname)
    for k, v in conf.items():
        pass
    for k in conf:
        pass
    for k in conf.keys():
        pass
    for v in conf.values():
        pass
    conf.update({'x': 6})
    assert conf.x == 6
    assert len(conf) == 3
