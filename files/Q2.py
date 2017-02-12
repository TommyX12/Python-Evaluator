i = float(raw_input("Enter marks to average, -1 to stop: "));
a = 0.0;
d = 0.0;
while i != -1:
    a += i;
    d += 1.0;
    i = float(raw_input());
r = a/d;
if int(r) == r: r = int(r);
print "Average is: " + str(r);