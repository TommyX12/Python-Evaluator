import re;

def newPassword():
    pwd = str(raw_input());
    if re.search('[A-Z].*[A-Z]', pwd) == None: return False;
    if re.search('[0-9]', pwd) == None: return False;
    if re.search('[^a-zA-Z0-9_]', pwd) != None: return False;
    return True;