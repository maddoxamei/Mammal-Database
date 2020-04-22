from flask import (Flask, render_template)
app = Flask(__name__)

from threading import Lock

app.secret_key = 'your string here'

lock = Lock()

# shared global; need to control access
numVisits = 0

@app.route('/')
def count():
    global numVisits
    lock.acquire()
    tmp = numVisits
    tmp += 1
    numVisits = tmp
    lock.release()
    return render_template('layout.html')

def start():
    subprocess.call("run.bat")

if __name__ == '__main__':
    import sys, os
    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        #port = os.getuid()
        pass;
    app.debug = True
    app.run()
    #app.run('0.0.0.0',port)
