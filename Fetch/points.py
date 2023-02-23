import sys
import csv

n_args = len(sys.argv)

if (n_args != 3):                               # ensure only 3 args are passed: prog name, # points, filename
    print("Usage: python3 points.py <# points to spend> transactions.csv")
    exit()

points = int(sys.argv[1])                       # points to use, indicated by user
file = open(sys.argv[2])                        # csv file to open

csv_reader = csv.DictReader(file, delimiter=',') # read lines of csv into individual dictionaries

lines = []                                      # list to store dictionaries
payers = {}                                     # dictionary of payers to store point totals at the end

for i in csv_reader:                            # read dictionaries into a list one at a time
    i['points'] = int(i['points'])              # convert points to int to enable arithmetic
    i['timestamp'] = i['timestamp'].split('T')  # separate date and time into a list
    if (payers.get(i['payer']) == None):        # add unique payers to dict. and set balance to 0
        payers[i['payer']] = 0
    lines.append(i)

def date_key(ln):                               # line from csv, convert time/date to comparable value for sorting
    timeDate = ln['timestamp']
    total = 0
    dt = timeDate[0].split('-') + timeDate[1].split(':') # split data and time into individual #'s
    dt = dt[:-2]                                # omitting minutes and seconds since dataset only contains hours

    for i in range(len(dt)):                    # convert date and time items to integers for arithmetic
        dt[i] = int(dt[i])
    
    total += 365*dt[0] + 31*dt[1] + dt[2] + dt[3]/24 # single numeric representation of date/time to allow sorting

    return total

lines.sort(key=date_key)                        # sort each csv entry by their timestamp in ascending order

for i in lines:                                 # main loop to use points
    points -= i['points']
    if (points < 0):                            # negative points indicates current payer had more than enough points to pay
        i['points'] = points*-1                 # return surplus points to payer, then set points remaining to 0
        points = 0
        break
    else:                                       # case where all points of a payer chunk were spent, but did not cover total points
        i['points'] = 0
for i in lines:                                 # assign remaining point totals to all payers
    payers[i['payer']] += i['points']

print(payers)                                   # output point totals