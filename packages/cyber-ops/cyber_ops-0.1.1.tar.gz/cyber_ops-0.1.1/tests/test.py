# tests/test.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cyber_ops import yap

a = 2 + 4
def say_hey():
    yap("hey")
# Your test code
yap("Hello", "World")
yap("custom print")
say_hey()
yap(a)
print(a)