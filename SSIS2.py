from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox
import re

# Main Window
root = Tk()
root.title('Student Information System')
root.configure(bg="#98B6D4")
root.geometry("880x540")
root.maxsize(880, 540)
root.iconbitmap(r'app_icon.ico')
# Create Style
style = ttk.Style()
style.theme_use("clam")
#=====================================================================FRAMES====================================================================================================
# Frame for Student TreeView and Scrollbar
tree_frame = Frame(root, bg="#98B6D4")
tree_frame.place(x=225, y=95, width=645, height=225)
# Frame for Student Entries and Buttons
content_frame = Frame(root, bg="#98B6D4")
content_frame.place(x=0, y=90, width=240, height=240)
# Frame for Course TreeView and Scrollbar
tree_frame2 = Frame(root, bg="#98B6D4")
tree_frame2.place(x=0, y=335, width=500, height=190)
# Frame for Course Entries and Buttons
content_frame2 =Frame(root, bg="#98B6D4")
content_frame2.place(x=500, y=320, width=380, height=250)
# Frame for Searchbar and Title
srch = Frame(root, bg="#98B6D4")
srch.place(x=0, y=0, width=880, height=90)
# Titles
title_label = Label(srch, text="Student  Information  System", font=("Impact", 20), fg="#23395d", bg="#98B6D4")
title_label.place(x=285,y=10)
title_label = Label(content_frame, text="Student Data", font=("Impact", 17), fg="#23395d", bg="#98B6D4")
title_label.place(x=80,y=3)
title_label = Label(content_frame2, text="Course Data", font=("Impact", 17), fg="#23395d", bg="#98B6D4")
title_label.place(x=115,y=13)
#===================================================================FUNCTIONS============================================================================================================
# Create Database
def sisdb():
    connect = sqlite3.connect('SIS.db')
    cursor = connect.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS "Course"(
        Course_Code TEXT,
        Course_Name TEXT,
        PRIMARY KEY(Course_Code)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS "Student"(
        ID_number TEXT NOT NULL,
        Name TEXT   NOT NULL,
        Course  TEXT NOT NULL,
        Year_Level TEXT NOT NULL,
        Gender TEXT NOT NULL,
        PRIMARY KEY(ID_number),
        FOREIGN KEY(Course_Code) REFERENCES Course(Course_Code)
        );
    """)
    connect.close()
    return 0

def search(): # Search Student
    query = search_entry.get()
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
            search_entry.delete(0, END)
            return
        else:
            query = '%s-%s' % (query[:4], query[4:8])
    except ValueError:
        messagebox.showerror("Error", "Please enter only the I.D. No. to search for a student.")
        search_entry.delete(0, END)
        return

    conn = sqlite3.connect('SIS.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Student WHERE ID_number=? ", (query,))
    records = c.fetchall()
    if len(records) == 1:
        records = records[0]
        records = f"{str(records[0])},{records[1]},{records[2]},{records[3]},{records[4]}"
        my_tree.delete(*my_tree.get_children())
        my_tree.insert("", "end", values=(records.split(",")))
        messagebox.showinfo("Success", "Student is found.")
        return
    else:
        messagebox.showerror("Error", "Student does not exists. Please try again.")
        search_entry.delete(0, END)
        return

def add(): # Add Student
    a1 = id_number.get()
    a2 = name_entry.get()
    a3 = course_entry.get()
    a4 = year_entry.get()
    a5 = gender_entry.get()
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
            conn = sqlite3.connect('SIS.db')
            c = conn.cursor()
            c.execute("INSERT INTO Student VALUES (:id_number, :name, :course, :year_level, :gender)",
                      {
                          'id_number': id_number.get(),
                          'name': name_entry.get(),
                          'course': course_entry.get(),
                          'year_level': year_entry.get(),
                          'gender': gender_entry.get()
                      }
                      )
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Student has been added successfully.")
            delete_data()
            displaydata()
        except:
            messagebox.showerror("Error", "Student already exists.")
            return
    clear()

def delete_data(): # Delete Data from the Table
    for record in my_tree.get_children():
        my_tree.delete(record)

def delete(): # Delete Student
    if not my_tree.selection():
        messagebox.showerror('Error', 'Please select a student first to delete.')
        return
    decision = messagebox.askquestion("Confirmation", "Do you want to delete the selected student?")
    if decision == "no":
        pass
        clear()
        return
    else:
        conn = sqlite3.connect("SIS.db")
        c = conn.cursor()
        selected = my_tree.focus()
        values = my_tree.item(selected, 'values')
        c.execute("DELETE from Student WHERE ID_number=?", (values[0],))
        conn.commit()
        conn.close()
        messagebox.showinfo('Succes', 'Student has been deleted successfully.')
    clear()
    delete_data()
    displaydata()

def select_record(e):
    id_number.delete(0, END)
    name_entry.delete(0, END)
    course_entry.delete(0, END)
    year_entry.delete(0, END)
    gender_entry.delete(0, END)

    selected = my_tree.focus()
    values = my_tree.item(selected, 'values')

    id_number.insert(0, values[0])
    name_entry.insert(0, values[1])
    course_entry.insert(0, values[2])
    year_entry.insert(0, values[3])
    gender_entry.insert(0, values[4])
    clear2()

def modify(): # Edit Student
    if not my_tree.selection():
        messagebox.showerror('Error', 'Please select a student first to edit.')
        return
    decision = messagebox.askquestion("Confirmation", "Do you want to save changes?")
    if decision == "no":
        pass
        return
    data1 = id_number.get()
    data2 = name_entry.get()
    data3 = course_entry.get()
    data4 = year_entry.get()
    data5 = gender_entry.get()
    if (data1 == '') or (data2 == '') or (data3 == '') or (data4 == '') or (data5 == ''):
        messagebox.showerror("Error", "Please fill all the missing input.")
        return
    else:
        try:
            conn = sqlite3.connect('SIS.db')
            c = conn.cursor()
            selected = my_tree.selection()
            my_tree.item(selected, values=(data1, data2, data3, data4, data5))
            c.execute(
                "UPDATE Student set  ID_number=?, Name=?, Course=?, Year_Level=?, Gender=?  WHERE ID_number=? ",
                (data1, data2, data3, data4, data5, data1))
            conn.commit()
            conn.close()
            messagebox.showinfo('Succes', 'Student has been updated successfully.')
        except:
            messagebox.showerror("Error", "Updating student is unsuccessful.")
            return
    clear()
    delete_data()
    displaydata()

def displaydata():
    conn = sqlite3.connect('SIS.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Student")
    records = c.fetchall()

    global count
    count = 0

    for record in records:
        if count % 2 == 0:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2],
                                                                               record[3], record[4]), tags=('evenrow',))
        else:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2],
                                                                               record[3], record[4]), tags=('oddrow',))
        count += 1
    return

def displaydata2():
    conn = sqlite3.connect('SIS.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Course")
    records = c.fetchall()

    global count2
    count2 = 0

    for record in records:
        if count2 % 2 == 0:
            my_tree2.insert(parent='', index='end', iid=count2, text='', values=(record[0], record[1]), tags=('evenrow',))
        else:
            my_tree2.insert(parent='', index='end', iid=count2, text='', values=(record[0], record[1]), tags=('oddrow',))
        count2 += 1
    return

def delete_data2():
    for record in my_tree2.get_children():
        my_tree2.delete(record)

def clear():
    id_number.delete(0, END)
    name_entry.delete(0, END)
    course_entry.delete(0, END)
    year_entry.delete(0, END)
    gender_entry.delete(0, END)

    course_entry.set("Select Course")
    year_entry.set("Select Year Level")
    gender_entry.set("Select Gender")

def add2():
    b1 = ccode_entry.get()
    b2 = cname_entry.get()
    if (b1 == '') or (b2 == ''):
        messagebox.showerror("Error", "Please fill all the missing input.")
        return
    pattern = re.compile("^[a-zA-Z]+$")
    if not pattern.match(b1):
        messagebox.showerror("Error", "Course code must only contain letters.")
        return

    conn = sqlite3.connect('SIS.db')
    c = conn.cursor()

    c.execute("INSERT INTO Course VALUES (:code, :name)",
              {
                  'code': ccode_entry.get(),
                  'name': cname_entry.get(),
              }
              )
    conn.commit()
    conn.close()
    addCourse()
    messagebox.showinfo("Success", "Course has been added successfully.")
    delete_data2()
    displaydata2()
    clear2()

    return

def delete2():
    if not my_tree2.selection():
        messagebox.showerror('Error', 'Please select a course first to delete.')
        return
    decision = messagebox.askquestion("Confirmation", "Do you want to delete the selected course?")
    if decision == "no":
        pass
        clear2()
        return
    else:
        conn = sqlite3.connect("SIS.db")
        c = conn.cursor()
        selected = my_tree2.focus()
        values = my_tree2.item(selected, 'values')

        c.execute("DELETE from Course WHERE Course_Code=?", (values[0],))
        conn.commit()
        conn.close()
        messagebox.showinfo('Succes', 'Course has been deleted successfully.')

    clear2()
    addCourse()
    delete_data2()
    displaydata2()

def modify2():
    if not my_tree2.selection():
        messagebox.showerror('Error', 'Please select a course first to edit.')
        return
    decision = messagebox.askquestion("Confirmation", "Do you want to save changes?")
    if decision == "no":
        pass
        return
    data1 = ccode_entry.get()
    data2 = cname_entry.get()
    if (data1 == '') or (data2 == ''):
        messagebox.showerror("Error", "Please fill all the missing input.")
        return
    else:
        try:
            conn = sqlite3.connect('SIS.db')
            c = conn.cursor()
            selected = my_tree2.selection()
            my_tree2.item(selected, values=(data1, data2))
            c.execute(
                "UPDATE Course set  Course_Code=?, Course_Name=? WHERE Course_Code=? ",
                (data1, data2, data1))
            conn.commit()
            conn.close()
            messagebox.showinfo("Succes", "Course has been updated successfully.")
        except:
            messagebox.showerror("Error", "Updating course is unsuccessful.")
            return
    clear2()
    delete_data2()
    displaydata2()

def clear2():
    ccode_entry.delete(0, END)
    cname_entry.delete(0, END)

def select_record2(e):
    ccode_entry.delete(0, END)
    cname_entry.delete(0, END)

    selected = my_tree2.focus()
    values = my_tree2.item(selected, 'values')

    ccode_entry.insert(0, values[0])
    cname_entry.insert(0, values[1])
    clear()

def search2(): # Search Student
    query1 = search_entry2.get()
    if query1 == "":
        messagebox.showerror("Error", "Please enter a course code to search for a course.")
        return
    pattern2 = re.compile("^[a-zA-Z]+$")
    if not pattern2.match(query1):
        messagebox.showerror("Error", "Course code must only contain letters.")
        search_entry2.delete(0, END)
        return
    conn = sqlite3.connect('SIS.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Course WHERE Course_Code=? ", (search_entry2.get(),))
    records = c.fetchall()
    if len(records) == 1:
        records = records[0]
        records = f"{str(records[0])},{records[1]}"
        my_tree2.delete(*my_tree2.get_children())
        my_tree2.insert("", "end", values=(records.split(",")))
        messagebox.showinfo("Success", "Course is found.")
        return
    else:
        messagebox.showerror("Error", "Course does not exists. Please try again.")
        return

def refresh():
    search_entry.delete(0, END)
    search_entry2.delete(0, END)
    delete_data()
    delete_data2()
    clear()
    clear2()
    displaydata()
    displaydata2()
    return

def addCourse():
    ex = sqlite3.connect('SIS.db')
    x = ex.cursor()

    x.execute("SELECT Course_Code FROM Course")
    rec = x.fetchall()
    xlist = []
    for i in rec:
        xlist.append(i[0])

    course_entry = ttk.Combobox(content_frame, font=("Roboto", 10), width=18)
    course_entry.set("Select Course")
    course_entry['values'] = xlist  # ("BSCS", "BSIT", "BSBA-B.ECON")
    course_entry.place(x=85, y=100)

ex = sqlite3.connect('SIS.db')
x = ex.cursor()
x.execute("SELECT Course_Code FROM Course")
rec = x.fetchall()
xlist = []
for i in rec:
    xlist.append(i[0])

#==========================================================================ENTRIES=================================================================================================
#ID Field
idnumber1 = Label(content_frame, text="I.D. No. :", fg="#23395d", bg="#98B6D4", font=("Roboto", 10, "bold"))
idnumber1.place(x=20, y=39)
id_number = Entry(content_frame, font=("Roboto", 10), bg="#FFFFFF", relief=RIDGE, width=20)
id_number.place(x=85, y=40)
#Name Field
name1 = Label(content_frame, text="Name :", fg="#23395d", bg="#98B6D4", font=("Roboto", 10, "bold"))
name1.place(x=20, y=69)
name_entry = Entry(content_frame, font=("Roboto", 10), bg="#FFFFFF", relief=RIDGE, width=20)
name_entry.place(x=85, y=70)
#Course Field
course1 = Label(content_frame, text="Course :", fg="#23395d", bg="#98B6D4", font=("Roboto", 10, "bold"))
course1.place(x=20, y=99)
course_entry = ttk.Combobox(content_frame, font=("Roboto", 10), width=18)
course_entry.set("Select Course")
course_entry['values'] = xlist
course_entry.place(x=85, y=100)
#Year Field
year1 = Label(content_frame, text="Year :", fg="#23395d", bg="#98B6D4", font=("Roboto", 10, "bold"))
year1.place(x=20, y=129)
year_entry = ttk.Combobox(content_frame, font=("Roboto", 10), width=18)
year_entry.set("Select Year Level")
year_entry['values'] = ("1st", "2nd", "3rd", "4th")
year_entry.place(x=85, y=129)
#Gender Field
gender1 = Label(content_frame, text="Gender :", fg="#23395d", bg="#98B6D4", font=("Roboto", 10, "bold"))
gender1.place(x=20, y=159)
gender_entry = ttk.Combobox(content_frame, font=("Roboto", 10), width=18)
gender_entry.set("Select Gender")
gender_entry['values'] = ("Male", "Female")
gender_entry.place(x=85, y=159)
#Course Code Field
cc = Label(content_frame2, text="Course Code :", fg="#23395d", bg="#98B6D4", font=("Roboto", 10, "bold"))
cc.place(x=10, y=109)
ccode_entry = Entry(content_frame2, font=("Roboto", 10), bg="#FFFFFF", relief=RIDGE, width=27)
ccode_entry .place(x=120, y=110)
#Course Name Field
cn = Label(content_frame2, text="Course Name :", fg="#23395d", bg="#98B6D4", font=("Roboto", 10, "bold"))
cn.place(x=10, y=139)
cname_entry = Entry(content_frame2, font=("Roboto", 10), bg="#FFFFFF", relief=RIDGE, width=27)
cname_entry.place(x=120, y=140)
#Search Course Field
search_entry = Entry(srch, font=("Roboto", 10), bg="#FFFFFF", relief=RIDGE, width=25)
search_entry.place(x=530, y=60)
search_entry2 = Entry(content_frame2, font=("Roboto", 10), bg="#FFFFFF", relief=RIDGE, width=15)
search_entry2.place(x=120, y=60)
#=====================================================================BUTTONS========================================================================================
#Search Button
search_btn = Button(srch, text="Search", font=("Roboto", 10, "bold"), fg="#FFFFFF", bg="#7B9FCF", command=search)
search_btn.place(x=715, y=55)
search_btn2 = Button(content_frame2, text="Search", font=("Roboto", 10, "bold"), fg="#FFFFFF", bg="#7B9FCF", command=search2)
search_btn2.place(x=235, y=55)
#Refresh Button
refresh_btn = Button(srch, text="Refresh", font=("Roboto", 10, "bold"), fg="#FFFFFF", bg="#7B9FCF", command=refresh)
refresh_btn.place(x=780, y=55)
refresh_btn2 = Button(content_frame2, text="Refresh", font=("Roboto", 10, "bold"), fg="#FFFFFF", bg="#7B9FCF", command=refresh)
refresh_btn2.place(x=300, y=55)
#Add Button
add_btn = Button(content_frame, text="Add", width=4, font=("Roboto", 10, "bold"), fg="#FFFFFF", bg="#7B9FCF", command=add)
add_btn.place(x=23, y=200)
add_btn2 = Button(content_frame2, text="Add", width=5, font=("Roboto", 10, "bold"), fg="#FFFFFF", bg="#7B9FCF", command=add2)
add_btn2.place(x=120, y=180)
#Delete Button
del_btn = Button(content_frame, text="Delete", width=6, font=("Roboto", 10, "bold"), fg="#FFFFFF", bg="#7B9FCF", command=delete)
del_btn.place(x=73, y=200)
del_btn2 = Button(content_frame2, text="Delete", width=6, font=("Roboto", 10, "bold"), fg="#FFFFFF", bg="#7B9FCF", command=delete2)
del_btn2.place(x=180, y=180)
#Edit Button
mod_btn = Button(content_frame, text="Edit", width=4, font=("Roboto", 10, "bold"), fg="#FFFFFF", bg="#7B9FCF", command=modify)
mod_btn.place(x=139, y=200)
mod_btn2 = Button(content_frame2, text="Edit", width=5, font=("Roboto", 10, "bold"), fg="#FFFFFF", bg="#7B9FCF",command=modify2)
mod_btn2.place(x=250, y=180)
#Clear Button
clr_btn = Button(content_frame, text="Clear", width=5, font=("Roboto", 10, "bold"), fg="#FFFFFF", bg="#7B9FCF", command=clear)
clr_btn.place(x=188, y=200)
clr_btn2 = Button(content_frame2, text="Clear", width=5, font=("Roboto", 10, "bold"), fg="#FFFFFF", bg="#7B9FCF",command=clear2)
clr_btn2.place(x=310, y=180)
#=====================================================================TREEVIEWS=============================================================================================
# Student Treeview Scrollbar
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)
# Add Student TreeView
my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
my_style = ttk.Style()
my_style.configure("Treeview.Heading", font=("Roboto", 10))
my_style.configure("Treeview", font=("Roboto", 10))
my_tree['columns'] = ('ID number', 'Name', 'Course', 'Year Level', 'Gender')
# Columns
my_tree.column("#0", stretch=NO, width=0)
my_tree.column("ID number", width=100, anchor=CENTER)
my_tree.column("Name", width=190, anchor=CENTER)
my_tree.column("Course", width=120, anchor=CENTER)
my_tree.column("Year Level", width=90, anchor=CENTER)
my_tree.column("Gender", width=90, anchor=CENTER)
# Headings
my_tree.heading("ID number", text='ID Number', anchor=CENTER)
my_tree.heading("Name", text='Name', anchor=CENTER)
my_tree.heading("Course", text='Course', anchor=CENTER)
my_tree.heading("Year Level", text='Year Level', anchor=CENTER)
my_tree.heading("Gender", text='Gender', anchor=CENTER)
my_tree.pack()
# Configure Student Treeview Scrollbar
my_tree.place(x=25, y=0, width=600, height=300)
tree_scroll.config(command=my_tree.yview)
# Course Treeview Scrollbar
tree_scroll2 = Scrollbar(tree_frame2)
tree_scroll2.pack(side=RIGHT, fill=Y)
# Add Course TreeView
my_tree2 = ttk.Treeview(tree_frame2, yscrollcommand=tree_scroll2.set)
my_style2 = ttk.Style()
my_style2.configure("Treeview", font=("Roboto", 10))
my_tree2['columns'] = ('Course Code', 'Course Name')
# Columns
my_tree2.column("#0", stretch=NO, width=0)
my_tree2.column("Course Code", width=120, anchor=CENTER)
my_tree2.column("Course Name", width=250, anchor=CENTER)
# Headings
my_tree2.heading("Course Code", text='Course Code', anchor=CENTER)
my_tree2.heading("Course Name", text='Course Name', anchor=CENTER)
my_tree2.pack()
# Configure Course Treeview Scrollbar
my_tree2.place(x=20, y=0, width=460, height=190)
tree_scroll2.config(command=my_tree2.yview)
sisdb() # Connect to Database
# Display data on Student Tree_view
displaydata()
displaydata2()
# Bindings
my_tree.bind("<ButtonRelease-1>", select_record)
my_tree2.bind("<ButtonRelease-1>", select_record2)
search_entry2.bind("<KeyRelease>", search2)
search_entry.bind("<KeyRelease>", search)

root.mainloop()
