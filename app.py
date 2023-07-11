from flask import Flask,render_template,request,redirect
import json
from core.firebase import Firebase
from waitress import serve


app = Flask(__name__)
firebase = Firebase()

@app.route("/api/v1/carrier",methods=["POST"])
def get_carrier():
    data = json.loads(request.get_data().decode("utf-8"))
    try:
        lead = data["phone"]
        nxxnsx = get_nxxnsx(lead)
        carrier = firebase.get_carrier(nxxnsx)
        return "{'carrier':'"+carrier+"'}"
    except Exception as e:
        print(e)
        return "{'error':'bad request'}",500


def get_nxxnsx(lead):
    if lead[0] == "1": lead = lead[1:]
    phone = lead.replace(" ","").replace("+1","")
    phone = phone.replace("(","").replace(")","").replace("-","")
    return phone[:6]

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8100)