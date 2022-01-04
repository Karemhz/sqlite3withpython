from util.ClearScreen import screen_clear
from Student.Student import ShowInfo
import sqlite3
conn = sqlite3.connect('school.db')


def ChangeGrade(studentID, courseID):
    while True:
        screen_clear()
        cursor = conn.execute("SELECT mid, final FROM Grade WHERE studentID = :sID AND courseID = :cID", {"sID": studentID, "cID": courseID})
        data = cursor.fetchone()
        if data:
            print("1) Midterm: ", data[0])
            print("2) Final: ", data[1])
            print("3) Back")
            x = int(input("Choose Number: "))
            if x == 1:
                ans = int(input("Enter Grade: "))
                cursor = conn.execute("UPDATE Grade set mid = :m WHERE studentID = :sID AND courseID = :cID",{"m": ans, "sID": studentID, "cID": courseID})
                conn.commit()
                print("Updated")
                a = input("Press any key to go back")
            elif x == 2:
                ans = int(input("Enter Grade: "))
                cursor = conn.execute("UPDATE Grade set final = :m WHERE studentID = :sID AND courseID = :cID",{"m": ans, "sID": studentID, "cID": courseID})
                conn.commit()
                print("Updated")
                a = input("Press any key to go back")
            elif x == 3:
                return
        else:
            print("Data Not found!")
            x = input("Press any key to go back")
            return

def ViewCourse(id, teacherID):
    while True:
        screen_clear()
        cursor = conn.execute("SELECT title FROM Course WHERE teacherID = :tID AND id = :cID", {"tID": teacherID, "cID": id})
        d = cursor.fetchone()
        if d:
            cursor = conn.execute("SELECT Student.id, Student.name, Student.email, mid, final FROM Grade INNER JOIN Student ON studentID = Student.id WHERE courseID = :courseID",{"courseID": id})
            data = cursor.fetchall()
            print("## There are", len(data), "Students ##\n")
            if len(data) > 0:
                for index, row in enumerate(data):
                    print(index+1,")", row[1], "-", row[2],"-- ID:", row[0])
                    print(" MidTerm",row[3], "-"," Final", row[4], "\n")
                x = input("Do you want to set student grade? y/n: ")
                if x == "y":
                    ans = int(input("Please Enter Student ID: "))
                    ChangeGrade(ans, id)
                else: 
                    return
            else:
                print("No Students")
                x = input("Press any key to go back")
                return
        else:
            print("You Don't Have access on this course!")
            x = input("Press any key to go back")
            return

def ShowMyCourses(id):
    screen_clear()
    cursor = conn.execute("SELECT id, title FROM Course WHERE teacherID = :id", {"id": id})
    data = cursor.fetchall()
    if len(data) > 0:
        for index, row in enumerate(data):
            print(index+1,")",row[1], "--ID:", row[0])
        x = input("Do you want to access any Course? y/n: ")
        if x == "y":
            ans = int(input("Enter Course ID: "))
            ViewCourse(ans, id)
        else:
            return
    else:
        print("No Courses Found!")
        x = input("Press any key to go back") 
        return       


def CreateCourse(teacherID):
    while True:
        screen_clear()
        title = input("Enter Course Title: ")
        cursor = conn.execute("SELECT title, id FROM Course WHERE title = :t",{"t": title})
        data = cursor.fetchone()
        if data:
            print("Course Already Exist!")
            s = input("Try different Name? y/n ")
            if s != "y":
                return
        else:
            cursor = conn.execute("INSERT INTO Course(title, teacherID) VALUES(?,?)",(title, teacherID))
            conn.commit()
            print("Course Added")
            p = input("Press any key to go back")
            return

def TeacherHome(id, name, email):
    while True:
        screen_clear()
        print("------------------------")
        print("Welcome Back",name,"!")
        print("------------------------")
        print("1) My Courses\n2) Create Course\n3) Display Info\n4) Logout")
        try:
            x = int(input("Please Enter a number: "))
            if x == 1:
                ShowMyCourses(id)
            elif x ==2:
                CreateCourse(id)
            elif x == 3:
                ShowInfo(id, name, email)
            elif x == 4:
                return
        except ValueError: 
            print("Oops! That was no valid number. Try again...")


def TeacherLogin():
    while True:
        email = input("Please Enter your Email: ")
        password = input("Please Enter your Password: ")
        cursor = conn.execute("SELECT email, password, name, id FROM Teacher WHERE email = :email", {"email": email})
        d = cursor.fetchone()
        if d:
            if d[1] == password:
                return TeacherHome(d[3], d[2], d[0])
            else:
                print("Wrong Password, Try again? y/n")
                ans = input()
                if ans == "n":
                    return 
        else: 
            print("Not Found, Try again? y/n")
            anss = input()
            if anss == "n":
                return 

def CreateTeacher():
    while True:
        screen_clear()
        name = input("Please Enter your Name: ")
        email = input("Please Enter your Email: ")
        password = input("Please Enter your password: ")
        s = conn.execute("SELECT email FROM Teacher WHERE email = :email", {"email": email})
        d = s.fetchone()
        if d:
            x = input("User Already Exist!.. Try different email address")
        else:
            cursor = conn.execute("INSERT INTO Teacher(name, email, password) VALUES(?,?,?)", (name, email,password))
            conn.commit()
            print("Teacher Created :)")
            x = input("Press any key to Continue login..")
            return 



def Teacher():
    screen_clear()
    print("Welcome Teacher...")
    print("1) Login\n2) Signup\n3) Go Back")
    while True:
            x = int(input("Please Enter a number: "))
            if x == 1:
                return TeacherLogin()
            elif x == 2:
                return CreateTeacher()
            elif x == 3:
                return
