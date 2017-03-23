from archiver import news_archive
import os
debug = __debug__
host = "0.0.0.0"
port = 9530
if debug:
    print("os.cpu_count()", os.cpu_count())
# workaround: set workers to 1
news_archive.app.run(host=host, port=port, debug=debug, workers=os.cpu_count())
