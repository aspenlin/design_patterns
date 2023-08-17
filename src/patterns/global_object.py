"""
Global Object Pattern
- A module instantiates an object at import time and assigns it a name in the module's global space

Advantages:
- Efficiency: no need to compute multiple times
- Readability: give name to magic numbers etc.

Drawback:
- The cost of importing the module increases
- Couple distant parts of your codebase, and even unrelated parts of different libraries
- Many of the worst Global Objects are those that perform file or network I/O at import time
"""
# The Constant Pattern
import calendar
import re
import os

print(calendar.January)
calendar.January = 12 # Bad: This constant value can be changed by any client
print(calendar.January)

# The Global Object Pattern
magic_check = re.compile('([*?[])') # In glob.py, now no need to compile multiple times in the code
os.environ['TERM'] = 'xterm' # Bad, this is now immediately visible to any other part of the program that reads the key