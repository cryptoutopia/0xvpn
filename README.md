# Huh
Lets you sell VPN using wireguard + btcpayserver.

# Installation
On debian 11 or newer just run ./install.sh. 
THen follow the setup with nginx -> @TODO

# python 3.9+, openssl needs to enable old cryptos
https://stackoverflow.com/questions/69922525/python-3-9-8-hashlib-and-ripemd160

# TODO
   * save peers to DB and just add them on the fly & delete them on the fly, see wgman add fnc
   * start/pare wireguard with systemd
   * lightning payments
   * distribution as a docker image
   * fix btcpayPython SSL bug on new system, add a dependency for 
   some ripemd library ... 
   * browser setup



# HOWTOS

## route incomming traffic through selected interface

### create a route
```bash
echo 200 <table_name> >> /etc/iproute2/rt_tables
ip rule add from <wireguard_client_ip> table <table_name>
ip route add default via <vpn_client_ip> dev <link> table <table_name>
```


### firewall rules (iptables)

```bash
iptables -A POSTROUTING -o <selected_interface> -j MASQUERADE
iptables -A FORWARD -i <wireguard_server_interface> -j ACCEPT
iptables -A FORWARD -m state --state RELATED,ESTABLISHED -j ACCEPT
```

** Enable forwarding: **  `echo 1 > /proc/sys/net/ipv4/ip_forward`

 - test with tshark, tcpdump or vpn client .. 





