import datetime

date = input("What date would you like? Use YYYY-MM-DD :")

year = date.split("-")[0]
month = date.split("-")[1]
day = date.split("-")[2]

print(year)
print(month)
print(day)

print(date)

x = datetime.datetime(int(year), int(month), int(day))
short_month = (x.strftime("%b"))


