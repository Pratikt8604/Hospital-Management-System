from tkinter import *
import sqlite3
import tkinter.messagebox
import pyttsx3
import time

# Connect to the SQLite database (or create a new one if it doesn't exist)
conn = sqlite3.connect('database3.db')
c = conn.cursor()

# Create the 'appointments' table if it doesn't exist
def create_appointments_table():
    c.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            location TEXT,
            schedule_time TEXT,
            phone TEXT
        )
    ''')
    # Commit the changes and close the connection
    conn.commit()

create_appointments_table()

class Application:
    def __init__(self, master):
        self.master = master

        self.left = Frame(master, width=800, height=720, bg='lightgreen')
        self.left.pack(side=LEFT)

        self.right = Frame(master, width=400, height=720, bg='steelblue')
        self.right.pack(side=RIGHT)

        self.heading = Label(self.left, text="YASHODA HOSPITAL MANAGEMENT", bg='lightgreen', fg='black', font=('arial 18 bold'))
        self.heading.place(x=140, y=0)

        self.name = Label(self.left, text="Patient's Name", font=('arial 18 bold'), bg='lightgreen', fg='black')
        self.name.place(x=0, y=70)

        self.age = Label(self.left, text='Age', bg='lightgreen', fg='black', font=('arial 18 bold'))
        self.age.place(x=0, y=140)

        self.gender = Label(self.left, text='Gender', bg='lightgreen', fg='black', font=('arial 18 bold'))
        self.gender.place(x=0, y=210)

        self.location = Label(self.left, text='Location', bg='lightgreen', fg='black', font=('arial 18 bold'))
        self.location.place(x=0, y=280)

        self.time = Label(self.left, text='Time', bg='lightgreen', fg='black', font=('arial 18 bold'))
        self.time.place(x=0, y=350)

        self.phone = Label(self.left, text='Phone', bg='lightgreen', fg='black', font=('arial 18 bold'))
        self.phone.place(x=0, y=420)

        self.name_ent = Entry(self.left, width=40)
        self.name_ent.place(x=250, y=70)

        self.age_ent = Entry(self.left, width=40)
        self.age_ent.place(x=250, y=140)

        self.gender_ent = Entry(self.left, width=40)
        self.gender_ent.place(x=250, y=210)

        self.location_ent = Entry(self.left, width=40)
        self.location_ent.place(x=250, y=280)

        self.time_ent = Entry(self.left, width=40)
        self.time_ent.place(x=250, y=350)

        self.phone_ent = Entry(self.left, width=40)
        self.phone_ent.place(x=250, y=420)

        self.submit = Button(self.left, text='Add Appointment', width=20, height=2, bg='steelblue', command=self.add_appointment)
        self.submit.place(x=290, y=470)

        # displaying the logs in our right frame
        self.box=Text(self.right, width=50, height=40)
        self.box.place(x=20, y=30)

    # function is called when the submit button is clicked
    def add_appointment(self):
        self.val1 = self.name_ent.get()
        self.val2 = self.age_ent.get()
        self.val3 = self.gender_ent.get()
        self.val4 = self.location_ent.get()
        self.val5 = self.time_ent.get()
        self.val6 = self.phone_ent.get()

        if self.val1 == '' or self.val2 == '' or self.val3 == '' or self.val4 == '' or self.val5 == '':
            tkinter.messagebox.showinfo("Warning!", "Please fill up all boxes.")
        else:
            # now we add to the database
            sql = "INSERT INTO 'appointments' (name, age, gender, location, schedule_time, phone) VALUES (?, ?, ?, ?, ?, ?)"
            c.execute(sql, (self.val1, self.val2, self.val3, self.val4, self.val5, self.val6))
            conn.commit()

            tkinter.messagebox.showinfo("success", "Appointment for " + str(self.val1) + " has been created")

            # getting the number of appointments fixed to view in the log
            sql2 = "SELECT ID FROM appointments"
            self.result = c.execute(sql2)
            ids = []
            for self.row in self.result:
                self.id = self.row[0]
                ids.append(self.id)
            # ordering the ids
            self.new = sorted(ids)
            self.final_id = self.new[len(ids) - 1]

            # displaying the logs in our right frame
            self.logs = Label(self.right, text='Logs', font=("arial 18  bold"), fg='white', bg='steelblue')
            self.logs.place(x=0, y=0)

            self.box = Text(self.right, width=50, height=40)
            self.box.place(x=20, y=30)
            self.box.insert(END, "\nTotal Appointments till  now:" + str(self.final_id))
            self.box.insert(END, '\nAppointment fixed ' + str(self.final_id))
            self.box.insert(END, '\nAppointment fixed for ' + str(self.val1) + ' at ' + str(self.val5))

# create the object
root = Tk()
app = Application(root)
root.geometry('1200x720+0+0')
root.resizable(False, False)
root.mainloop()


class UpdateApplication:
    def __init__(self, master):
        self.master = master
        self.heading = Label(master, text="Update Appointments", fg='steelblue', font=('arial 40  bold'))
        self.heading.place(x=350, y=0)
        # search criteria -->name
        self.name = Label(master, text="Enter Patient's Name", font=('arial 18 bold'))
        self.name.place(x=10, y=60)

        # entry for the name
        self.name_ent = Entry(self.master, width=40)
        self.name_ent.place(x=300, y=70)

        # creating the object

        # search button
        self.search = Button(master, text="Search", width=12, height=1, bg='steelblue', command=self.search_db)
        self.search.place(x=350, y=102)

        # function to search
    def search_db(self):
        self.input = self.name_ent.get()

        # execute sql
        sql = "SELECT * FROM appointments WHERE name LIKE ?"
        self.res = c.execute(sql, (self.input,))
        rows = self.res.fetchall()  # fetch all rows

        for self.row in rows:
            self.name1 = self.row[1]
            self.age = self.row[2]
            self.gender = self.row[3]
            self.location = self.row[4]
            self.time = self.row[5]
            self.phone = self.row[6]

        # creating the update form
        self.uname = Label(self.master, text="Patient's Name", font=("arial 18 bold"))
        self.uname.place(x=0, y=150)

        self.uage = Label(self.master, text="Age", font=("arial 18 bold"))
        self.uage.place(x=0, y=200)

        self.ugender = Label(self.master, text="Gender", font=("arial 18 bold"))
        self.ugender.place(x=0, y=250)

        self.ulocation = Label(self.master, text="Location", font=("arial 18 bold"))
        self.ulocation.place(x=0, y=300)

        self.utime = Label(self.master, text="Appointment Time", font=("arial 18 bold"))
        self.utime.place(x=0, y=350)

        self.uphone = Label(self.master, text="Phone Number", font=("arial 18 bold"))
        self.uphone.place(x=0, y=400)

        # entries for each labels
        # filling the search result to entry box to update

        self.ent1 = Entry(self.master, width=40)
        self.ent1.place(x=300, y=150)
        self.ent1.insert(END, str(self.name1))

        self.ent2 = Entry(self.master, width=40)
        self.ent2.place(x=300, y=200)
        self.ent2.insert(END, str(self.age))

        self.ent3 = Entry(self.master, width=40)
        self.ent3.place(x=300, y=250)
        self.ent3.insert(END, str(self.gender))

        self.ent4 = Entry(self.master, width=40)
        self.ent4.place(x=300, y=300)
        self.ent4.insert(END, str(self.location))

        self.ent5 = Entry(self.master, width=40)
        self.ent5.place(x=300, y=350)
        self.ent5.insert(END, str(self.time))

        self.ent6 = Entry(self.master, width=40)
        self.ent6.place(x=300, y=400)
        self.ent6.insert(END, str(self.phone))

        # button to execute
        self.update = Button(self.master, text='Update', width=20, height=2, bg='lightblue', command=self.update_db)
        self.update.place(x=250, y=450)

        # button to delete
        self.delete = Button(self.master, text='Delete', width=20, height=2, bg='red', command=self.delete_db)
        self.delete.place(x=440, y=450)

    def update_db(self):
        # declaring the variable to update
        self.var1 = self.ent1.get()  # updated name
        self.var2 = self.ent2.get()
        self.var3 = self.ent3.get()
        self.var4 = self.ent4.get()
        self.var5 = self.ent5.get()
        self.var6 = self.ent6.get()

        query = "UPDATE appointments SET name=?,age=?,gender=?,location=?,schedule_time=?,phone=? WHERE name LIKE ?"
        c.execute(query, (self.var1, self.var2, self.var3, self.var4, self.var5, self.var6, self.name_ent.get(),))
        conn.commit()
        tkinter.messagebox.showinfo("Updated", "Successfully Updated.")
        self.ent1.destroy()
        self.ent2.destroy()
        self.ent3.destroy()
        self.ent4.destroy()
        self.ent5.destroy()
        self.ent6.destroy()

    def delete_db(self):
        # delete the appointment
        sql2 = "DELETE FROM appointments WHERE name LIKE ?"
        c.execute(sql2, (self.name_ent.get(),))
        conn.commit()
        tkinter.messagebox.showinfo("Success", "Deleted Successfully")


# creating the object
root_update = Tk()
b_update = UpdateApplication(root_update)
root_update.geometry('1200x720+0+0')
root_update.resizable(False, False)
root_update.mainloop()

number = []
patients = []

# retrieve data from the appointments table
sql = "SELECT * FROM appointments"
res = c.execute(sql)
for r in res:
    ids = r[0]
    name = r[1]
    number.append(ids)
    patients.append(name)

# window
class Application:
    def __init__(self, master):
        self.master = master
        self.x = 0
        self.heading = Label(master, text="Appointments", font=('arial', 90, 'bold'),fg='green')
        self.heading.place(x=300, y=0)
    
        #button to change patients
        self.change=Button(master,text="Next Patient",width=25,height=2,bg='steelblue',command=self.func)
        self.change.place(x=500,y=600)
        
        #empty text labels to later configure
        self.n=Label(master,text="",font=('arial 150 bold'))
        self.n.place(x=550,y=200)

        self.pname=Label(master,text="",font=('arial 60 bold'))
        self.pname.place(x=500,y=450)
        
        #initialize pyttsx3 engine once
        self.engine=pyttsx3.init()
        self.engine.setProperty('rate',150) #adjust the speed rate(words per minute)
        self.engine.setProperty('volume',1.0) #set volume level(0.0 to 1.0)
        
        
        #function to speak the text and update the text
    def func(self):
        self.n.config(text=str(number[self.x]))
        self.pname.config(text=str(patients[self.x]))
        
      
        voices=self.engine.getProperty('voices')
        rate=self.engine.getProperty('rate')
        self.engine.say("patient  number" +str(number[self.x])+str(patients[self.x]))
        time.sleep(0.5)
        self.engine.runAndWait()
        self.x+=1
        
# create an instance of the Application class
root = Tk()
b = Application(root)
root.geometry("1366x768+0+0")
root.resizable(False, False)
root.mainloop()
        