#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    result = req.get("result")
    parameters = result.get("parameters")
    base_url = 'https://intuit.service-now.com/sp?id=search&t=&q='
    ln = len(parameters.values())
    ctr = 0
    for p in parameters.values():
        ctr += 1
        base_url += p
        if ctr != ln:
            base_url += '%20'
        else:
            base_url +='&search='
    #result = urlopen(base_url).read()
    #data = json.loads(base_url)
    res = makeWebhookResult(base_url)
    return res


def makeWebhookResult(data):
    return {
        "speech": data,
        "displayText": data,
        # "data": data,
        # "contextOut": [],
        "source": "buddy"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
