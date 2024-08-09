from flask import Flask, render_template, request, jsonify
from datetime import datetime, date
from doomsday_algorithm import is_leap_year, get_day_of_week, get_day_name

app = Flask(__name__)

# Function to get the ordinal suffix
def ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f"{n}{suffix}"
@app.route('/')
def index():
    current_year = datetime.now().year
    return render_template('index.html', current_year=current_year)

@app.route('/compute', methods=['POST'])
def compute():
    data = request.get_json()
    month = data['month']
    day = data['day']
    year = data['year']

    # Error handling for invalid dates
    if (month == 2 and day > 29) or ((month in [4, 6, 9, 11]) and day > 30) or (month == 2 and day == 29 and not is_leap_year(year)):
        return jsonify({"error": "Invalid date selected. Please choose a valid date."}), 400

    # Doomsday algorithm calculations
    day_of_week = get_day_of_week(month, day, year)
    day_name = get_day_name(day_of_week)
    today = date.today()
    selected_date = date(year, month, day)
    day_of_year = selected_date.timetuple().tm_yday
    days_in_year = 366 if is_leap_year(year) else 365
    remaining_days = days_in_year - day_of_year
    
    ordinal_day = ordinal(day)
    month_name = selected_date.strftime("%B")

    if selected_date < today:
        result_text = f"{ordinal_day} of {month_name} {year} was on a {day_name}. It was day {day_of_year} of the year and there were {remaining_days} days remaining in {year}."
    elif selected_date == today:
        result_text = f"You're right! Today is {day_name}, the {ordinal_day} of {month_name} {year}. We are in day {day_of_year} of this year and {remaining_days} days are remaining in {year}."
    else:
        result_text = f"{ordinal_day} of {month_name} {year} will be on a {day_name}. It will be day {day_of_year} of the year and there will be {remaining_days} days remaining in {year}."

    more_about_text = f"{selected_date.strftime('%B')} {day}"
    more_about_link = f"https://en.wikipedia.org/wiki/{selected_date.strftime('%B')}_{day}"

    century_anchor = (year // 100) * 100
    century_anchor_day = get_day_name((century_anchor // 100) % 4)

    # Doomsday for the month calculation
    doomsday_months = [3, 28, 14, 4, 9, 6, 11, 8, 5, 10, 7, 12]
    if is_leap_year(year):
        doomsday_months[0] = 4
        doomsday_months[1] = 29
    doomsday_month = doomsday_months[month - 1]

    result = {
        "result_text": result_text,
        "more_about_text": more_about_text,
        "more_about_link": more_about_link,
        "century_anchor": century_anchor,
        "century_anchor_day": century_anchor_day,
        "result_month": selected_date.strftime('%B'),
        "doomsday_month": f"{doomsday_month}",
        "calculated_day": day_name
    }

    return jsonify(result)

@app.route('/lapse')
def lapse():
    return render_template('lapse.html')

if __name__ == '__main__':
    app.run(debug=True)
