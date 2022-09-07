import sys
import re
import pickle
class Person():
    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone
    def display(self):
        print("Employee id: " + self.id)
        print('\t' + self.first + " " + self.mi + " " + self.last)
        print('\t' + self.phone)

try:
    text = sys.argv
except Exception as e:
    print(e)

f = open(text[1], 'r')
text = f.readlines()[1:] #Skip first line

dict = {}
for line in text: #read line by line
    list = line.split(",")
    if(len(list[2])== 0): #list[2]=middle name, change to X if empty
        list[2] = "X"
    idMatch = re.fullmatch("[a-zA-Z]{2}\d{4}", list[3])
    if(not idMatch): #Validate id
        print("ID invalid: "+list[3])
        print("Please enter a valid id: ")
        list[3] = input()

    phone = list[4].replace("\n","") #validate phone number
    numMatch = re.fullmatch("[0-9]{3}-?[0-9]{3}-?[0-9]{4}|[0-9]{3}\.?[0-9]{3}\.?[0-9]{4}|[0-9]{3}\s[0-9]{3}\s[0-9]{4}", phone)
    if (not numMatch):
        print("Phone " + phone + " is invalid")
        print("Enter phone number in form 123-456-7890")
        phone = input()
    phone = re.sub("\.","-", phone) #Formats phone number
    phone = re.sub(" ","-", phone)
    #create person object with modified input
    p = Person(list[0].capitalize(), list[1].capitalize(), list[2].capitalize(), list[3], phone)
    dict[list[3]] = p #list[3] is id, makes id key and person object the value
    #p.display()

pickle.dump(dict, open('dict.p', 'wb')) #Creates pickle file
dict_in = pickle.load(open('dict.p', 'rb'))
print("Employee List")
for key in dict_in:
    dict_in[key].display()

