from newsfeed import newsfeed

debug = True
host = "0.0.0.0"

newsfeed.app.run(host=host, port=9528, debug=debug)
