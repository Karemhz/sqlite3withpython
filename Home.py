from Student.Student import Student
from Teacher.Teacher import Teacher
from util.ClearScreen import screen_clear
# Home Function
def Home():
     while True:
        screen_clear()
        print("---------------------------------------------")
        print("Welcome to our Tiny School Management System")
        print("---------------------------------------------")
        print("1) Teacher\n2) Student\n3) Exit\n")
        try:
            x = int(input("Please Enter a number: "))
            if x == 1:
                print("You are a Teacher")
                Teacher()
            elif x == 2:
                print("You are student")
                Student()
            elif x == 3:
                return
        except ValueError: 
            print("Oops! That was no valid number. Try again...")
