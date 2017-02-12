i = int(raw_input("How many runners?"));
w = -1.0;
for h in range(i):
    n = float(raw_input("Enter time: "));
    if n < w or w == -1.0: w = n;
print "Winning time: " + str(w);