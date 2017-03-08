from archiver import news_archive

debug = __debug__
host = "0.0.0.0"
port = 9530

news_archive.app.run(host=host, port=port, debug=debug)
