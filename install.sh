#!/bin/bash

fn_installPythonReq() {
    pip install -r requirements.txt
}

fn_setupDjangoApp() {
    cd wgConManWeb && npm install && python3 manage.py makemigrations && python3 manage.py migrate
}

fn_connectBTCPay() {
    cd ..
    python3 btcpay_connect.py
}

fn_instrequirements() {

    #npm
    if ! command -v npm &> /dev/null
    then
        echo "npm is not installed"
        exit
    fi

    #pip
    if ! command -v pip &> /dev/null
    then
        echo "pip is not installed"
        exit
    fi

    #python
    if ! command -v python3 &> /dev/null
    then
        echo "python is not installed"
        exit
    fi

    echo "Requirements ... OK"
}

echo "
+-+-+-+-+-+-+ +-+ +-+-+-+-+-+-+-+-+-+
|b|i|t|v|p|n| |-| |i|n|s|t|a|l|l|e|r|
+-+-+-+-+-+-+ +-+ +-+-+-+-+-+-+-+-+-+
"
echo "Installing requirements .... "
fn_instrequirements
fn_installPythonReq
fn_setupDjangoApp
fn_connectBTCPay




