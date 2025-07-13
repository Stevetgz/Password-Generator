import mysql
import mysql.connector
import random
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from dotenv import load_dotenv
import os
load_dotenv()


def password_gen(passwordlevel):

    my_letter="qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
    my_symbols="!@#$%^&*()"
    numbers = "1234567890"
    with open ('filess.txt', 'r') as file:
        content = file.read().splitlines()
    text_word = random.choice(content)

    if passwordlevel == 1:
        length = 4
        merged = my_letter+numbers+my_symbols
        mergedwords = ''.join(random.choices(merged, k=length))
        passcode = f"{text_word}.{mergedwords}"
        

    elif passwordlevel ==2:
        length = 7
        merged = numbers+my_symbols+my_letter
        mergedwords = ''.join(random.choices(merged, k = length))
        passcode = f"{text_word}.{mergedwords}"

    else:
        length = 14
        my_symbols="!@#$%^&*()!@#$%^&*()[]|:<>?.,"
        chars_megred = my_letter+my_symbols+numbers
        passcode = ''.join(random.choices(chars_megred, k = length)
                           )
    
    print(f"Your passcode for is {passcode}")
    return passcode
def my_sql(password,name):
        db = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        passwd=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")

        )
        my_cursor = db.cursor()
        my_cursor.execute("""
    CREATE TABLE IF NOT EXISTS myData (
        name VARCHAR(50),
        password VARCHAR(50)
    )
""")
    
        
        
        my_cursor.execute(
            'INSERT INTO myData (name, password) VALUES (%s,%s)',
            (name,password)
        )

        db.commit()

        db.close()
    
def greet():
    try:
        passwordlevel=int(entry1.get())
    except ValueError:
        messagebox.showinfo("ERORR", "NOT VALID PASSWORD LEVEL")
        return
    
    passwordapp=entry2.get()
    if not passwordapp:
         messagebox.showinfo("ERROR","ENTER A VALID NAME")
         return
   

    

    password=password_gen(passwordlevel)
    my_sql(password,passwordapp)
    messagebox.showinfo("PASSWORD", f"YOUR PASSWORD FOR {passwordapp} IS: \n{password}")
def find_passcode():
     
    password_find = entryfind.get().strip()
    if not password_find:
        messagebox.showerror("ERROR", "Enter a valid entry")
        return
    db = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        passwd=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")

        )
    my_cursor = db.cursor()
    my_cursor.execute("SELECT password FROM myData WHERE name = %s",(password_find,))
    result = my_cursor.fetchone()
    db.close()
    if result:
        messagebox.showinfo("Password found", f"Your password for {password_find} is: \n {result[0]}")

    if not result:
        messagebox.showerror("Password not found", "Password was not found enter a valid application name")

root = tk.Tk()
root.title("Password generator and database")
root.geometry("400x800")
root.config(bg = "Royalblue1")

label1 = tk.Label(root, text="Eneter password level", bg="Royalblue1",fg="GRAY12")
label1.pack(pady=11)
entry1 = ttk.Combobox(root, values=[1,2,3])
entry1.pack(pady=11)

label2 = tk.Label(root, text="Enter application name for password", bg = "Royalblue1",fg="Gray12")
label2.pack(pady=10)
entry2 = ttk.Entry(root)
entry2.pack(pady=9)

ttk.Button(root, text="Click to generate and save password", command=greet).pack(pady=9)

labelfind = tk.Label(root, text="If you want to find a saved password enter the application name: ", bg="Royalblue1", fg="Gray12" ).pack(pady=8)
entryfind = ttk.Entry(root)
entryfind.pack(pady=7)
ttk.Button(root,text="Click to find",command=find_passcode).pack(pady=4)
root.mainloop()