from flask import Flask, render_template, request, redirect
import pandas as pd

app = Flask(__name__)

FILE = "data/Daily Household Transactions.csv"


# ---------- HOME (redirect to login) ----------
@app.route("/")
def home():
    return redirect("/login")


# ---------- LOGIN PAGE ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "manasa" and password == "swathi@1023":
            return redirect("/dashboard")
        else:
            return "Invalid username or password"

    return render_template("login.html")


# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    df = pd.read_csv(FILE)
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

    income = df[df["Income/Expense"] == "Income"]["Amount"].sum()
    expense = df[df["Income/Expense"] == "Expense"]["Amount"].sum()
    total = income - expense

    return render_template(
        "index.html",
        income=income,
        expense=expense,
        total=total,
        tables=df.to_html(index=False)
    )


# ---------- ADD TRANSACTION ----------
@app.route("/add", methods=["POST"])
def add():
    category = request.form["category"]
    amount = request.form["amount"]
    entry_type = request.form["type"]

    df = pd.read_csv(FILE)

    df.loc[len(df)] = [
        "Today",
        category,
        amount,
        "Income" if entry_type == "income" else "Expense"
    ]

    df.to_csv(FILE, index=False)
    return redirect("/dashboard")


# ---------- DELETE ROW ----------
@app.route("/delete", methods=["POST"])
def delete():
    row = int(request.form["row"])
    df = pd.read_csv(FILE)
    df.drop(index=row, inplace=True)
    df.to_csv(FILE, index=False)
    return redirect("/dashboard")


if __name__ == "__main__":
    app.run(debug=True)
