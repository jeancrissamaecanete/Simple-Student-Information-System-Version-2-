from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import csv

#Main Window
root = Tk()
root.title("Student Information System")
root.geometry("825x580")
root.maxsize(825, 580)
root.iconbitmap(r'app_icon.ico')
#Frames
content = Frame(root, bg="#98B6D4")
content.place(x=0, y=50, width=1000, height=700)
subSearch = Frame(root, bg="#98B6D4")
subSearch.place(x=0, y=0, width=1200, height=50)
searchContent = Frame(root, bg="#98B6D4")
searchContent.place(x=20, y=190, width=800, height=500)
#Data Title
header = Label(content, text="Student Information", fg="#23395d", bg="#98B6D4", font=("Arial", 15, "bold"))
header.place(x=325,y=-5)
#Search Field
searchBy = Entry(subSearch, font=("Roboto", 10))
searchBy.place(x=490, y=10, height=25, width=163)
#ID Field
idnumber = Label(content, text="I.D. No. :", fg="#23395d", bg="#98B6D4", font=("Roboto", 10, "bold"))
idnumber.place(x=145, y=28)
idnumberEntry = Entry(content, font=("Roboto", 10), bg="#FFFFFF", relief=RIDGE, width=25)
idnumberEntry.place(x=210, y=30)
#Name Field
name = Label(content, text="Name :", fg="#23395d", bg="#98B6D4", font=("Roboto", 10, "bold"))
name.place(x=145, y=58)
nameEntry = Entry(content, font=("Roboto", 10), bg="#FFFFFF", relief=RIDGE, width=25)
nameEntry.place(x=210, y=60)
#Course Field
course = Label(content, text="Course :", fg="#23395d", bg="#98B6D4", font=("Roboto", 10, "bold"))
course.place(x=145, y=88)
courseEntry = Entry(content, font=("Roboto", 10), bg="#FFFFFF", relief=RIDGE,width=25)
courseEntry.place(x=210, y=90)
#Year Level Field
year = Label(content, text="Year :", fg="#23395d", bg="#98B6D4", font=("Roboto", 10, "bold"))
year.pack()
year.place(x=425, y=28)
i = ["1st Year", "2nd Year", "3rd Year", "4th Year"]
yearEntry = ttk.Combobox(content, font=("Roboto", 10), values=i)
yearEntry.pack()
yearEntry.place(x=490, y=27)
#Gender Field
gender = Label(content, text="Gender :", fg="#23395d", bg="#98B6D4", font=("Roboto", 10, "bold"))
gender.pack()
gender.place(x=425, y=55)
j = ["Male", "Female"]
genderEntry = ttk.Combobox(content, font=("Roboto", 10), values=j)
genderEntry.pack()
genderEntry.place(x=490, y=55)

def tree():
    with open("Student Data.csv") as f:
        r = csv.DictReader(f, delimiter=",")
        for row in r:
            idnumber = row["idnumber"]
            name = row["name"]
            course = row["course"]
            year = row["year"]
            gender = row["gender"]
            view.insert("", 0, values=(idnumber, name, course, year, gender))

def showall():
    view.delete(*view.get_children())
    tree()

def add():
    if nameEntry.get() == "":
        messagebox.showerror("Error", "There are some missing input.")
    elif idnumberEntry.get() == "":
        messagebox.showerror("Error", "There are some missing input.")
    elif courseEntry.get() == "":
        messagebox.showerror("Error", "There are some missing input.")
    elif yearEntry.get() == "":
        messagebox.showerror("Error", "There are some missing input.")
    elif genderEntry.get() == "":
        messagebox.showerror("Error", "There are some missing input.")

    else:
        data = []
        data.append(idnumberEntry.get())
        data.append(nameEntry.get())
        data.append(courseEntry.get())
        data.append(yearEntry.get())
        data.append(genderEntry.get())

        with open("Student Data.csv", "a", newline="") as f:
            w = csv.writer(f)
            w.writerow(data)
            view.insert("", 0, values=(data))

        nameEntry.delete(0, END)
        idnumberEntry.delete(0, END)
        courseEntry.delete(0, END)
        yearEntry.delete(0, END)
        genderEntry.delete(0, END)

        showall()

        messagebox.showinfo("Success", "Student has been added successfully.")

def remove():
    selected = view.selection()
    values = view.item(selected, "values")
    query = values[0]

    if bool(query) is False:
        pass
    else:
        data = open("Student Data.csv", "r").readlines()
        with open("Student Data.csv", "w") as csv_file:
            for row in data:
                if query in row:
                    pass
                else:
                    csv_file.write(f"{row}")
        view.delete(selected)
        showall()


def edit():
    nameEntry.delete(0, END)
    idnumberEntry.delete(0, END),
    courseEntry.delete(0, END)
    yearEntry.delete(0, END)
    genderEntry.delete(0, END)

    selected = view.focus()
    values = view.item(selected, "values")

    remove()

    nameEntry.insert(0, values[0])
    idnumberEntry.insert(0, values[1])
    courseEntry.insert(0, values[2])
    yearEntry.insert(0, values[3])
    genderEntry.insert(0, values[4])


def save():
    selected = view.focus()
    view.item(selected, text="", values=(
    nameEntry.get(), idnumberEntry.get(), courseEntry.get(), yearEntry.get(), genderEntry.get()))
    add()

    nameEntry.delete(0, END)
    idnumberEntry.delete(0, END)
    courseEntry.delete(0, END)
    yearEntry.delete(0, END)
    genderEntry.delete(0, END)


def search():
    query = searchBy.get()

    if query == "":
        messagebox.showerror("Error", "Please enter some keyword.")
    else:
        with open("Student Data.csv", "r") as f:
            for row in f:
                    if query in row:
                        view.delete(*view.get_children())
                        view.insert("", "end", values=(row.split(",")))

#Add Button
addButton = Button(content, text="Add", width=5, font=("Roboto", 10, "bold"), fg="#FFFFFF", bg="#7B9FCF", command=add)
addButton.place(x=428, y=90)
#Update Button
editButton = Button(content, text="Edit", width=5, font=("Roboto", 10, "bold"), fg="#FFFFFF", bg="#7B9FCF", command=edit)
editButton.place(x=485, y=90)
#Delete Button
deleteButton = Button(content, text="Delete", width=5, font=("Roboto", 10, "bold"), fg="#FFFFFF", bg="#7B9FCF", command=remove)
deleteButton.place(x=543, y=90)
#Save Button
saveButton = Button(content, text="Save", width=5, font=("Roboto", 10, "bold"), fg="#FFFFFF", bg="#7B9FCF", command=save)
saveButton.place(x=602, y=90)
#Show All Button
displayButton = Button(subSearch, text="Show All", width=8, font=("Roboto", 10, "bold"), fg="#FFFFFF", bg="#7B9FCF", command=showall)
displayButton.place(x=730, y=10)
#Search Button
searchButton = Button(subSearch, text="Search", width=6, font=("Roboto", 10, "bold"), fg="#FFFFFF", bg="#7B9FCF", command=search)
searchButton.place(x=665, y=10)
#Scrollbar
scrollx = Scrollbar(searchContent)
scrollx.pack(side=RIGHT, fill=Y)
#Data Table
view = ttk.Treeview(searchContent, columns=(1, 2, 3, 4, 5), show="headings", height=10, yscrollcommand=scrollx.set)
style = ttk.Style()
style.configure("Treeview.Heading", foreground="#23395d", font=("Roboto", 10, "bold"))
style.map("Treeview", background=[("selected", "#7B9FCF")])
#Headings
view.heading(1, text="I.D. Number")
view.heading(2, text="Name")
view.heading(3, text="Course")
view.heading(4, text="Year")
view.heading(5, text="Gender")
#Column Alignment
view.column(1, width=50, anchor=CENTER)
view.column(2, width=50, anchor=W)
view.column(3, width=50, anchor=CENTER)
view.column(4, width=50, anchor=CENTER)
view.column(5, width=50, anchor=CENTER)
#Scrollbar
view.place(x=0, y=0, width=760, height=370)
scrollx.config(command=view.yview)

tree()

root.mainloop()
