from fbfeed import fbfeed
import os

debug = __debug__
host = "0.0.0.0"
port = 9529

fbfeed.app.run(host=host, port=port, debug=debug, workers=os.cpu_count())