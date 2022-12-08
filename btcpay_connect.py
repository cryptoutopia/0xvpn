from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import select
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from btcpayPython.btcpay import BTCPayClient
from sqlalchemy.orm import Session
from base64 import b64encode
import pickle


B = declarative_base()

class Btcpay(B):
    __tablename__ = "btcpay"

    pickle = Column(Text, primary_key=True)

'''
class Wireguard(B):
    _tablename = "wireguard"
    pickle = Column(Text)
'''


e = create_engine("sqlite:///wgConManWeb/settings.sqlite3", echo=True, future=True)
B.metadata.create_all(e)

session = Session(e)
stmnt = select(Btcpay)

try:
    row = session.scalars(stmnt).one()
    c = input("BTCPayServer is likely paired already, do you wish to recreate the pairing? [y/n]")
    if c != "y":
        exit(0)

    session.delete(row)
    session.commit()

except:
    print("Creating database")


_host = input("Ented BTCPayServer URL: ")
_code = input("Enter pairing code from BTCPayServer: ")

client = BTCPayClient.create_client(
    host=_host, 
    code=_code
)
    
pickled = pickle.dumps(client)
pickled = b64encode(pickled).decode()

with Session(e) as s:
    
    bpay = Btcpay(
        pickle = pickled
    )

    s.add_all([bpay])
    s.commit()



