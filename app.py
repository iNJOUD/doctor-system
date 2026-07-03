from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

data = {
    "doctors": [],
    "shifts": []
}


# ---------------- ADD DOCTOR ----------------
@app.route("/add_doctor", methods=["POST"])
def add_doctor():
    name = request.form["name"]
    role = request.form["role"]

    data["doctors"].append({
        "name": name,
        "type": role,
        "vacations": [],
        "assigned": 0,
        "last": None
    })

    return redirect("/")


# ---------------- VACATION ----------------
@app.route("/add_vacation", methods=["POST"])
def add_vacation():
    name = request.form["name"]
    start = request.form["start"]
    end = request.form["end"]

    for d in data["doctors"]:
        if d["name"] == name:
            d["vacations"].append({
                "start": start,
                "end": end
            })

    return redirect("/")


# ---------------- GENERATE ----------------
@app.route("/generate")
def generate():
    data["shifts"] = []

    start_date = request.args.get("start")
    days = int(request.args.get("days"))

    start = datetime.strptime(start_date, "%Y-%m-%d")

    for i in range(days):
        date = start + timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")

        shift = {
            "date": date_str,
            "ER": [],
            "Ward": [],
            "Supervisor": []
        }

        # Supervisor
        seniors = [d for d in data["doctors"] if d["type"] == "senior"]
        if seniors:
            shift["Supervisor"].append({
                "name": seniors[0]["name"],
                "role": "Supervisor"
            })

        # Juniors
        juniors = [d for d in data["doctors"] if d["type"] == "junior"]

        er_count = 0
        ward_done = False

        for j in juniors:
            if er_count < 2:
                shift["ER"].append({"name": j["name"], "role": "ER"})
                er_count += 1
            elif not ward_done:
                shift["Ward"].append({"name": j["name"], "role": "Ward"})
                ward_done = True

        data["shifts"].append(shift)

    return redirect("/")


# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html", data=data)


if __name__ == "__main__":
  if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)