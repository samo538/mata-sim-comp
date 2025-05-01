import csv
import matplotlib.pyplot as plt
import re
import tabulate
import sys
import statistics

def categ_x(row, what):
    # logic
    if (row[0][:40] == "automata/nfa-bench/benchmarks/presburger"):
        logic_x.append(what)

    # regex
    elif (row[0][:42] == "automata/nfa-bench/benchmarks/email_filter"):
        regex_x.append(what)

    # operations
    elif (row[0][:40] == "automata/nfa-bench/benchmarks/z3-noodler"):
        operations_x.append(what)
    elif (row[0][:39] == "automata/nfa-bench/benchmarks/bool_comb"):
        operations_x.append(what)
    elif (row[0][:48] == "automata/nfa-bench/benchmarks/automata_inclusion"):
        operations_x.append(what)


def categ_y(row, what):
    # logic
    if (row[0][:40] == "automata/nfa-bench/benchmarks/presburger"):
        logic_y.append(what)

    # regex
    elif (row[0][:42] == "automata/nfa-bench/benchmarks/email_filter"):
        regex_y.append(what)

    # operations
    elif (row[0][:40] == "automata/nfa-bench/benchmarks/z3-noodler"):
        operations_y.append(what)
    elif (row[0][:39] == "automata/nfa-bench/benchmarks/bool_comb"):
        operations_y.append(what)
    elif (row[0][:48] == "automata/nfa-bench/benchmarks/automata_inclusion"):
        operations_y.append(what)

def fix_timeout(to_fix):
    for i in range(0, len(to_fix)):
        if (to_fix[i] == 'TO'):
            to_fix[i] = limit

# global variables
x = []
y = []
count_x = 0
count_y = 0

iny_win = 0
rt_win = 0

iny_timeout = 0
rt_timeout = 0

iny_priemer = 0
rt_priemer = 0

# set the division into categories false by default
categories = False
logic_x = []
logic_y = []
regex_x = []
regex_y = []
operations_x = []
operations_y = []

if (len(sys.argv) != 4 and len(sys.argv) != 5):
    print("python3 graph.py [horisontal_axis] [vertical_axis] [metric] {categories}")
    sys.exit()

if (len(sys.argv) == 5):
    if (sys.argv[4] == "categories"):
        categories = True
    else:
        print("python3 graph.py [horisontal_axis] [vertical_axis] [metric] {categories}")
        sys.exit()


# open files
csvfile = open(sys.argv[1], 'r')
csvfile2 = open(sys.argv[2], 'r')
plots = csv.reader(csvfile, delimiter = ';')
plots2 = csv.reader(csvfile2, delimiter = ';')

selector = 0
limit = ''

# selection
if (sys.argv[3] == "time"):
    color = 'g'
    selector = 3
    limit = '60'
elif (sys.argv[3] == "states"):
    color = 'b'
    selector = 4
    limit = '1000'
elif (sys.argv[3] == "transitions"):
    color = 'orange'
    selector = 5
    limit = '5000'
else:
    print("python3 graph.py [horisontal_axis] [vertical_axis] [metric] {categories}")
    sys.exit()


# parse x axis data
for row in plots:
    if (row[0] == 'name'):
        continue

    count_x = count_x + 1

    if (row[selector] == 'TO' or row[selector] == 'ERR'):
        iny_timeout = iny_timeout + 1;
        x.append('TO');
        if (categories):
            categ_x(row, 'TO')
        continue

    x.append(float(row[selector]))
    if (categories):
        categ_x(row, float(row[selector]))

# parse y axis data
for row in plots2:
    if (row[0] == 'name'):
        continue

    count_y = count_y + 1

    if (row[selector] == 'TO' or row[selector] == 'ERR'):
        rt_timeout = rt_timeout + 1
        y.append('TO')
        if (categories):
            categ_y(row, 'TO')
        continue

    y.append(float(row[selector]))
    if (categories):
        categ_y(row, float(row[selector]))
#    match = re.match(r'([a-z]*)\/b-([a-z-]*)\/(aut[0-9]*)', row[0])
#    x.append('{0},{1}'.format(match[2], match[3]))
#    y.append(float(row[3]))

# set limit for the graph
if (sys.argv[3] == "time"):
    limit = 60
else:
    # To be able to do max(x) we need to delete the strings inside x
    x_helper = []
    y_helper = []
    for integer in x:
        if (isinstance(integer, float)):
            x_helper.append(integer)

    for integer in y:
        if (isinstance(integer, float)):
            y_helper.append(integer)

    if (max(x_helper) > max(y_helper)):
        limit = int(max(x_helper) * 1.1)
    else:
        limit = int(max(y_helper) * 1.1)

# replace all timeouts with the limit
fix_timeout(x)
fix_timeout(logic_x)
fix_timeout(regex_x)
fix_timeout(operations_x)

fix_timeout(y)
fix_timeout(logic_y)
fix_timeout(regex_y)
fix_timeout(operations_y)

# sanity check
if (count_x != count_y):
    print("exiting")
    sys.exit()

# calculate wins and mean
for i in range(0, count_x):
    if (x[i] < y[i]):
        iny_win = iny_win + 1
    if (x[i] > y[i]):
        rt_win = rt_win + 1
    iny_priemer = iny_priemer + x[i]
    rt_priemer = rt_priemer + y[i]

# finish mean
iny_priemer = iny_priemer / (i + 1)
rt_priemer = rt_priemer / (i + 1)

# max min
max_x = max(x)
min_x = min(x)

max_y = max(y)
min_y = min(y)

# median
iny_median = statistics.median(x) 
rt_median = statistics.median(y) 

#std dev
iny_stddev = statistics.stdev(x)
rt_stddev = statistics.stdev(y)

# statistics table
data = [
    {"Algorithm": sys.argv[1], "Max": max_x, "Min": min_x, "Median": iny_median, "Stddev": iny_stddev, "Mean": iny_priemer, "Wins": iny_win , "Timeouts" : iny_timeout},
    {"Algorithm": sys.argv[2], "Max": max_y, "Min": min_y, "Median": rt_median, "Stddev": rt_stddev, "Mean": rt_priemer, "Wins": rt_win , "Timeouts" : rt_timeout}
]

table = tabulate.tabulate(data,headers = "keys", tablefmt="pipe",colalign=("left", "center", "right"),missingval = "N/A")

# Printing the table
print(table)

# the plot
if (not(categories)):
    plt.scatter(x, y, color = color,s = 25)
else:
    plt.scatter(logic_x, logic_y, color = 'b',s = 25)
    plt.scatter(regex_x, regex_y, color = 'g',s = 25)
#    plt.scatter(operations_x, operations_y, color = 'r',s = 25)

plt.xlabel(sys.argv[1], fontsize = 18) 
plt.ylabel(sys.argv[2], fontsize = 18) 
plt.xscale("log") 
plt.yscale("log") 
plt.grid(True)
plt.axis('square')

limit = float(limit)

line = plt.axline((0,0),(limit,limit))
line.set_dashes([5,2,1,2])
line.set_color('gray')

line = plt.axline((limit,0),(limit,limit))
line.set_dashes([5,2,1,2])
line.set_color('gray')

line = plt.axline((0,limit),(limit,limit))
line.set_dashes([5,2,1,2])
line.set_color('gray')

plt.show()
