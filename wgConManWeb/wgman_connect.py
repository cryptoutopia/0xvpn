from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import select
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

from sqlalchemy.orm import Session
from base64 import b64encode
import pickle

from wgConManWeb.wgConManWeb import settings

'''
B = declarative_base()

class Wireguard(B):
    _table = "wireguard"
    pickle = Column(Text)

class Btcpay(B):
    __tablename__ = "btcpay"
    pickle = Column(Text, primary_key=True)


e = create_engine("sqlite:///settings.sqlite3")
B.metadata.create_all(e)
session = Session(e)
stmnt = select(Wireguard)

'''

print("WAN_LINK")

'''
 SHOULD BE SORT OF INSTALLER BUT LAZY RN
 I HIDE THE WIREGUARD INSTALLATION INSIDE THE MIDDLEWARE FOR NOW
 PICKLE IT INSIDE A DB ... 
'''

