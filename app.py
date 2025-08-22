from flask import Flask, render_template, request, redirect, send_file
import pandas as pd
import os

app = Flask(__name__)
csv_file = 'classes.csv'

# Create CSV if not exists
if not os.path.exists(csv_file):
    df = pd.DataFrame(columns=['Name', 'Date', 'Hours', 'Price_per_Hour', 'Total'])
    df.to_csv(csv_file, index=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        hours = int(request.form['hours'])
        price = int(request.form['price'])
        total = hours * price

        df = pd.read_csv(csv_file)
        df = pd.concat([df, pd.DataFrame({
            'Name': [name],
            'Date': [date],
            'Hours': [hours],
            'Price_per_Hour': [price],
            'Total': [total]
        })], ignore_index=True)
        df.to_csv(csv_file, index=False)

        return redirect('/')

    df = pd.read_csv(csv_file)
    data = df.to_dict(orient='records')

    names = ["Kuhu", "Mairav", "Gowri", "Arnit", "Harini","Harshini","Aarav","Abhay","Laksh","Anushka"]
    hours = [1, 2, 3, 4, 5]
    prices = [100, 200, 300, 400, 500]

    return render_template('tuition.html',
                           data=data,
                           names=names,
                           hours=hours,
                           prices=prices)

# ✅ Route to download CSV
@app.route('/download')
def download_csv():
    return send_file(csv_file, as_attachment=True)

# Render will use Gunicorn, so no need for app.run()
