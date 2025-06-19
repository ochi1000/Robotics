from flask import Flask, request
from easygopigo3 import EasyGoPiGo3
import time
from flask_cors import CORS

gpg = EasyGoPiGo3()
app = Flask(__name__)
CORS(app)

@app.route('/control', methods=['POST'])
def control():
    cmd = request.json.get('command')
    duration = float(request.json.get('duration', 3))
    
    if cmd == "forward":
        gpg.forward()
    elif cmd == "backward":
        gpg.backward()
    elif cmd == "left":
        gpg.left()
    elif cmd == "right":
        gpg.right()
    elif cmd == "stop":
        gpg.stop()
    else:
        return {"error": "Invalid command"}, 400
    
    if cmd != "stop":
        time.sleep(duration)
        gpg.stop()
    
    return {"status": "OK"}

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
    