from archiver import news_archive

debug = __debug__
host = "0.0.0.0"
port = 9530

# workaround: set workers to 1
news_archive.app.run(host=host, port=port, debug=debug, workers=1)
