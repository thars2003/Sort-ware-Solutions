import subprocess
import threading
import time
from flask import Flask, render_template, Response, request, json, redirect, url_for,send_from_directory
from Computer_Vision import Magic, Pokemon
# from Computer_Vision import Led
app = Flask(__name__)
wifi_device = "wlan0"
# @app.before_first_request
# def start_led():
#     Led.run() 

@app.route("/")
def home():
    return render_template("home.html")

OUTPUT_FOLDER="/home/sortware/Documents/Sort-ware-Solutions/Output_Files"
@app.route("/download-csv")
def download_csv():
    filename = "magic-2026-03-12_21-25-34.csv"  # your existing CSV filename
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)

pause_event = threading.Event()
stop_event = threading.Event()

pause_event.clear()
stop_event.clear()

def card_sort_stream(sort_value):
    if not sort_value:
        return
    generator = None
    if sort_value.startswith("mtg"):
        generator = Magic.magic_main(sort_value)
    elif sort_value.startswith("pokemon"):
        generator = Pokemon.pokemon_main(sort_value)
    else:
        return
    for card in generator:
        # Wait if paused
        while pause_event.is_set():
            time.sleep(0.3)
        if stop_event.is_set():
            break
        yield f"data: {json.dumps(card)}\n\n"
@app.route("/stream")
def stream():
    sort_value = request.args.get("sort")
    stop_event.clear()
    return Response(card_sort_stream(sort_value), mimetype="text/event-stream")
@app.route("/pause", methods=["POST"])
def pause():
    pause_event.set()
    return "paused"
@app.route("/resume", methods=["POST"])
def resume():
    pause_event.clear()
    return "resumed"
@app.route("/stop", methods=["POST"])
def stop():
    stop_event.set()
    pause_event.clear()
    return "stopped"


@app.route("/wifi")
def wifi():
    # Force a rescan
    subprocess.run(["sudo", "nmcli", "device", "wifi", "rescan"], capture_output=True)

    # List available networks
    result = subprocess.check_output([
        "nmcli", "--colors", "no", "-m", "multiline",
        "--get-value", "SSID", "dev", "wifi", "list", "ifname", wifi_device
    ])
    ssids_list = result.decode().split('\n')

    dropdowndisplay = """
        <!DOCTYPE html>
        <html>
        <head><title>WiFi Setup</title></head>
        <body>
            <h1>WiFi Setup</h1>
            <form action="/wifi/connect" method="post">
                <label for="ssid">Choose a WiFi network:</label>
                <select name="ssid" id="ssid">
    """
    for ssid in ssids_list:
        only_ssid = ssid.removeprefix("SSID:")
        if len(only_ssid) > 0:
            dropdowndisplay += f'<option value="{only_ssid}">{only_ssid}</option>\n'

    dropdowndisplay += """
                </select>
                <p/>
                <label for="password">Password: <input type="password" name="password"/></label>
                <p/>
                <input type="submit" value="Connect">
            </form>
        </body>
        </html>
    """
    return dropdowndisplay


@app.route("/wifi/connect", methods=["POST"])
def wifi_connect():
    ssid = request.form["ssid"]
    password = request.form["password"]

    
    subprocess.run(
        ["sudo", "nmcli", "connection", "delete", ssid],
        capture_output=True, text=True
    )

    # Add fresh connection profile
    result = subprocess.run(
        [
            "sudo", "nmcli", "connection", "add",
            "type", "wifi",
            "ifname", wifi_device,
            "con-name", ssid,
            "ssid", ssid,
            "wifi-sec.key-mgmt", "wpa-psk",
            "wifi-sec.psk", password
        ],
        capture_output=True, text=True
    )

    if result.returncode != 0:
        return "Error adding connection: %s" % result.stderr

    # Activate the connection
    result2 = subprocess.run(
        ["sudo", "nmcli", "connection", "up", ssid],
        capture_output=True, text=True
    )

    if result2.returncode != 0:
        return "Error connecting: %s" % result2.stderr

    return """
        <!DOCTYPE html>
        <html>
        <head>
            <meta http-equiv="refresh" content="10;url=http://raspberrypi.local:5000">
        </head>
        <body>
            <h1>Connected!</h1>
            <p>The Pi is joining the WiFi network. Reconnect your phone to your WiFi now.</p>
            <p>You will be automatically redirected in 10 seconds...</p>
        </body>
        </html>
    """
if __name__ == "__main__":
    # app.run(debug=True, threaded=True)
    # app.run(host='10.248.222.234', port=5000, debug=True, threaded=True)
    app.run(host="0.0.0.0", port=5000, debug=False)