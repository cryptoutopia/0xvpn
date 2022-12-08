from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
import sys
import os

def index(request):
    wg = request.wg
    connections = wg.status()

    template = loader.get_template("bitvpn/index.html")
    return HttpResponse(
            template.render({
                "connections": connections
            },
            request
        )
    )