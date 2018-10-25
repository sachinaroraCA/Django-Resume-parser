from automationCTI.automationfx import *
from example_tests import SimpleCallTest

p1 = findPhone(Phone.DN == '50005')
p2 = findPhone(Phone.DN == '10136')


SimpleCallTest(p1, p2, 5)

