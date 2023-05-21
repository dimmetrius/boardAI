import json

import quart
import quart_cors
from datetime import date
from quart import request
from loadmenu import load_menu

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")


@app.get("/menu/<string:schoolname>/<string:date>")
async def get_menus(schoolname, date):
    # Keep track of todo's. Does not persist if Python session is restarted.
    _MENUS = load_menu()
    _MENUS["menu_days"] = list(filter(lambda o: o["date"] == date, _MENUS["menu_days"]))
    return quart.Response(response=json.dumps(_MENUS), status=200)


@app.get("/logo.png")
async def plugin_logo():
    filename = "logo.png"
    return await quart.send_file(filename, mimetype="image/png")


@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers["Host"]
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")


@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers["Host"]
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")


def main():
    app.run(debug=True, host="0.0.0.0", port=5003)


if __name__ == "__main__":
    main()
