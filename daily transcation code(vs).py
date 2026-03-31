from flask import Flask, render_template, request, redirect
import pandas as pd

app = Flask(__name__)

FILE = "data/Daily Household Transactions.csv"

@app.route("/", methods=["GET", "POST"])
def home():
    df = pd.read_csv(FILE)

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

@app.route("/add", methods=["POST"])
def add():
    category = request.form["category"]
    amount = request.form["amount"]
    entry_type = request.form["type"]

    df = pd.read_csv(FILE)

    new_row = {
        "Date": "Today",
        "Category": category,
        "Amount": amount,
        "Income/Expense": "Income" if entry_type == "income" else "Expense"
    }

    df.loc[len(df)] = new_row
    df.to_csv(FILE, index=False)

    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    row = int(request.form["row"])
    df = pd.read_csv(FILE)
    df.drop(index=row, inplace=True)
    df.to_csv(FILE, index=False)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
