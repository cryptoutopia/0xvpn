from curses.ascii import HT
from urllib.request import Request
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.template import loader
from django.conf import settings
from requests import request
from bitvpn.models import BtcPay
from btcpayPython.btcpay import BTCPayClient
from base64 import b64decode
from bitvpn.models import Client
import datetime
import segno
import pickle
import json
import sys
import os
sys.path.append("../")
import wgman

PAYMENTOK = ["settled", "processing", "paid", "confirmed"]
EXPIRED = ["expired"]

def verify_payment(request, invoice_id):
    
    if not invoice_id:
        return False
    
    status = request.session.get("invoice_status")
    if status in PAYMENTOK:
        return status

    try:  
        bp = request.bpay
        status = bp.get_invoice(invoice_id)["status"]

        request.session["invoice_status"] = status
        
        if status in PAYMENTOK:
            return status

        return False

    except Exception as e:
        return False

def index(request):
    return redirect("/bitvpn/checkout")

def checkout(request):
    template = loader.get_template("bitvpn/checkout.html")
    invoice_id = request.session.get("invoice_id", False)
    invoice_status = verify_payment(request, invoice_id)

    if invoice_status in EXPIRED:
        request.session.flush()
        return redirect("/")

    if invoice_status in PAYMENTOK:
        return redirect("summary")

    if invoice_status not in PAYMENTOK and invoice_id:

        request.session["counter"] = int(request.session.get("counter", 1)) + int(1)
        btcqr = segno.make(
            "bitcoin: " +
            str(request.session.get("bitcoinAddress")) +
            "?amount=" +
            str(request.session.get("amount"))
        )

        data = {
            "bitcoinAddress": request.session.get("bitcoinAddress"),
            "btcPrice": request.session.get("amount"),
            "paymentUrl": "bitcoin://" + request.session.get("bitcoinAddress") + "?amount=" + request.session.get("amount"),
            "btcqr": btcqr.svg_inline(scale=10),
            "lnqr": segno.make("lighting invoice").svg_inline(scale=10)
        }

        return HttpResponse(template.render(data, request))

    try:
        bp = request.bpay
        new_invoice = bp.create_invoice({"price": 1, "currency": "EUR"})

        request.session["lnaddr"] = "NONE"                                  # LN is not yet supported
        request.session["bitcoinAddress"] = new_invoice["bitcoinAddress"]
        request.session["url"] = new_invoice["url"]
        request.session["amount"] = new_invoice["btcPrice"]
        request.session["invoice_id"] = new_invoice["id"]
        request.session["invoice_token"] = new_invoice["token"]
        request.session["invoice_expiration"] = new_invoice["expirationTime"]
        request.session["counter"] = 1

        btcqr = segno.make(
            "bitcoin: " +
            str(request.session.get("bitcoinAddress")) +
            "?amount=" +
            str(request.session.get("amount"))
        )

        data = {
            "bitcoinAddress": request.session.get("bitcoinAddress"),
            "btcPrice": request.session.get("amount"),
            "paymentUrl": "bitcoin://" + request.session.get("bitcoinAddress") + "?amount=" + request.session.get("amount"),
            "btcqr": btcqr.svg_inline(scale=10),
            "lnqr": segno.make("lighting invoice").svg_inline(scale=10)
        }

        return HttpResponse(template.render(data, request))

    except Exception as e:
        return HttpResponse(json.dumps({"error": "error occured, please come back later"}))

def summary(request):

    invoice_id = request.session.get("invoice_id")
    invoice_status = verify_payment(request, invoice_id)

    template = loader.get_template("bitvpn/summary.html")

    if invoice_id and invoice_status:
        request.session.flush()

        txt = ""
        cfg = ""

        try:

            wg = request.wg
            txt, cfg, _pubkey = wg.add()

            data = {
                "status": PAYMENTOK[0],
                "txtcfg": txt,
                "qr": segno.make(txt).svg_inline(scale=10),
                "zip": "Zip file"       
            }

            # save client to database
            _ip = cfg["Interface"]["Address"]
            _expir = (datetime.datetime.today() + datetime.timedelta(days=30)).date()
            _c = Client(ip=_ip, public_key=_pubkey, expiration=_expir)
            _c.save()

            return HttpResponse(template.render(data, request))
        except Exception as e:
            return
        

    elif invoice_id and not invoice_status:
        return HttpResponse(template.render({"status": False, "error": "Please pay the invoce first."}, request))
    else:
        return HttpResponse(template.render({"status": False, "error": "Please make your order first"}, request))

# verify if invoce has been payed
def payment(request):
    if not request.session.get("invoice_id"):
        return HttpResponse(json.dumps("no invoice"))
    elif verify_payment(request, request.session["invoice_id"]):
        return HttpResponse(json.dumps("invoice payed"))
    else:
        return HttpResponse(json.dumps("invoice not payed"))

def api_checkout(request):
    pass

def api_summary(request):
    pass