#!/bin/bash

curl -c ckies.json -L http://127.0.0.1:8000/bitvpn/checkout >> /tmp/garbage
curl -b ckies.json -L http://127.0.0.1:8000/bitvpn/payment_done >> /tmp/garbage
curl -b ckies.json -L http://127.0.0.1:8000/bitvpn/summary > /tmp/garbage

