import tkinter, random, ast, sqlite3
from tkinter import messagebox
from tkinter import ttk

    
window = tkinter.Tk()
window.title("Sign up")
window.geometry('925x500+300+200')
window.configure(bg="white")
photo = tkinter.PhotoImage(file = "fbla_logo.png")
window.iconphoto(False, photo)
window.resizable(False,False)

#Functions
def signup():
    username = user.get()
    password = code.get()
    confirm_password = confirm_code.get()
        
    if password == confirm_password:
        try:
            file = open('login_info.txt','r+')
            d = file.read()
            r = ast.literal_eval(d)
                
            dict2 = {username:password}
            r.update(dict2)
            file.truncate(0)
            file.close()

            file = open('login_info.txt','w')
            w = file.write(str(r))
            messagebox.showinfo('Signup','Sucessful Sign up')

            window.destroy()

        except:
            file = open('login_info.txt','w')
            pp = str({'Username':'password'})
            file.write(pp)
            file.close
    else:
        messagebox.showerror('Invalid', "Both Passwords should match")

def sign_in():
    window.destroy()

#Sign up page image
img = tkinter.PhotoImage(file='login_icon.png')
tkinter.Label(window, image=img, bg='white').place(x=50,y=75)

#Frames
#Login frame is used to place all objects needed
sign_up_frame = tkinter.Frame(window, width=350,height=370,bg='white')
sign_up_frame.place(x=480,y=50)
            
#Sign in Text
heading = tkinter.Label(sign_up_frame , text='Sign Up', fg='#800000',bg='white',font=('Microsoft YaHei UI Light', 23,'bold'))
heading.place(x=30,y=5)

#Textbox to enter username
def on_enter(e):
    if user.get() == "Username":
        user.delete(0,'end')
        
def on_leave(e):
    if user.get()=='':
        user.insert(0, "Username")

user = tkinter.Entry(sign_up_frame,width=25,fg='black',border=0,bg='white',font=('Microsoft YaHei UI Light', 11))
user.place(x=30,y=80)
user.insert(0, "Username")
user.bind('<FocusIn>',on_enter)
user.bind('<FocusOut>',on_leave)

tkinter.Frame(sign_up_frame, width=295,height=2,bg='black').place(x=25,y=107)

#Textboxt to enter password
def on_enter(e):
    if code.get() == "Password":
        code.delete(0,'end')
        
def on_leave(e):
    if code.get()=='':
        code.insert(0, "Password")

code = tkinter.Entry(sign_up_frame,width=25,fg='black',border=0, bg='white',font=('Microsoft YaHei UI Light', 11))
code.place(x=30,y=150)
code.insert(0, "Password")
code.bind('<FocusIn>',on_enter)
code.bind('<FocusOut>',on_leave)

tkinter.Frame(sign_up_frame, width=295,height=2,bg='black').place(x=25,y=177)

#Confirmation of Password Textbox
def on_enter(e):
    if confirm_code.get() == "Confirm":
        confirm_code.delete(0,'end')
        
def on_leave(e):
    if confirm_code.get()=='':
        confirm_code.insert(0, "Confirm")

confirm_code = tkinter.Entry(sign_up_frame,width=25,fg='black',border=0, bg='white',font=('Microsoft YaHei UI Light', 11))
confirm_code.place(x=30,y=220)
confirm_code.insert(0, "Confirm")
confirm_code.bind('<FocusIn>',on_enter)
confirm_code.bind('<FocusOut>',on_leave)

tkinter.Frame(sign_up_frame, width=295,height=2,bg='black').place(x=25,y=247)

#Sign in button
tkinter.Button(sign_up_frame,width=39,pady=7,text='Sign Up',bg='#800000',cursor='hand2', fg='white',border=0, command=signup).place(x=35,y=280)

need_to_register = tkinter.Label(sign_up_frame, text="I have an account", fg='black',bg='white',font=('Microsoft YaHei UI Light', 9))
need_to_register.place(x=75,y=340)

register_btn = tkinter.Button(sign_up_frame,width=6,text='Sign in',border=0,cursor='hand2',bg='white',fg='#57a1f8', command=sign_in)
register_btn.place(x=215,y=340)


window.mainloop()
