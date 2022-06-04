import sqlite3

class Database:
    def __init__(self, db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
        sql = """
        CREATE TABLE IF NOT EXISTS students(
            rollno Integer Primary Key,
            idnumber Integer Not Null Unique,
            name text,
            course text,
            year text,
            gender text
        )
        """
        self.cur.execute(sql)
        self.con.commit()

    # Add data
    def insert(self, idnumber, name, course, year, gender):
        self.cur.execute("insert into students values (NULL,?,?,?,?,?)",
                         (idnumber, name, course, year, gender))
        self.con.commit()

    # Fetch data
    def fetch(self):
        self.cur.execute("SELECT * from students")
        rows = self.cur.fetchall()
        # print(rows)
        return rows

    # Delete data
    def delete(self, rollno):
        self.cur.execute("delete from students where rollno=?", (rollno,))
        self.con.commit()

    # Update data
    def update(self, rollno='', idnumber='', name='', course='', year='', gender=''):
        self.cur.execute(
            "update students set idnumber=?, name=?, course=?, year=?, gender=? where rollno=?",
            (idnumber, name, course, year, gender, rollno))
        self.con.commit()
    
    # Search data
    def search(self, idnumber =""):
        self.cur.execute(f"SELECT * FROM students WHERE idnumber='{idnumber}'")
        rows = self.cur.fetchall()
        return rows

