#!/usr/bin/python
import sys
# import logging
# logging.basicConfig(stream=sys.stderr)
# sys.path.insert(0,"/home/webdev/btsite/")

# from logging.handlers import RotatingFileHandler
from btsite import cncApp as cncApp
#
# handler = RotatingFileHandler('./tmp/error.log', maxBytes=100000, backupCount=2)
# handler.setLevel(logging.DEBUG)
#
# cncApp.logger.addHandler(handler)
cncApp.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
if __name__ == '__main__':
   context = ('cert.cert', 'key.key')
   cncApp.run(host='0.0.0.0', ssl_context=context, debug=True)
