from flask import Flask, render_template, Response, request, json
from Computer_Vision import Magic, Pokemon
from Computer_Vision import Led
app = Flask(__name__)

@app.before_first_request
def start_led():
    Led.run() 

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/stream")
def stream():
    sort_value = request.args.get("sort")
    def event_stream():
        if not sort_value:
            return

        if sort_value.startswith("mtg"):
            for card in Magic.magic_main(sort_value):
                yield f"data: {json.dumps(card)}\n\n"

        elif sort_value.startswith("pokemon"):
            for card in Pokemon.pokemon_main(sort_value):
                yield f"data: {json.dumps(card)}\n\n"

    return Response(event_stream(), mimetype="text/event-stream")


if __name__ == "__main__":
    #app.run(debug=True, threaded=True)
    app.run(host='10.248.222.234', port=5000, debug=True, threaded=True)
