import tkinter, random, ast, sqlite3
from tkinter import messagebox
from tkinter import ttk





#Window Settings
root = tkinter.Tk()
root.title("Login")
root.geometry('925x500+300+200')
root.configure(bg="white")
root.resizable(False,False)
photo = tkinter.PhotoImage(file = "fbla_logo.png")
root.iconphoto(False, photo)

#Functions
def signin():
    username = user.get()
    password = code.get()

    file = open('login_info.txt','r')
    d = file.read()
    r = ast.literal_eval(d)
    file.close()

    # print(r.keys())
    # print(r.values())

    if username in r.keys() and password==r[username]:

        screen= tkinter.Toplevel(root)
        screen.title("App")
        screen.geometry('925x500+300+200')
        screen.configure(bg="white")

        tkinter.Label(screen,text='Hello World',bg='white',font=('Microsoft YaHei UI Light', 23,'bold')).pack(expand=True)


        screen.mainloop()
    else: 
        messagebox.showerror("Invalid", "Invalid username or password")

####################################################################################################################################################################
def sign_up():
    print("Hello")
################################################################################################################################








#Startup page image
img = tkinter.PhotoImage(file='login_icon.png')
tkinter.Label(root, image=img, bg='white').place(x=50,y=75)

#Frames
#Login frame is used to place all objects needed
login_frame = tkinter.Frame(root, width=350,height=350,bg='white')
login_frame.place(x=480,y=70)
        
#Sign in Text
heading = tkinter.Label(login_frame , text='Sign in', fg='#800000',bg='white',font=('Microsoft YaHei UI Light', 23,'bold'))
heading.place(x=100,y=5)

#Textbox to enter username
def on_enter(e):
    name = user.get()
    if name == "Username":
        user.delete(0,'end')
    
def on_leave(e):
    name=user.get()
    if name=='':
        user.insert(0, "Username")

user = tkinter.Entry(login_frame,width=25,fg='black',border=0,bg='white',font=('Microsoft YaHei UI Light', 11))
user.place(x=30,y=80)
user.insert(0, "Username")
user.bind('<FocusIn>',on_enter)
user.bind('<FocusOut>',on_leave)

tkinter.Frame(login_frame, width=295,height=2,bg='black').place(x=25,y=107)

#Textboxt to enter password
def on_enter(e):
    password = code.get()
    if password == "Password":
        code.delete(0,'end')
    
def on_leave(e):
    password = code.get()
    if code=='':
        code.insert(0, "Password")

code = tkinter.Entry(login_frame,width=25,fg='black',border=0, bg='white',font=('Microsoft YaHei UI Light', 11))
code.place(x=30,y=150)
code.insert(0, "Password")
code.bind('<FocusIn>',on_enter)
code.bind('<FocusOut>',on_leave)

tkinter.Frame(login_frame, width=295,height=2,bg='black').place(x=25,y=177)

#Sign in button
tkinter.Button(login_frame,width=39,pady=7,text='Sign in',bg='#800000',cursor='hand2', fg='white',border=0, command=signin).place(x=35,y=204)

need_to_register = tkinter.Label(login_frame, text="Don't have an account?", fg='black',bg='white',font=('Microsoft YaHei UI Light', 9))
need_to_register.place(x=75,y=270)

register_btn = tkinter.Button(login_frame,width=6,text='Sign up',border=0,cursor='hand2',bg='white',fg='#57a1f8',command=sign_up)
register_btn.place(x=215,y=270)

root.mainloop()
    