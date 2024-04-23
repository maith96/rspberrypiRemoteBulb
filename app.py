from flask import Flask, render_template, redirect, request
import requests

app = Flask(__name__)

authorized_user = {'username':'Johny', 'password': '12345'}
current_user = {}

@app.route("/system/<state>")
def system(state):
    if current_user != authorized_user:
        return redirect('/login')
    if state:
        try:
            # Replace with the IP address of your MicroPython server
            server_ip = "192.168.43.153"
            url = f"http://{server_ip}/?led={state}"

            # Send a GET request to the MicroPython server
            response = requests.get(url)

            # Check if the request was successful
            if response.status_code == 200:
                # Get the bulb state from the response content
                bulb_state = response.text
                print(bulb_state)
                # return bulb_state
                return render_template('index.html', bulb_state=bulb_state)
            else:
                return f"Error: {response.status_code}"

        except Exception as e:
            return f"Error: {e}"
    else:
        return redirect('/system/off')
    
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        print(request.form)
        if valid_login(request.form['username'],
                       request.form['password']):
            current_user = authorized_user
            return redirect('/system/off')
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)

def valid_login(username, password):
    return ((username == authorized_user['username']) and (password == authorized_user['password']))