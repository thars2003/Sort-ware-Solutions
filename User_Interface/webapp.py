import subprocess
import threading
import time
from flask import Flask, render_template, Response, request, json, redirect, url_for,send_from_directory
from Computer_Vision import Magic, Pokemon
from Controls import dispenser
# from Computer_Vision import Led
app = Flask(__name__)
wifi_device = "wlan0"


@app.route("/")

def home():
    return render_template("home.html")
def boot_buzzer():
    import lgpio
    import time
    

    BUZZER_PIN = 20
    # Ensure melody and durations are accessible (passed in or defined)
    melody = [523, 659, 784, 1047]  # C5, E5, G5, C6
    durations = [0.1, 0.1, 0.1, 0.3]

    h_buzz = lgpio.gpiochip_open(0)
    
    try:
        lgpio.gpio_claim_output(h_buzz, BUZZER_PIN)

        for freq, dur in zip(melody, durations):
            # Start the tone
            lgpio.tx_pwm(h_buzz, BUZZER_PIN, freq, 50)
            time.sleep(dur)
            
            # Silence the buzzer by forcing the pin LOW 
            # This is cleaner than duty 0 for preventing screeching
            lgpio.tx_pwm(h_buzz, BUZZER_PIN, freq, 0) 
            lgpio.gpio_write(h_buzz, BUZZER_PIN, 0)
            time.sleep(0.03)
            
    except Exception as e:
        print(f"Buzzer Error: {e}")
    
    finally:
        # Cleanup: Ensure pin is LOW and released
        lgpio.gpio_write(h_buzz, BUZZER_PIN, 0)
        lgpio.gpio_free(h_buzz, BUZZER_PIN)
        lgpio.gpiochip_close(h_buzz)
    dispenser._get_bin_motor().disable()
    print("disabled")
    dispenser._get_dispense_motor().disable()


threading.Thread(target=boot_buzzer, daemon=True).start()

OUTPUT_FOLDER="/home/sortware/Documents/Sort-ware-Solutions/Output_Files"
@app.route("/download-csv")
def download_csv():
    filename = "sortware_export.csv"  # your existing CSV filename
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)


@app.route('/wifi-status')
def wifi_status():
    result = subprocess.run(
        ['nmcli', '-t', '-f', 'ACTIVE,SSID', 'dev', 'wifi'],
        capture_output=True, text=True
    )
    for line in result.stdout.splitlines():
        if line.startswith('yes:'):
            ssid = line.split(':', 1)[1]
            return json.jsonify({'connected': True, 'ssid': ssid})
    return json.jsonify({'connected': False, 'ssid': ''})
 
 
 
pause_event = threading.Event()
stop_event = threading.Event()

pause_event.clear()
stop_event.clear()

def card_sort_stream(sort_value):
    if not sort_value:
        return
    # stop_event.clear() #change
    generator = None
    if sort_value.startswith("mtg"):
        generator = Magic.magic_main(sort_value, pause_event, stop_event)
    elif sort_value.startswith("pokemon"):
        generator = Pokemon.pokemon_main(sort_value)
    else:
        return
    for card in generator:
        # Wait if paused
        while pause_event.is_set():
            time.sleep(0.3)
        if stop_event.is_set():
            yield f"event: stop\ndata: {{}}\n\n"
            break
        yield f"data: {json.dumps(card)}\n\n"

@app.route("/stream")
def stream():
    sort_value = request.args.get("sort")
    if stop_event.is_set():          # ← frontend reconnected after stop, reject it
        return Response("", mimetype="text/event-stream")
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
@app.route("/start", methods=["POST"])
def start():
    stop_event.clear()
    pause_event.clear()
    return "started"


@app.route('/calibrate/left', methods=['POST'])
def calibrate_left():
    dispenser._get_bin_motor().enable()
    dispenser.step_clockwise(dispenser._get_bin_motor(), calibrate=False)
    dispenser._get_bin_motor().disable()
    return '', 204

@app.route('/calibrate/right', methods=['POST'])
def calibrate_right():
    dispenser._get_bin_motor().enable()
    dispenser.step_counterclockwise(dispenser._get_bin_motor(),calibrate=True)
    dispenser._get_bin_motor().disable()
    return '', 204


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