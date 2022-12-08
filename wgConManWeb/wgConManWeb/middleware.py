from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from bitvpn.models import BtcPay
from bitvpn.models import Wgman
from btcpayPython.btcpay import BTCPayClient
from bitvpn.models import Client
from django.conf import settings
from base64 import b64decode
import datetime
import pickle
import sys
sys.path.append("../")
import wgman


class BTCPayMiddleware(MiddlewareMixin):

    def process_request(self, request):
        try:
            bp = BtcPay.objects.using('bitvpn').first()
            bp = bp.pickle.encode()
            bp = b64decode(bp)
            bp = pickle.loads(bp)

            request.bpay = bp
        except Exception as e:
            print(e)
            return HttpResponse("Your app is likely not installed correctly, please check your logs.")


# not used for now
class WgManMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            bitvpnconf = {
                "name": getattr(settings, "WG_NAME", ""),
                "ip": getattr(settings, "WG_IP", ""),
                "port": getattr(settings, "WG_PORT", ""),
                "domain": getattr(settings, "WG_DOMAIN", ""),
                "postup": getattr(settings, "WG_POSTUP", ""),
                "postdown": getattr(settings, "WG_POSTDOWN", ""),
            }

            wg = wgman.WgConMan(bitvpnconf)
            if not wg.s_peers:
                clients = Client.objects.all().filter(expiration__gte=datetime.datetime.today())
                
                for client in clients:
                    wg.add_existing(
                        client.ip,
                        client.public_key
                    )
            else:
                print(wg.s_peers)

            request.wg = wg

        except Exception as e:
            print(e)
            return HttpResponse("Wireguard management up is not set up correctly")