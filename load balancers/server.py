from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/hello")
def hello():
    print(request.headers)
    return f"Hello from port {port}.\n"

if __name__ == "__main__":
    port = os.environ.get("PORT", 3000)
    app.run(host="0.0.0.0", port=port)