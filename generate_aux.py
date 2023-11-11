
import datetime
import json

config = {}
with open('./config.json', 'r') as f:
    config = json.load(f);

assignments = []
with open("./assignment_types.json", 'r') as f:
    assignments = json.load(f);


def get_config(key):
    return config.get(key, "Bad Key")

PrimaryAuthorName = get_config("author_name")
AuthorIdentifier = get_config("author_extra_identifier")


def input_string(prompt):
    inn = input(prompt)
    print("")
    return inn

def input_string_upper(prompt):
    inn = input(prompt).upper()
    return inn

def input_options(prompt, choices, allowCustom = False):

    #Generate
    choicestr = "["
    for i in range(len(choices)):

        #Skip
        if choices[i] == "":
            continue;

        choicestr += str(i) + ": " + str(choices[i]) + ", "

    # End The String
    if allowCustom:
        choicestr += "Type #XXX to have XXX as choice. ]"
    else:
        choicestr += "]"

    # Get the Integer Input
    inn = input(prompt + "\nChoices Are: " + choicestr + "\nEnter Choice Number: ")

    #
    #
    # Grab
    try:
        return int(inn);
    except:
        if inn[0] == '#' and allowCustom:
            return inn[1:];

    # Bad
    raise Exception("Bad Input.")

def input_duedate():

    #Months
    months = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    month = input_options("Month", months)

    #Convert to Proper
    month = months[month]
    year = datetime.date.today().year

    #If it's november or something and the due date is overflowed than make sure year is right
    if datetime.date.today().month >= 11 and months.index(month) < 4:
        year += 1;

    # Pass back
    return month + " " + str(year);



def choose_assignment(details):

    #Generate a display list
    choices = [x["name"] for x in details]
    assignmentId = input_options("Assignment Type", choices, False)

    #Passback the Assignment Struct
    return details[assignmentId]



def input_authors():

    auths = []
    while True:
        inn = input_string("Input Alternate Author Name:")

        if  (inn == ""):
            break;

        auths.append(inn)

    #Exit Early
    if len(auths) == 0:
        return PrimaryAuthorName + "\n" + AuthorIdentifier

    #Generate Author String
    authStr = PrimaryAuthorName
    for auth in auths:
        authStr += "\\and " + auth

    #Return
    return authStr

def int_to_roman(num):

    # Storing roman values of digits from 0-9
    # when placed at different places
    m = ["", "M", "MM", "MMM"]
    c = ["", "C", "CC", "CCC", "CD", "D",
         "DC", "DCC", "DCCC", "CM "]
    x = ["", "X", "XX", "XXX", "XL", "L",
         "LX", "LXX", "LXXX", "XC"]
    i = ["", "I", "II", "III", "IV", "V",
         "VI", "VII", "VIII", "IX"]
 
    # Converting to roman
    thousands = m[num // 1000]
    hundreds = c[(num % 1000) // 100]
    tens = x[(num % 100) // 10]
    ones = i[num % 10]
 
    ans = (thousands + hundreds +
           tens + ones)
 
    return ans