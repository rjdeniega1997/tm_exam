def addNumbers(x,y):
    return x+y

print(addNumbers(5,5))


class Person:
    birthday = ""
    age = 0


def createPerson(birthday, age):
    person = Person()
    person.birthday = birthday
    person.age = age
    return person

personlist = []
for x in range (1,5):
    x = createPerson("October 23", 15)
    personlist.append(x)

print(personlist)

