from flask import Flask, render_template, request, jsonify
from datetime import datetime
from doomsday_algorithm import get_day_of_week, get_day_name

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lapse')
def lapse():
    return render_template('lapse.html')

@app.route('/compute', methods=['POST'])
def compute():
    data = request.get_json()
    date_str = data.get('date')
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    
    day_of_week = get_day_of_week(date_obj.month, date_obj.day, date_obj.year)
    day_name = get_day_name(day_of_week)
    
    today = datetime.today()
    is_past = date_obj < today
    is_today = date_obj.date() == today.date()
    is_future = date_obj > today

    day_of_year = (date_obj - datetime(date_obj.year, 1, 1)).days + 1
    days_in_year = 366 if (date_obj.year % 4 == 0 and date_obj.year % 100 != 0) or (date_obj.year % 400 == 0) else 365
    days_remaining = days_in_year - day_of_year

    result = {
        "day_name": day_name,
        "day_of_year": day_of_year,
        "days_remaining": days_remaining,
        "is_past": is_past,
        "is_today": is_today,
        "is_future": is_future
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
