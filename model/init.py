# ...
# from app import routes, models, errors

#!/usr/bin/env python
#encoding=utf8
"""
model/__init__.py contains the table definitions, the ORM classes and an init_model() function. 
This init_model() function must be called at application startup. 
"""
from model.init import *
from model.setting import *
# from model.meta import Session, Base

# from model.footwear import Footwear, FootwearType
# from model.vendor import Vendor
# from model.page import Page
# from model.user import User
# from model.setting import Setting
# from model.whitesite import Whitesite
# from model.shop import Shop, Shoplink
