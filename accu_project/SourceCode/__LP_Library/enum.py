from enum import Enum

class LoginStatus(Enum):
  success = 1
  error   = 0
  invaild = -1

class AjaxResponseResult(Enum):
  success = 1
  error   = 0