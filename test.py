#!/home/thomas/anaconda3/bin/python

"""
    # Author : Thomas Neuer (tneuer)
    # File Name : test.py
    # Creation Date : Fre 12 Okt 2018 19:52:28 CEST
    # Last Modified : Fre 12 Okt 2018 19:55:40 CEST
    # Description :
"""
#==============================================================================

import re
import numpy as np
import pandas as pd

from numpy import sqrt

class TestClass(AnotherClass,
second_class,    more_classes):
    """ asd
    sadad
    """

    def __init__(self, t, r=0):
        self.t = t
        self.p = None
        self.r = r
        self.t = 1
	a = self.method_1(3)

    def method_1(self, t,
baaad_code=42):
        """
        asdasdasd

        """
	return t

#TestComment1
def testFunction(a, b, c=0):
    """ Test
    Just a test
    """ #NotShown

    return 0, something

     #TestComment2

asdasd
"""
Comment
"""

def test2(bc=3,
    ak=4
   n, K="string"):
    if True:
        return False
    else:
        return True, blah

def test3(a):
    pass

def test4(
a, # Why the fuck put here a comment?
   asd=2, 
 #This is extremely ugly code!
asd
)
    return None

