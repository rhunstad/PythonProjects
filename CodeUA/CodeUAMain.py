

# Slide 16: Variables
a = 75      # integer
b = 76.46       # float
c = "This is a String"      # string
d = True

e = "let's try some escape-characters. The first one it tab: \tSee?" \
    "Also notice how I made a new line in my code, but that DOESNT make a new line in my output? " \
    "To do a new line in your output, you do \nSee?"
print(e)


# Slide 17: Variable operators
f = 5
print("\nf should equal 5: ", f)
f += 1
print("\nf should equal 6: ", f)
f = 20/2
print("\nf should equal 10: ", f)
f = 20 * 2
print("\nf should equal 40: ", f)
f = 5**2
print("\nf should equal 25: ", f)
f = 15 % 12
print("\nf should equal 3: ", f)


f = 5
g = str(f)
print(g, type(g), f, type(f))

f = "5"
g = int(f)
print(g, type(g), f, type(f))


f = 10
if f < 20:
    print(f)


# Slide 20:
a = 5
while a < 8:
    print(a)
    a += 1


# Slide 21:
for i in range(10):
    print(i)

for i in range(10, 15, 1):
    print(i)


# Slide 24:
a = True
if a is True:
    print("a is True")

if a:
    print("a is True")


# Slide 25:
a = 10
if a == 0:
    print("A is 0")
elif a < 10:
    print("A is less than 10 but is not 0")
else:
    print("A is greater or equal to 10")


"""
# Slide 26:
for i in range(5):
    for j in range(4):
        print(i*j)


# Slide 27:
for i in range(5):
    for j in range(4):
        if i*j < 10:
            print(i*j)

# Slide 28:
name = input("Student name: ")
CWID = input("Student CWID: ")
major = input("Student major: ")
email = input("Student crimson email: ")
print(name, CWID, major, email)

"""
#
#
#
#
#
#
# Day 2:
# Slide 7:

fruits = ['orange', 'grapes', 'apple', 'mango']
print(fruits)

print(fruits[0])    # What does this print?
print(len(fruits))  # What does this print?

fruits.append('kiwi')
print(fruits[4])    # What does this print?

fruits.insert(1, 'peaches')
print(fruits[1])    # What does this print?

fruits = sorted(fruits)
print(fruits)    # What does this print?

fruits += fruits
print(fruits)   # What does this print?

# You can even have nested lists:
my_list = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [10, 11, 12],
]
print(my_list)
print(my_list[0])
print(my_list[0][1])


# Slide 8:
print("\n\n\n\n")
my_tuple = tuple(fruits)
print(my_tuple)
print(my_tuple[1])

# Slide 9:
users_dict = {
    "user1": "password",
    "rhunstad": "mypassword",
    "user2": "goodpassword"
}

users_dict['user3'] = 'very_good_password'

print(users_dict)
print(users_dict.get('name'), "\n\n")

for key, value in users_dict.items():
    print(key, value)


# Slide 14: Functions
def login():
    username = input("\nUsername: ")
    user_password = users_dict.get(username)
    if user_password is None:
        return

    password = input("Password: ")

    if password == user_password:
        return True
    else:
        return False


success = True
# success = login()
if success:
    print("You're logged in!\n\n")
else:
    print("Sorry, something went wrong.")


# Slide 19:
f = open("inventory.txt", 'w')
f.write("Ryland Hunstad#11800000#Junior#MIS\nJeff Lucas#22222222#Faculty#MIS")
f.close()

f = open("inventory.txt", 'r')
f = f.read()
# print(f)


# Slide 22:
f = open("inventory.txt", 'r')
f = f.read()
f = f.split("\n")

for line in f:
    line = line.split("#")
    print(line)


# Slide 26:

class Student(object):
    def __init__(self, f_name_var, l_name_var, CWID_var):
        self.f_name = f_name_var
        self.l_name = l_name_var
        self.CWID = CWID_var
        self.crimson_email = self.f_name[0].lower() + self.l_name.lower() + "@crimson.ua.edu"

    def print_student(self):
        output = self.l_name + ", " + self.f_name + ": \n" + str(self.CWID) + "\n" + self.crimson_email
        print(output)


# if __name__ == '__main__':
    # main()


# Slide 33: See the TicTacToe game