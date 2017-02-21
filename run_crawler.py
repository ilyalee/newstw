from crawler import crawler

debug = True
host = "0.0.0.0"

crawler.app.run(host=host, port=9527, debug=debug)
