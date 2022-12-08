import configparser
from http import server
from http.client import CONFLICT
from shutil import which
import subprocess
import datetime
import argparse
import string
import random
import time
import sys
import os
import io
import re

import wgConManWeb.settings as settings

CONST_EXT = ".conf"

class WgConMan:
    def __init__(self, conf):
        self.s_name = conf.get("name", "wgbitvpn")
        self.s_ip = conf.get("ip", "10.10.10.1/32")
        self.s_port = conf.get("port", 51820)
        self.s_pk = conf.get("pk", self.gen_pk())
        self.s_pubk = conf.get("pubk", self.gen_pubk())
        self.s_postup = conf.get("postup", "echo e")
        self.s_postdown = conf.get("postdown", "echo e")
        self.s_domain = conf.get("domain", "vpn.lekaren.digital")
        self.s_peers = []

        if os.path.exists(self.s_name + CONST_EXT):
            config = configparser.ConfigParser(strict=False)
            config.optionxform = str
            config.read(self.s_name + CONST_EXT)

            server = config["Interface"]

            self.s_ip = server["Address"]
            self.s_port = server["ListenPort"]
            self.s_pk = server["PrivateKey"]
            self.s_pubk = self.gen_pubk()
            self.s_postup = server["PostUp"]
            self.s_postdown = server["PostUp"]
            self.s_domain = conf.get("domain", "vpn.example.com")

        if not os.path.exists(self.s_name + CONST_EXT):
            config = configparser.ConfigParser()
            config.optionxform = str
            config["Interface"] = {
                "Address": self.s_ip,
                "ListenPort": self.s_port,
                "PrivateKey": self.s_pk,
                "PostUp": self.s_postup,
                "PostDown": self.s_postdown
            }

            with open(self.s_name + CONST_EXT, "w") as f:
                config.write(f)
        
        self.readcnf()
        self.wgstart()
        self.peers()


    def readcnf(self):
        self.peers()
            
    def add(self):
        pk = self.gen_pk()
        pubk = self.gen_pubk(pk)
        ip = self.octet_to_ip(self.get_octet())
        dns = "8.8.8.8" # we can talk about this ... 

        self.wg_addcfg(ip, pubk)

        # client part
        cfg = configparser.ConfigParser()
        cfg.optionxform = str
        cfg["Interface"] = {
            "PrivateKey": pk,
            "Address": ip,
            "DNS": dns,
        }

        cfg['Peer'] = {
            'PublicKey': self.s_pubk,
            'AllowedIPs': "0.0.0.0/0," + self.s_ip,
            'EndPoint': self.s_domain + ":" + self.s_port
        }

        r = io.StringIO()
        cfg.write(r)

        self.readcnf()
        return r.getvalue(), cfg, pubk
    
    def wg_addcfg(self, ip="", pubk=""):
        ipcmd = which("ip")
        wgcmd = which("wg")

        server_interface = self.s_name.split('/')[-1]
        subprocess.run(f"{wgcmd} set {server_interface} peer {pubk} allowed-ips {ip}", shell=True)
        subprocess.run(f"{ipcmd} -4 route add {ip} dev {server_interface}", shell=True)
        
        # rout using this table, otherwise use WAN
        if hasattr(settings, 'ROUTING_TABLE'):
            subprocess.run(f"{ipcmd} rule add from {ip} table {settings.ROUTING_TABLE}", shell=True)
        
        #subprocess.run(f"{wgqcmd} save {os.path.abspath(server_interface)}" + CONST_EXT, shell=True)

    def remove(ipaddr):
        print(ipaddr)

    def wgstart(self):

        cmp = f"interface: {self.s_name.split('/')[-1]}"
        
        try:
            print(f"wg show | grep \"{cmp}\"")
            o = subprocess.check_output(f"wg show | grep \"{cmp}\"", shell=True).decode("utf-8").strip()
            if o != "": return True

        except subprocess.CalledProcessError as e:
            r = subprocess.check_output(
                "wg-quick up " + os.path.abspath(self.s_name) + CONST_EXT, shell=True
            )

    def gen_pk(self):
        pk = subprocess.check_output(
            "wg genkey", shell=True).decode("utf-8").strip()
        
        return pk

    def gen_pubk(self, pk=""):
        if not pk:
            pk = self.s_pk
        pubk = subprocess.check_output(
            f"echo {pk} | wg pubkey", shell=True).decode("utf-8").strip()
    
        return pubk

    def get_octet(self):
        ips = []
        x = 2
        MAX = 2**8 -2 -1

        for peer in self.s_peers:
            ip = peer['allowed-ips']
            ip = re.match(r"\d{1,3}.\d{1,3}.\d{1,3}.(\d{1,3})", ip)
            ips.append(int(ip.group(1)))

            print(ip.group(1))

        if len(ips) == MAX:
            return False
        
        ips.sort()
        for ip in ips:  
            if x != int(ip):
                break
            else:
                x = x + 1

        if x > 1 and x <= MAX:
            return x
        
        return False
    
    def octet_to_ip(self, octet):
        patt = (r"\d{1,3}\/\d{1,2}")
        repl = str(octet) + "/32"
        ip = self.s_ip

        return re.sub(patt, repl, ip)

    def randstr(self,length = 16):
        letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str

    def status(self):
        TD = 60 * 60
        connections = 0

        for s in self.s_peers:
            handshake = datetime.datetime.fromtimestamp(int(s['latest-handshake']))
            handshake = datetime.datetime.timestamp(handshake)
            if (time.time() - handshake) < TD:
                connections = connections + 1

        return connections
    
    def peers(self):
        server_interface = self.s_name.split('/')[-1]
        peers = subprocess.check_output(
                f"wg show {server_interface} dump",
                shell=True
            ).decode("utf-8")
        
        self.s_peers = peers.splitlines(keepends=False)[1:]
        
        parsed_peers = []
        for peer in self.s_peers:
            tmp = str(peer).split("\t")
            parsed_peers.append({
                'public-key': tmp[0],
                'preshared-key': tmp[1],
                'endpoint': tmp[2],
                'allowed-ips': tmp[3],
                'latest-handshake': tmp[4],
                'transfer-rx': tmp[5],
                'transfer-tx': tmp[6]
            })

        self.s_peers = parsed_peers
        return self.s_peers


    def dummy(self):
        s = "Dummy called"
        print(s)

        return s

if __name__ == "__main__":
    '''
    c = {
        "name": "wg0",
        "ip": "10.10.10.1/32",
        "port": "51820",
        "domain": "vpn.lekaren.digital",
        "postup": "iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o enp41s0 -j MASQUERADE",
        "postdown": "iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o enp41s0 -j MASQUERADE",
    }

    #p = argparse.ArgumentParser()
    #p.add_argument('-c', action='store', required=True, help='path to configuration')
    #p.add_argument('-a', action='store_true', required=False, help='add client')
    #p.add_argument('-d', action='store', required=False, help='delete client')
    #args = p.parse_args()

    wg = WgConMan(c)
    print(wg.add()[0])
    '''
