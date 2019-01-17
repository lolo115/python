from __future__ import print_function
class Dba:
    #  The __init__() function is called automatically every time the class is being used to create a new object.
    # But it's not the "constructor" which is __new__ but as __new__ is rarely used (inheritance for example),
    # we frequently use __init__ (initiator of something that is previously created by __new__)
    # https://docs.python.org/3/reference/datamodel.html#basic-customization

    def __init__(self, name, age, skills):
        self.name=name
        self.age=age
        # Private class parameters (same from methods)
        self.__skills=skills

    def setAge(self,age):
        self.age=age;

    def getAge(self):
        return self.age

    def getSkills(self):
        return self.__skills

    def setSkills(self,skills):
        self.__skills=skills


# Notes:
# The self parameter is a reference to the class instance itself, and is used to access variables that belongs to the class.


# main
if __name__ == '__main__':
    laurent = Dba(name="Laurent",age=40,skills='Good')
    print("laurent's type = ", type(laurent))

    print ("Laurent's age: ",laurent.getAge())
    laurent.setAge(41)
    print ("After his birthday: " , laurent.getAge ())
    laurent.age=42
    print ("But wait ... : ", laurent.age)

    #print("Laurent's skills:", laurent.__skills)
    print("Laurent's skills:", laurent.getSkills())

