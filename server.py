from flask import Flask, request, Response
import requests as req
import re
import logging
from extract_mables_from_parzu import get_mables
from corzu import main as get_coref


class Server(object):
    def __init__(self, parzuport=5003):
        self.app = Flask('CorZuServer')
        self.parzuport = parzuport

        @self.app.route('/coref/', methods=['GET'])
        def coref():
            text = request.args.get("text", None)
            # parse with ParZu server
            r = req.get("http://localhost:{}/parse/".format(self.parzuport), params={"text": text})
            ret = re.sub("\n\n", "\n", r.text)
            #print(ret.split("\n"))
            parzulines = ret.split("\n")
            ret = get_mables(ret.split("\n"))
            #print(ret)
            ret = get_coref(ret, parzulines)
            return Response(ret, mimetype='text/plain')


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", "-p", type=int, default=5004,
                        help="Port number to listen to (default: 5004)")
    parser.add_argument("--parzuport", "-q", type=int, default=5003,
                        help="Port number to send requests for ParZu parser to (default:5003)")
    parser.add_argument("--host", "-H", help="Host address to listen on (default: localhost)")
    args = parser.parse_args()
    print(args)

    debug=False

    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO,
                        format='[%(asctime)s %(name)-12s %(levelname)-5s] %(message)s')

    server = Server(parzuport=args.parzuport)

    server.app.run(port=args.port, host=args.host, debug=debug, threaded=True)
