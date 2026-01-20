from flask import Flask, render_template, Response, request, json
from Computer_Vision import Magic, Pokemon

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("test.html")


@app.route("/stream")
def stream():
    sort_value = request.args.get("sort")

    def event_stream():
        if not sort_value:
            return

        if sort_value.startswith("mtg"):
            for card in Magic.magic_main():
                yield f"data: {json.dumps(card)}\n\n"

        elif sort_value.startswith("pokemon"):
            for card in Pokemon.pokemon_main():
                yield f"data: {json.dumps(card)}\n\n"

    return Response(event_stream(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
