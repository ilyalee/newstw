from crawler import crawler
import os

debug = __debug__
host = "0.0.0.0"
port = 9527

crawler.app.run(host=host, port=port, debug=debug, workers=os.cpu_count())
