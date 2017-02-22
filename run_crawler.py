from crawler import crawler

debug = __debug__
host = "0.0.0.0"

crawler.app.run(host=host, port=9527, debug=debug)
