# doomsday_algorithm.py

def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

def get_doomsday(year):
    anchor_days = [2, 0, 5, 3]  # Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday
    century = year // 100
    anchor_day = anchor_days[century % 4]

    y = year % 100
    doomsday = (anchor_day + y + y // 4) % 7
    return doomsday

def get_day_of_week(month, day, year):
    doomsday = get_doomsday(year)
    doomsday_months = [3, 28, 14, 4, 9, 6, 11, 8, 5, 10, 7, 12]
    if is_leap_year(year):
        doomsday_months[0] = 4
        doomsday_months[1] = 29

    day_of_week = (day - doomsday_months[month - 1] + doomsday) % 7
    if day_of_week < 0:
        day_of_week += 7
    return day_of_week

def get_day_name(day_of_week):
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    return days[day_of_week]

if __name__ == "__main__":
    month = int(input("Enter month: "))
    day = int(input("Enter day: "))
    year = int(input("Enter year: "))
    day_of_week = get_day_of_week(month, day, year)
    print(f"The day of the week for {month}/{day}/{year} is {get_day_name(day_of_week)}.")
