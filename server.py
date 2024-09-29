from index import layout
from app import app
from os.path import exists
import sys

debug = True if "--debug" in sys.argv else False

app.layout = layout
srv = app.server
app.title = "BlackDash"


if __name__ == "__main__":
    ssl_paths = "certs/fullchain.pem", "certs/privkey.pem"
    ssl_context = ssl_paths if all(exists(path) for path in ssl_paths) else None

    app.run_server(
        host="0.0.0.0",
        port=8079 if debug else 443,
        ssl_context=ssl_context if debug else None,
        debug=debug,
    )
