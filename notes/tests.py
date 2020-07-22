# from django.test import TestCase
#
# # Create your tests here.

import datetime

s = "qqqq:||" + str(datetime.datetime.now().microsecond) + "||qqq"
a = s.split("||")
# b = s.split("}")
print(a[0]+a[2])
# print(b)