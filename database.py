import tkinter, random, ast, sqlite3, re
from tkinter import messagebox
from tkinter import ttk

#Window Settings
screen = tkinter.Tk()
screen.title('Business Partners')
screen.geometry('1000x500+300+200')
screen.configure(bg="white")
screen.resizable(False,False)
photo = tkinter.PhotoImage(file = "assets\login_icon.png")
screen.iconphoto(False, photo)


##############################################################################
#Fucntion is an entry form that inserts values into the table
def data_entry():
    #Sponsor Info
    name = sponsor_name_entry.get()
    org_box = sponsor_org_box.get()
    resources = sponsor_resource_box.get()

    #Contact Info
    contact_first = contact_first_entry.get()
    contact_last = contact_last_entry.get()

    email = email_entry.get()
        #Email Validation
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if (re.fullmatch(regex,email)):
        pass
    else:
        email = ""
        email_entry.delete(0,'end')
        messagebox.showerror("Invalid input","Invalid email")

    phone = phone_entry.get()
        #Phone Number Validation
    try: 
        int(phone)
    except ValueError:
        phone = ""
        phone_entry.delete(0,'end')
        messagebox.showerror("Invalid input","Invalid number")
    if len(phone) != 10:
        phone = ""
        phone_entry.delete(0,'end')
        messagebox.showerror("Invalid input","Invalid number")


    print(name, org_box, resources, contact_first, email, phone)

    if name != "" and org_box != "" and resources != "" and contact_first != "" and contact_last != "" and email != "" and phone != "":
        #Datebase Storage
        connection = sqlite3.connect('sponsors.db')
        table_create_query = '''CREATE TABLE IF NOT EXISTS Sponsor_Data
                (name TEXT, 
                type TEXT, 
                resources TEXT, 
                contact_first TEXT, 
                contact_last TEXT,
                email TEXT, phone INT)
        '''

        connection.execute(table_create_query)

        data_insert_query ='''INSERT INTO Sponsor_Data 
        (name,
        type,
        resources,
        contact_first,
        contact_last,
        email,
        phone)
        VALUES(?,?,?,?,?,?,?)
        '''
            
        data_insert_tuple = (name,org_box,resources,contact_first,contact_last,email,phone)
            
        cursor = connection.cursor()
        cursor.execute(data_insert_query,data_insert_tuple)
        connection.commit()
        data = cursor.execute("SELECT * FROM Sponsor_Data")
        
        for d in database_tree.get_children():
            database_tree.delete(d)
        for d in data:
            database_tree.insert(parent= '', index=tkinter.END, values=(d[0],d[1],d[2],(f"{d[3]} {d[4]}"),d[5],d[6]))

        connection.close()

        sponsor_name_entry.delete(0,'end')
        sponsor_org_box.delete(0,'end')
        sponsor_resource_box.delete(0,'end')
        contact_first_entry.delete(0,'end')
        contact_last_entry.delete(0,'end')
        email_entry.delete(0,'end')
        phone_entry.delete(0,'end')

        database_tree.pack(fill='y', expand=True)
    else:
        messagebox.showerror("Invalid Input","Not all textboxes have been filled")
##############################################################################

##############################################################################
#Function prints data of item selected
# def item_select(_):
#     for i in database_tree.selection():
#         print(database_tree.item(i)['values'])
##############################################################################

##############################################################################
#Function deletes item selected thens adds previous data to entry form to allow edits
def edit():
    for i in database_tree.selection():
        sponsor_name_entry.insert(0,database_tree.item(i)['values'][0])
        sponsor_org_box.insert(0,database_tree.item(i)['values'][1])
        sponsor_resource_box.insert(0,database_tree.item(i)['values'][2])
        name = database_tree.item(i)['values'][3].split(" ")
        contact_first_entry.insert(0,name[0])
        contact_last_entry.insert(0,name[1])
        email_entry.insert(0,database_tree.item(i)['values'][4])
        phone_entry.insert(0,database_tree.item(i)['values'][5])

        d = database_tree.item(i)['values'][0]
        connection = sqlite3.connect('sponsors.db')
        cursor = connection.cursor()
        delete_query = f"DELETE FROM Sponsor_Data WHERE name=?"
        cursor.execute(delete_query, (d,))
        connection.commit()

        data = cursor.execute("SELECT * FROM Sponsor_Data")

        for d in database_tree.get_children():
            database_tree.delete(d)
        for d in data:
            database_tree.insert(parent= '', index=tkinter.END, values=(d[0],d[1],d[2],(f"{d[3]} {d[4]}"),d[5],d[6]))
        connection.close()
##############################################################################

##############################################################################
#Function deletes item selected in the table
def delete_item():
    for i in database_tree.selection():
        d = database_tree.item(i)['values'][0]
        connection = sqlite3.connect('sponsors.db')
        cursor = connection.cursor()
        delete_query = f"DELETE FROM Sponsor_Data WHERE name=?"
        cursor.execute(delete_query, (d,))
        connection.commit()

        data = cursor.execute("SELECT * FROM Sponsor_Data")

        for d in database_tree.get_children():
            database_tree.delete(d)
        for d in data:
            database_tree.insert(parent= '', index=tkinter.END, values=(d[0],d[1],d[2],(f"{d[3]} {d[4]}"),d[5],d[6]))
        connection.close()
##############################################################################

##############################################################################
#Function prompts user if they want to close their screen | If yes application closes | If no application stays the same
def quit():
    res = messagebox.askquestion('Exit Application', "Are you sure you want to leave")
    if res == 'yes':
        screen.destroy()
    else:
        messagebox.showinfo('Canceled', "Returning back to application")
##############################################################################  

##############################################################################
#Fucntion searchs for items by type
def search(): 
    s = search_box.get()
    t = search_by.get()
    ls = ['Name','Type', 'Resources','Contact','Email','Phone']

    for d in database_tree.get_children():
        database_tree.delete(d)

    connection = sqlite3.connect('sponsors.db')
    cursor = connection.cursor()   

    if t in ls:
        if t == 'Contact':
            data = cursor.execute(f"SELECT * FROM Sponsor_Data WHERE contact_first LIKE '%{s}%' OR contact_last LIKE '%{s}%'")
        else:
            data = cursor.execute(f"SELECT * FROM Sponsor_Data WHERE {t} LIKE '%{s}%'")

        if s != "":
            for d in data:
                database_tree.insert(parent= '', index=tkinter.END, values=(d[0],d[1],d[2],(f"{d[3]} {d[4]}"),d[5],d[6]))
        else:
            data = cursor.execute("SELECT * FROM Sponsor_Data")
            for d in data:
                database_tree.insert(parent= '', index=tkinter.END, values=(d[0],d[1],d[2],(f"{d[3]} {d[4]}"),d[5],d[6]))
    else:
        data = cursor.execute("SELECT * FROM Sponsor_Data")
        for d in data:
            database_tree.insert(parent= '', index=tkinter.END, values=(d[0],d[1],d[2],(f"{d[3]} {d[4]}"),d[5],d[6]))
        messagebox.showerror("Invalid Type","Unknown Search Type")
        
    connection.close()
##############################################################################

##############################################################################
#Function pulls up help screen with list of directions
def help():
    pass
##############################################################################

##############################################################################
points = 0
#Functions that sorts table by column
def sort_name():
    global points
    
    for d in database_tree.get_children():
        database_tree.delete(d)

    connection = sqlite3.connect('sponsors.db')
    cursor = connection.cursor()   

    if points == 0:
        data = cursor.execute(f"SELECT * FROM Sponsor_Data ORDER BY name")
    else:
        data = cursor.execute(f"SELECT * FROM Sponsor_Data ORDER BY name DESC")
    for d in data:
        database_tree.insert(parent= '', index=tkinter.END, values=(d[0],d[1],d[2],(f"{d[3]} {d[4]}"),d[5],d[6]))

    connection.close()
    points +=1
    if points > 1:
        points = 0

def sort_type():
    global points
    
    for d in database_tree.get_children():
        database_tree.delete(d)

    connection = sqlite3.connect('sponsors.db')
    cursor = connection.cursor()   

    if points == 0:
        data = cursor.execute(f"SELECT * FROM Sponsor_Data ORDER BY type")
    else:
        data = cursor.execute(f"SELECT * FROM Sponsor_Data ORDER BY type DESC")
    for d in data:
        database_tree.insert(parent= '', index=tkinter.END, values=(d[0],d[1],d[2],(f"{d[3]} {d[4]}"),d[5],d[6]))

    connection.close()
    points +=1
    if points > 1:
        points = 0

def sort_resources():
    global points
    
    for d in database_tree.get_children():
        database_tree.delete(d)

    connection = sqlite3.connect('sponsors.db')
    cursor = connection.cursor()   

    if points == 0:
        data = cursor.execute(f"SELECT * FROM Sponsor_Data ORDER BY resources")
    else:
        data = cursor.execute(f"SELECT * FROM Sponsor_Data ORDER BY resources DESC")
    for d in data:
        database_tree.insert(parent= '', index=tkinter.END, values=(d[0],d[1],d[2],(f"{d[3]} {d[4]}"),d[5],d[6]))

    connection.close()
    points +=1
    if points > 1:
        points = 0

def sort_contact():
    global points
    
    for d in database_tree.get_children():
        database_tree.delete(d)

    connection = sqlite3.connect('sponsors.db')
    cursor = connection.cursor()   

    if points == 0:
        data = cursor.execute(f"SELECT * FROM Sponsor_Data ORDER BY contact_first")
    else:
        data = cursor.execute(f"SELECT * FROM Sponsor_Data ORDER BY contact_first DESC")
    for d in data:
        database_tree.insert(parent= '', index=tkinter.END, values=(d[0],d[1],d[2],(f"{d[3]} {d[4]}"),d[5],d[6]))

    connection.close()
    points +=1
    if points > 1:
        points = 0

def sort_email():
    global points
    
    for d in database_tree.get_children():
        database_tree.delete(d)

    connection = sqlite3.connect('sponsors.db')
    cursor = connection.cursor()   

    if points == 0:
        data = cursor.execute(f"SELECT * FROM Sponsor_Data ORDER BY email")
    else:
        data = cursor.execute(f"SELECT * FROM Sponsor_Data ORDER BY email DESC")
    for d in data:
        database_tree.insert(parent= '', index=tkinter.END, values=(d[0],d[1],d[2],(f"{d[3]} {d[4]}"),d[5],d[6]))

    connection.close()
    points +=1
    if points > 1:
        points = 0

def sort_num():
    global points
    
    for d in database_tree.get_children():
        database_tree.delete(d)

    connection = sqlite3.connect('sponsors.db')
    cursor = connection.cursor()   

    if points == 0:
        data = cursor.execute(f"SELECT * FROM Sponsor_Data ORDER BY phone")
    else:
        data = cursor.execute(f"SELECT * FROM Sponsor_Data ORDER BY phone DESC")
    for d in data:
        database_tree.insert(parent= '', index=tkinter.END, values=(d[0],d[1],d[2],(f"{d[3]} {d[4]}"),d[5],d[6]))

    connection.close()
    points +=1
    if points > 1:
        points = 0

##############################################################################

#Entry Bar | GUI for entry form on the left   
##############################################################################
#Information frame
info_frame = tkinter.Frame(screen,width=300,height=900, bg='navy')
info_frame.place(x=0,y=0)

#Saving Info frame
sponsor_info_frame = tkinter.LabelFrame(info_frame, border=0, text="Sponsor Info",bg="navy",fg="gold")
sponsor_info_frame.grid(row=0,column=0)

#Saves sponsor name
sponsor_name_lbl = tkinter.Label(sponsor_info_frame, text='Sponsor Name',bg="navy",fg="gold")
sponsor_name_lbl.grid(row=0,column=0)
sponsor_name_entry = tkinter.Entry(sponsor_info_frame)
sponsor_name_entry.grid(row=1,column=0)

#Org type
type_org = ["", "Non-profit", "Other"]
sponsor_org_lbl = tkinter.Label(sponsor_info_frame, text='Type of organization',bg="navy",fg="gold")
sponsor_org_box = ttk.Combobox(sponsor_info_frame, values=type_org)
sponsor_org_lbl.grid(row=3,column=0)
sponsor_org_box.grid(row=4,column=0)

#Resources available
resources = ["", "Funding", "Food and Beverage", "Transportation", "Other"]
sponsor_resource_lbl = tkinter.Label(sponsor_info_frame, text='Resources available',bg="navy",fg="gold")
sponsor_resource_box = ttk.Combobox(sponsor_info_frame, values=resources)
sponsor_resource_lbl.grid(row=5,column=0)
sponsor_resource_box.grid(row=6,column=0)

for widget in sponsor_info_frame.winfo_children():
    widget.grid_configure(padx=10,pady=5)
##############################################################################

#Contacts
##############################################################################
    #Contact Info
    contact_frame = tkinter.LabelFrame(info_frame,border=0, text="Direct Contact Info",bg="navy",fg="gold")
    contact_frame.grid(row=1,column=0)

    #Contact  First name
    contact_lbl = tkinter.Label(contact_frame, text='Contact First Name',bg="navy",fg="gold")
    contact_lbl.grid(row=0,column=0)
    contact_first_entry = tkinter.Entry(contact_frame)
    contact_first_entry.grid(row=1,column=0)

    #Contact Last name
    contact_last_lbl = tkinter.Label(contact_frame, text='Contact Last Name',bg="navy",fg="gold")
    contact_last_lbl.grid(row=2,column=0)
    contact_last_entry = tkinter.Entry(contact_frame)
    contact_last_entry.grid(row=3,column=0)

    #Contact email
    email_lbl = tkinter.Label(contact_frame, text='Email',bg="navy",fg="gold")
    email_lbl.grid(row=4,column=0)
    email_entry = tkinter.Entry(contact_frame)
    email_entry.grid(row=5,column=0)

    #Contact number
    phone_lbl = tkinter.Label(contact_frame, text='Phone Number',bg="navy",fg="gold")
    phone_lbl.grid(row=6,column=0)
    phone_entry = tkinter.Entry(contact_frame)
    phone_entry.grid(row=7,column=0)

    for widget in contact_frame.winfo_children():
            widget.grid_configure(padx=10,pady=5)

    entry_btn = tkinter.Button(info_frame,text="Enter data", cursor='hand2',bg='#800000',fg='gold',command=data_entry)
    entry_btn.grid(row=3,column=0, sticky="news", padx=10,pady=10)
##############################################################################


#Buttons
##############################################################################
    action_frame = tkinter.Frame(screen, width=837,height=55,bg='white')
    action_frame.place(x=163,y=0)

    #Search box
    search_box = tkinter.Entry(action_frame,width=25,fg='black',border=2.5, bg='white')
    search_box.place(x=1 , y=25)

    search_btn = tkinter.Button(action_frame, text='Search',width=10,border=3,cursor='hand2',bg='#800000',fg='gold', command=search)
    search_btn.place(x=160,y=10)

    search_by = ttk.Combobox(action_frame,width=22, values=['Name','Type', 'Resources','Contact','Email','Phone'])
    search_by.place(x=3 , y=1)

    edit_btn = tkinter.Button(action_frame,pady = 5, text='Edit Sponsor',border=3,cursor='hand2',bg='#800000',fg='gold', command=edit)
    edit_btn.place(x=545,y=10)

    remove_btn = tkinter.Button(action_frame,pady = 5, text='Remove Sponsor',border=3,cursor='hand2',bg='#800000',fg='gold', command=delete_item)
    remove_btn.place(x=630,y=10)

    exit_btn = tkinter.Button(action_frame,width=10, pady = 5, text='Exit',border=3,cursor='hand2',bg='#800000',fg='gold',command=quit)
    exit_btn.place(x=737,y=10)


    tkinter.Frame(action_frame, width=837,height=2,bg='gold').place(x=0,y=50)
##############################################################################

#Datebase | GUI for table with all sponsors
##############################################################################
connection = sqlite3.connect('sponsors.db')
cursor = connection.cursor()   
data = cursor.execute("SELECT * FROM Sponsor_Data")


database_frame = tkinter.Frame(screen, width=1000,height=400,bg='white')
database_frame.place(x=163,y=60)

help_btn = tkinter.Button(screen,width=10, pady = 5, text='Help ?',border=3,cursor='hand2',bg='#800000',fg='gold',command=help)
help_btn.place(x=893,y=400)

#Tree
database_tree = ttk.Treeview(database_frame, selectmode='browse',columns= ('Name','Type', 'Resources','Contact','Email','Phone'), show='headings')
database_tree.heading('Name', text='Name',command=sort_name)
database_tree.heading('Type', text='Type',command=sort_type)
database_tree.heading('Resources', text='Resources',command=sort_resources)
database_tree.heading('Contact', text='Contact',command=sort_contact)
database_tree.heading('Email', text='Email',command=sort_email)
database_tree.heading('Phone', text='Phone',command=sort_num)

database_tree.column('Name',width=100)
database_tree.column('Type', width=100)
database_tree.column('Resources', width=100)
database_tree.column('Contact', width=100)

database_tree.pack(padx=10)


for d in data:
    num = str(d[6])
    print(num)
    database_tree.insert(parent= '', index=tkinter.END, values=(d[0],d[1],d[2],(f"{d[3]} {d[4]}"),d[5],(f"({num[0:3]})-{num[3:6]}-{num[6:10]}")))
    

#database_tree.bind('<<TreeviewSelect>>',item_select)

connection.close()

screen.mainloop() 