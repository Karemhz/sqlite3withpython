import sqlite3
from util.ClearScreen import screen_clear
conn = sqlite3.connect('school.db')

def AddCourse(studentID, courseID):
    cursor = conn.execute("""
    SELECT studentID, courseID 
    FROM Grade 
    WHERE courseID = :courseID AND studentID = :studentID""", {"courseID": courseID, "studentID": studentID})
    d = cursor.fetchone()
    if d:
        print("Course Already Exist!")
        x = input("Press any key to go back")
        return
    else:
        cursor = conn.execute("INSERT INTO Grade(courseID, studentID) VALUES(?,?)",(courseID, studentID))
        conn.commit()
        print("Course has been added :)")
        x = input("Press any key to go back")
        return


def ShowMyCourses(id):
    cursor = conn.execute("""
      SELECT Course.title, Teacher.name FROM Course JOIN
      Teacher ON Course.teacherID = Teacher.id WHERE Course.id IN (SELECT courseID FROM Grade WHERE studentID = :id)
    """, {"id": id})
    screen_clear()
    data = cursor.fetchall()
    if(len(data) > 0):
        print("Found",len(data), "Courses!")
        for index, row in enumerate(data):
            print(index+1,") ",row[0], "With Teacher:", row[1])
    else:
        print("No Courses Found!")
    x = input("Press any key to go back")
    return



def ShowAllCourses(studentID):
    cursor = conn.execute("SELECT Course.title, Course.id, Teacher.name FROM Course JOIN Teacher ON Course.teacherID = Teacher.id")
    screen_clear()
    data = cursor.fetchall()
    if(len(data) > 0):
        print("Found",len(data), "Courses!")
        for index, row in enumerate(data):
            print(index+1,")",row[0], "- Teacher:", row[2], "- ID:", row[1])
    else:
        print("No Courses Found!")
    if len(data) > 0:
        x = input("Do you want to add any to your courses? y/n: ")
        if x == "y":
            try:
                courseID = int(input("Please Enter Course ID: "))
                AddCourse(studentID, courseID)
                return
            except ValueError: 
                print("Oops! That was no valid number. Try again...")
        else:
            return
    else:
        x = input("Press Any key to go back")
   



def ShowInfo(id, name, email):
    screen_clear()
    print("Name:", name)
    print("Email", email)
    x = input()
    return

def ShowGrade(id):
    cursor = conn.execute("SELECT Course.title, mid, final FROM Grade INNER JOIN Course ON courseID = Course.id WHERE studentID = :id",{"id": id})
    data = cursor.fetchall()
    screen_clear()
    if len(data) > 0:
        for index, row in enumerate(data):
            print(index+1,") ",row[0], " Midterm:", row[1], " Final:", row[2])
        
        x = input("Press Any key to go back")

    else:
        print("No Courses Found!")
        x = input("Press Any key to go back")


def StudentHome(id, name, email):
    while True:
        screen_clear()
        print("------------------------")
        print("Welcome Back",name,"!")
        print("------------------------")
        print("1) Show my Courses\n2) Show Grade\n3) All Courses\n4) Display Info\n5) Logout")
        try:
            x = int(input("Please Enter a number: "))
            if x == 1:
                ShowMyCourses(id)
            elif x ==2:
                ShowGrade(id)
            elif x == 3:
                ShowAllCourses(id)
            elif x == 4:
                ShowInfo(id, name, email)
            elif x == 5:
                return
        except ValueError: 
            print("Oops! That was no valid number. Try again...")





def StudentLogin():
    while True:
        email = input("Please Enter your Email: ")
        password = input("Please Enter your Password: ")
        cursor = conn.execute("SELECT email, password, name, id FROM Student WHERE email = :email", {"email": email})
        d = cursor.fetchone()
        if d:
            if d[1] == password:
                return StudentHome(d[3], d[2], d[0])
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
              

def CreateStudent():
    while True:
        screen_clear()
        name = input("Please Enter your Name: ")
        email = input("Please Enter your Email: ")
        password = input("Please Enter your password: ")
        s = conn.execute("SELECT email FROM Student WHERE email = :email", {"email": email})
        d = s.fetchone()
        if d:
            x = input("User Already Exist!.. Try different email address")
        else:
            cursor = conn.execute("INSERT INTO Student(name, email, password) VALUES(?,?,?)", (name, email,password))
            conn.commit()
            print("Student Created :)")
            x = input("Press any key to Continue login..")
            return 

def Student():
    screen_clear()
    print("Welcome Student...")
    print("1) Login\n2) Signup\n3) Go Back\n")
    while True:
            x = int(input("Please Enter a number: "))
            if x == 1:
                return StudentLogin()
            elif x == 2:
                return CreateStudent()
            elif x == 3:
                return
        