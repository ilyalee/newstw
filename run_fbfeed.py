from fbfeed import fbfeed

debug = __debug__
host = "0.0.0.0"

fbfeed.app.run(host=host, port=9529, debug=debug)
