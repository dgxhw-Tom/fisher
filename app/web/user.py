import requests

from . import web
import time
from flask import request


@web.route('/', methods=["GET", "POST"])
def test():
    data = request.files['data']
    url = 'http://xhcjrich.search.datagrand.com:8000/pdf'
    files = {'data': data}

    r = requests.post(url, files=files)
    #
    print(r.json())
    return 'okkk'
