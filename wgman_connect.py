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
import wgman

from wgConManWeb.wgConManWeb import settings


B = declarative_base()

class Wireguard(B):
    __tablename__ = "wireguard"
    pickle = Column(Text, primary_key=True)

e = create_engine("sqlite:///settings.sqlite3")
B.metadata.create_all(e)
session = Session(e)
stmnt = select(Wireguard)

print(settings.WAN_LINK)

bitvpnconf = {
            "name": "wgConManWeb/" + settings.WG_NAME,
            "ip": settings.WG_IP,
            "port": settings.WG_PORT,
            "domain": settings.WG_DOMAIN,
            "postup": settings.WG_POSTUP,
            "postdown": settings.WG_POSTDOWN,
}

try:
    wg = wgman.WgConMan(bitvpnconf)
    pickled = pickle.dumps(wg)
    pickled = b64encode(pickled).decode()

    with Session(e) as s:

        wireguard = Wireguard(
            pickle = pickled
        )

        s.add_all([wireguard])  
        s.commit()

except Exception as e:
    print("WARNING")
    print(e)

'''
 SHOULD BE SORT OF INSTALLER BUT LAZY RN
 I HIDE THE WIREGUARD INSTALLATION INSIDE THE MIDDLEWARE FOR NOW
 PICKLE IT INSIDE A DB ... 
'''

