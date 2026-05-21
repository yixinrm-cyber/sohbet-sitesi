from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.secret_key = "gizli_anahtar"   # session için gerekli
socketio = SocketIO(app)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/setname", methods=["POST"])
def setname():
    session["username"] = request.form["username"]
    return redirect("/chat")

@app.route("/chat")
def chat():
    if "username" not in session:
        return redirect("/")
    return render_template("chat.html", username=session["username"])

@socketio.on("message")
def handle_message(msg):
    username = session.get("username", "Anonim")
    send(f"{username}: {msg}", broadcast=True)

if __name__ == "__main__":
    socketio.run(app, debug=True, host="127.0.0.1", port=8080)
