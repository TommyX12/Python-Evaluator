import subprocess;
import sys;
import re;
import os;
import glob;
import math;

def removeInputPrompts(filePath, outPath):
    print "Removing input prompts...",
    script = open(filePath, "r");
    text = script.read();
    startRE = re.compile("""(\Wraw_|\W)input\s*\(""");
    startIterator = startRE.finditer(text);
    startIndex = [];
    for match in startIterator:
        startIndex.append(match.end());
    endRE = re.compile("""(\Wraw_|\W)input\s*\(\s*(["'].*["'])?\s*\)""");
    endIterator = endRE.finditer(text);
    endIndex = [];
    for match in endIterator:
        endIndex.append(match.end());
    removedLength = 0;
    for index in range(len(startIndex)):
        text = text[:startIndex[index]-removedLength] + text[endIndex[index]-1-removedLength:];
        removedLength += endIndex[index] - startIndex[index] - 1;
    out = open(outPath, "w");
    out.write(text);
    out.close();
    print "Done.";

def checkOutput(filePath, testCase):
    script = subprocess.Popen([sys.executable, filePath], universal_newlines=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE);
    out_value = script.communicate(testCase)[0];
    out_value = out_value.strip();
    return out_value;

def evaluateSingleCase(filePath, testCase, answer):
    removeInputPrompts(filePath, os.path.dirname(os.path.realpath(sys.argv[0]))+"/_temp");
    print "-----|" + filePath + "|-----";
    output = checkOutput("_temp", testCase);
    os.remove(os.path.dirname(os.path.realpath(sys.argv[0]))+"/_temp");
    print output;
    answer = answer.strip();
    print "--|Answer|--";
    print answer;
    if output == answer:
        print "-|Matched answer|-";
        print "";
        return True;
    else:
        print "-|Mismatched answer|-";
        print "";
        return False;

def evaluateMultiCase(filePath, casePath, answerPath):
    caseFile = open(casePath, "r");
    cases = caseFile.read();
    if "---|View Source|---" in cases:
        source = open(filePath);
        sourceText = source.read().strip();
        print "---|Source|---";
        print sourceText;
        print "";
        return -1;
    cases = cases.split("---|Case|---\n");
    answerFile = open(answerPath, "r");
    answers = answerFile.read();
    answers = answers.split("---|Case|---\n");
    removeInputPrompts(filePath, os.path.dirname(os.path.realpath(sys.argv[0]))+"/_temp");
    count = 0;
    matched = 0;
    for case in cases:
        print "---|Case " + str(count+1) + "|---";
        output = checkOutput(os.path.dirname(os.path.realpath(sys.argv[0]))+"/_temp", case);
        print output;
        answers[count] = answers[count].strip();
        print "--|Answer|--";
        print answers[count];
        if output == answers[count]:
            matched += 1;
            print "-|Matched answer|-";
        else:
            print "-|Mismatched answer|-";
        count += 1;
        print "-";
    print "--|Preliminary score: "+ str(matched) + "/" + str(count) + " " + str(math.ceil(matched/count*100)) + "%|--";
    os.remove(os.path.dirname(os.path.realpath(sys.argv[0]))+"/_temp");
    print "";
    return matched/count;

def evaluateFolder(folderPath, caseFolderPath, answerFolderPath):
    fileList = glob.glob(folderPath+"/*.py");
    caseList = glob.glob(caseFolderPath+"/*.txt");
    answerList = glob.glob(answerFolderPath+"/*.txt");
    total = 0;
    count = 0;
    for index in range(len(fileList)):
        print "-----|" + fileList[index] + "|-----";
        score = evaluateMultiCase(fileList[index], caseList[index], answerList[index]);
        if score != -1:
            total += score;
            count += 1;
    print "-----|Approximated final score: "+ str(math.ceil(total/count*100)) + "%|-----";


if ".py" in sys.argv[1]:
    evaluateMultiCase(sys.argv[1], os.path.dirname(os.path.realpath(sys.argv[0]))+"/case.txt", os.path.dirname(os.path.realpath(sys.argv[0]))+"/answer.txt");
else:
    evaluateFolder(sys.argv[1], os.path.dirname(os.path.realpath(sys.argv[0]))+"/cases", os.path.dirname(os.path.realpath(sys.argv[0]))+"/answers");

raw_input("Press enter to exit");


# --------------
#
# Default behaviour:
#
# - drag and drop a python script onto the script to evaluate it
# -- using test cases txt in "case.txt" and answers in "answer.txt"n(same directory as the script)
# -- test cases and answers separate each case using 1 line of "---|Case|---" (no separation line before 1st case)
#
# - drag and drop folder onto the script to evaluate all python scripts inside the folder
# -- using test cases txt in "cases" folder and answers in "answers" folder (same directory as the script)
# -- test cases and answers separate each case using 1 line of "---|Case|---" (no separation line before 1st case)
# -- files will correspond as long as they have the same index sorted by name
# -- put the line "---|View Source|---" inside a test case txt to view the source of the script file for that question
#
# -------
#
# Methods:
#
# evaluateSingleCase(filePath:str, testCase:str, answer:str)
# - prints output value of python script file without input prompts at filePath using testCase as stdin
# - also checks if the output matches the answer string.
# -- example: evaluateSingleCase("files/Q1.py", "1+1", "2")
#
# evaluateMultiCase(filePath:str, casePath:str, answerPath:str)
# - prints output value of python script file without input prompts at filePath, checking every case in text file at casePath.
# -- cases are separated by 1 line of "---|Case|---"
# - also provides preliminary score by comparing the output with the answers (also separated by 1 line of "---|Case|---")
# -- example: evaluateMultiCase("files/Q1.py", "cases/Q1.txt", "answers/Q1.txt")
#
# evaluateFolder(folderPath:str, caseFolderPath:str, answerFolderPath:str)
# - evaluates all .py files under folderPath, using corresponding .txt under caseFolderPath.
# -- files will correspond as long as they have the same index sorted by name
# - provide approximated final score
# -- example: evaluateFolder("files", "cases", "answers")
#
# --------------
