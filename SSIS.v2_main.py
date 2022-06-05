from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from db import Database

db = Database("Students.db")

#Main Window
root = Tk()
root.title("Student Information System")
root.geometry("825x580")
root.maxsize(825, 580)
root.iconbitmap(r'app_icon.ico')

idnumber = StringVar()
name = StringVar()
course = StringVar()
year = StringVar()
gender = StringVar()


#====================================================================Display=====================================================================================
#Frames
content = Frame(root, bg="#98B6D4")
content.place(x=0, y=50, width=1000, height=700)
subSearch = Frame(root, bg="#98B6D4")
subSearch.place(x=0, y=0, width=1200, height=50)
searchContent = Frame(root, bg="#98B6D4")
searchContent.place(x=20, y=190, width=800, height=370)
#Data Title
header = Label(content, text="Student Information", fg="#23395d", bg="#98B6D4", font=("Arial", 15, "bold"))
header.place(x=325,y=-5)
#Search Field
searchBy = Entry(subSearch, font=("Roboto", 10))
searchBy.place(x=490, y=10, height=25, width=163)
#ID Field
idnumber1 = Label(content, text="I.D. No. :", fg="#23395d", bg="#98B6D4", font=("Roboto", 10, "bold"))
idnumber1.place(x=145, y=28)
idnumberEntry = Entry(content, font=("Roboto", 10), bg="#FFFFFF", relief=RIDGE, width=25)
idnumberEntry.place(x=210, y=30)
#Name Field
name1 = Label(content, text="Name :", fg="#23395d", bg="#98B6D4", font=("Roboto", 10, "bold"))
name1.place(x=145, y=58)
nameEntry = Entry(content, font=("Roboto", 10), bg="#FFFFFF", relief=RIDGE, width=25)
nameEntry.place(x=210, y=60)
#Course Field
course1 = Label(content, text="Course :", fg="#23395d", bg="#98B6D4", font=("Roboto", 10, "bold"))
course1.place(x=145, y=88)
courseEntry = Entry(content, font=("Roboto", 10), bg="#FFFFFF", relief=RIDGE,width=25)
courseEntry.place(x=210, y=90)
#Year Level Field
year1 = Label(content, text="Year :", fg="#23395d", bg="#98B6D4", font=("Roboto", 10, "bold"))
year1.pack()
year1.place(x=425, y=28)
i = ["1st", "2nd", "3rd", "4th"]
yearEntry = ttk.Combobox(content, font=("Roboto", 10), values=i)
yearEntry.pack()
yearEntry.place(x=490, y=27)
#Gender Field
gender1 = Label(content, text="Gender :", fg="#23395d", bg="#98B6D4", font=("Roboto", 10, "bold"))
gender1.pack()
gender1.place(x=425, y=55)
j = ["Male", "Female"]
genderEntry = ttk.Combobox(content, font=("Roboto", 10), values=j)
genderEntry.pack()
genderEntry.place(x=490, y=55)

#===================================================================Functions=================================================================================


def clear(): # Clears all the entries
    nameEntry.delete(0, END)
    idnumberEntry.delete(0, END)
    courseEntry.delete(0, END)
    yearEntry.delete(0, END)
    genderEntry.delete(0, END)


clear()

def fetchdata(): # Gets all the data
    view.delete(*view.get_children())
    count = 0
    for row in db.fetch():
        count += 1
        view.insert("",0,values=(count,row[1],row[2],row[3],row[4],row[5]))

def showall(): # Displays all the data and refreshes
    view.delete(*view.get_children())
    for row in db.fetch():
        view.insert("", END, values=row)
    clear()

def add(): # Add a student
    a1 = idnumberEntry.get()
    a2 = nameEntry.get()
    a3 = courseEntry.get()
    a4 = yearEntry.get()
    a5 = genderEntry.get()

    try:
        if (a1 == '') or (a2 == '') or (a3 == '') or (a4 == '') or (a5 == ''):
            messagebox.showerror("Error", "Please fill all the missing input.")
            return

        y = str(a1)
        y = str(y.replace('-', ''))
        a1 = int(y)
        a1 = str(a1)
        if len(a1) != 8:
            messagebox.showerror("Error", "I.D. No. must be exactly 8 numbers.\n(Ex: 2020-1570)")
            return
        else:
            a1 = '%s-%s' % (a1[:4], a1[4:8])
    except ValueError:
        messagebox.showerror("Error", "I.D. No. must only contain numbers.")
        return
    else:
        try:
            db.insert(idnumberEntry.get(), nameEntry.get(), courseEntry.get(), yearEntry.get(), genderEntry.get())
            messagebox.showinfo("Success", "Student has been added successfully.")
            showall()
        except:
            messagebox.showerror("Error", "Student already exists.")
            return

    clear()
    showall()

def edit(): # Update a student
    selected_student = ""
    try:
        selected_item = view.selection()[0]
        selected_student = str(view.item(selected_item)['values'][0])
        decision = messagebox.askquestion("Warning", "Do you want to update the selected student?")
        if decision == "yes":
            selected = view.focus()
            values = view.item(selected, "values")

            clear()

            idnumberEntry.insert(0, values[1])
            nameEntry.insert(0, values[2])
            courseEntry.insert(0, values[3])
            yearEntry.insert(0, values[4])
            genderEntry.insert(0, values[5])

    except:
        messagebox.showerror("Error", "Please select a student first to edit.")
        return

def remove(): #Delete a student
    if not view.selection():
        messagebox.showerror('Error', 'Please select a student first to delete.')

    else:
        selected = view.focus()
        values = view.item(selected)
        selection = values["values"]
        decision = messagebox.askquestion("Warning", "Do you want to delete the selected student?")
        if decision == "yes":
            view.delete(selected)
            db.delete(selection[0])
            messagebox.showinfo("Success", "Student has been deleted successfully.")
            showall()
        else:
            return

def save(): # Save an updated student

    a1 = idnumberEntry.get()
    a2 = nameEntry.get()
    a3 = courseEntry.get()
    a4 = yearEntry.get()
    a5 = genderEntry.get()

    try:
        if (a1 == '') or (a2 == '') or (a3 == '') or (a4 == '') or (a5 == ''):
            messagebox.showerror("Error", "Please select the edit button first to save changes.")
            return
        y = str(a1)
        y = str(y.replace('-', ''))
        a1 = int(y)
        a1 = str(a1)
        if len(a1) != 8:
            messagebox.showerror("Error", "I.D. No. must be exactly 8 numbers.\n(Ex: 2020-1570)")
            return
        else:
            a1 = '%s-%s' % (a1[:4], a1[4:8])

    except ValueError:
        messagebox.showerror("Error", "I.D. No. must only contain numbers.")
        return


    selected_student = ""

    try:
        selected_item = view.selection()[0]
        selected_student = str(view.item(selected_item)['values'][0])
    except:
        messagebox.showinfo("Error", "Please edit a student first to save changes.")

    idnumber = str(idnumberEntry.get())
    name = str(nameEntry.get())
    course = str(courseEntry.get())
    year = str(yearEntry.get())
    gender = str(genderEntry.get())

    if (idnumber == "" or idnumber == " ") or (name == "" or name == " ") or (course == "" or course == " ") or (
            year == "" or year == " ") or (gender == "" or gender == " "):
        messagebox.showinfo("Error", "Please fill up the blank entry")
        return
    else:
        try:
            db.update(selected_student[0],idnumberEntry.get(),nameEntry.get(),courseEntry.get(),yearEntry.get(),genderEntry.get())
            decision = messagebox.askquestion("Warning", "Do you want to save changes?")
            if decision == "yes":
                messagebox.showinfo("Success", "Student has been updated successfully.")
        except:
            messagebox.showinfo("Unsuccessful", "Updating student unsuccessful. Please try again.")
            return
    showall()


def search(): # Search a student by I.D. Number

    query = searchBy.get()

    if query == "":
        messagebox.showerror("Error", "Please enter an I.D. No. first to search for a student.")
        return
    try:
        y = str(query)
        y = str(y.replace('-', ''))
        query = int(y)
        query = str(query)

        if len(query) != 8:
            messagebox.showerror("Error", "I.D. No. must be exactly 8 numbers.\n( Ex: 2020-1570 )")
            return
        else:
            query = '%s-%s' % (query[:4], query[4:8])
    except ValueError:
        messagebox.showerror("Error", "Please enter only the I.D. No. to search for a student.")
        return

    row = db.search(query)

    if len(row) == 1:
        row = row[0]
        row = f"{str(row[0])},{row[1]},{row[2]},{row[3]},{row[4]},{row[5]}"

        view.delete(*view.get_children())
        view.insert("", "end", values=(row.split(",")))
        messagebox.showinfo("Success", "Student is found.")
        return

    else:
        messagebox.showerror("Error", "Student does not exists. Please try again.")
        return

#===================================================================Buttons==================================================================================
#Add Button
addButton = Button(content, text="Add", width=5, font=("Roboto", 10, "bold"), fg="#FFFFFF", bg="#7B9FCF", command=add)
addButton.place(x=428, y=90)
#Delete Button
deleteButton = Button(content, text="Delete", width=5, font=("Roboto", 10, "bold"), fg="#FFFFFF", bg="#7B9FCF", command=remove)
deleteButton.place(x=485, y=90)
#Edit Button
editButton = Button(content, text="Edit", width=5, font=("Roboto", 10, "bold"), fg="#FFFFFF", bg="#7B9FCF", command=edit)
editButton.place(x=543, y=90)
#Save Button
saveButton = Button(content, text="Save", width=5, font=("Roboto", 10, "bold"), fg="#FFFFFF", bg="#7B9FCF", command=save)
saveButton.place(x=602, y=90)
#Show All Button
displayButton = Button(subSearch, text="Refresh", width=8, font=("Roboto", 10, "bold"), fg="#FFFFFF", bg="#7B9FCF", command=showall)
displayButton.place(x=730, y=10)
#Search Button
searchButton = Button(subSearch, text="Search", width=6, font=("Roboto", 10, "bold"), fg="#FFFFFF", bg="#7B9FCF", command=search)
searchButton.place(x=665, y=10)

#===================================================================Data Table==================================================================================
#Scrollbar
scrollx = Scrollbar(searchContent)
scrollx.pack(side=RIGHT, fill=Y)
#Data Table
view = ttk.Treeview(searchContent, columns=(1, 2, 3, 4, 5, 6), show="headings", height=10, yscrollcommand=scrollx.set)
style = ttk.Style()
style.configure("Treeview.Heading", foreground="#23395d", font=("Roboto", 10, "bold"))
style.map("Treeview", background=[("selected", "#7B9FCF")])
#Headings
view.heading(1, text="Roll Number")
view.heading(2, text="I.D. Number ")
view.heading(3, text="Name")
view.heading(4, text="Course")
view.heading(5, text="Year")
view.heading(6, text="Gender")
#Column Alignment
view.column(1, width=5, anchor=CENTER)
view.column(2, width=5, anchor=CENTER)
view.column(3, width=120, anchor=W)
view.column(4, width=5, anchor=CENTER)
view.column(5, width=5, anchor=CENTER)
view.column(6, width=5, anchor=CENTER)
#Scrollbar
view.place(x=0, y=0, width=760, height=370)
scrollx.config(command=view.yview)

fetchdata()

root.mainloop()
