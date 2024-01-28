from contactbook import ContactBook

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox 

cb = ContactBook() # Instance for contactBk class

class ContactApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        # Set up the main window
        tk.Tk.wm_title(self, "My Contact Book")
        
        # Create a container to hold frames
        container = tk.Frame(self)
        container.pack(side="top",padx="20px",pady="20px",fill="both", expand=True)
        
        # Configure the container
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        # Create a dictionary to store frames
        self.frames = {}
        
        # Add frames to the dictionary
        for F in (LoginPage,HomePage,ManageContactPage,ChangePasswordPage,AddContactPage,UpdateContactPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # Show the start page initially
        self.show_frame(LoginPage)

    def show_frame(self, cont):
        # Raise the selected frame to the front
        frame = self.frames[cont]
        frame.tkraise()


    def destroy_and_reopen(self):
        # Destroy the current Tkinter window
        self.destroy()

        # Create a new Tkinter window
        new_app = ContactApp()
        new_app.geometry("900x700")  # Set the initial window size
        new_app.mainloop()

    

# Login page
class LoginPage(tk.Frame):
    is_login = False
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text="LOGIN")
        label.pack(pady=10, padx=10)
       
        user = tk.StringVar()
        pas = tk.StringVar()
        
        input_label = tk.Label(self,text="username:").pack()
        self.username_input = tk.Entry(self,textvariable=user)
        self.username_input.pack()
        self.username_input.focus()
        

        password_label = tk.Label(self,text="password:").pack()
        self.password_input = tk.Entry(self,textvariable=pas)
        self.password_input.pack()
       
        button = tk.Button(self,text="Login",command=lambda:[self.login(controller,user.get(),pas.get())])
        button.pack()

    def login(self,controller,username,password):
        if cb.login(username,password) == True:
            controller.show_frame(HomePage)
            self.is_login = True
            self.username_input.delete(0, "end")
            self.password_input.delete(0, "end")
            self.username_input.focus()
            LoginPage.is_login=True

            manage_contact_page_instance = controller.frames[ManageContactPage]
            manage_contact_page_instance.details()
        else:
            messagebox.showerror(message="your login credentials are worng")
            LoginPage.is_login=False

# Home page
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text="HOME")
        label.pack(pady=0.1, padx=0.1)

        button = tk.Button(self, text="Logout",command=lambda:[controller.destroy_and_reopen(),controller.show_frame(LoginPage)])
        button.place(y=15)

        button = tk.Button(self, text="Change Passsword",command=lambda: controller.show_frame(ChangePasswordPage))
        button.place(y=45)

        button2 = tk.Button(self, text="Manage Contacts", command=lambda: [controller.show_frame(ManageContactPage),messagebox.showinfo(message="Select a Contact Before Edit")])
        button2.place(y=75)

        button2 = tk.Button(self, text="Add Contact", command=lambda: controller.show_frame(AddContactPage))
        button2.place(x=700,y=75)


# #Page to Change Password
class ChangePasswordPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) 

        Homebutton = tk.Button(self, text='Home',command=lambda:controller.show_frame(HomePage))
        Homebutton.place(x=500,y=5)

        old_pass = tk.StringVar()
        new_pass = tk.StringVar()
        
        old_label = tk.Label(self, text="Old Password")
        old_label.pack()

        self.old_entry = tk.Entry(self,textvariable=old_pass)
        self.old_entry.pack()

        new_label = ttk.Label(self, text="New Password")
        new_label.pack()

        self.new_entry = tk.Entry(self,textvariable=new_pass)
        self.new_entry.pack()

        Changepassbutton = tk.Button(self,text="Change Password",command=lambda:self.change(old_pass.get(),new_pass.get(),controller)).pack()
    
    def change(self,old_passoword,new_passowrd,controller):
        if cb.change_password(old_passoword,new_passowrd) == True:
            messagebox.showinfo(message="Password changed successfully")
            controller.show_frame(HomePage)
            self.old_entry.delete(0, "end")
            self.new_entry.delete(0, "end")
        else:
            messagebox.showerror(message="your old password is wrong")
    

# Page to create new Contact
class AddContactPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Add Contacts")
        label.pack(pady=10, padx=10)

        Homebutton = tk.Button(self, text='Home',command=lambda:controller.show_frame(HomePage))
        Homebutton.place(x=500,y=5)

        self.username = tk.StringVar()
        self.phoneno = tk.StringVar()
        self.email = tk.StringVar()
        self.city = tk.StringVar()

        label_username= tk.Label(self,text="username").pack()
        self.username_entry = tk.Entry(self,textvariable=self.username)
        self.username_entry.pack()

        label_phoneno = tk.Label(self,text="Phone Number").pack()
        self.phone_entry = tk.Entry(self,textvariable=self.phoneno)
        self.phone_entry.pack()

        label_email = tk.Label(self,text="Email").pack()
        self.email_entry = tk.Entry(self,textvariable=self.email)
        self.email_entry.pack()
        
        label_city = tk.Label(self,text="City").pack()
        self.city_entry = tk.Entry(self,textvariable=self.city)
        self.city_entry.pack()

        button = tk.Button(self,text="Add",command=lambda:self.Add(controller)).pack()

    def Add(self,controller):
       if cb.add_contacts(self.username.get(),self.phoneno.get(),self.email.get(),self.city.get()) == True:
           messagebox.showinfo(message="Contacts Added")
           controller.show_frame(HomePage)
           self.username_entry.delete(0,"end")
           self.phone_entry.delete(0,"end")
           self.email_entry.delete(0,"end")
           self.city_entry.delete(0,"end")
           self.username_entry.focus_set()
       else:
            messagebox.showinfo(message="Error")
        


#Page to update Contact
class UpdateContactPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Update Contacts")
        label.pack(pady=10, padx=10)

        button = tk.Button(self, text='Back',command=lambda:controller.show_frame(ManageContactPage))
        button.place(x=100,y=10)

        Homebutton = tk.Button(self, text='Home',command=lambda:controller.show_frame(HomePage))
        Homebutton.place(x=500,y=5)
        
        self.id=0
        self.name=0
        self.number=0
        self.email=0
        self.city=0


        self.id = tk.StringVar()
        self.username = tk.StringVar()
        self.phoneno = tk.StringVar()
        self.emailv = tk.StringVar()
        self.cityv = tk.StringVar()
        self.contact_id = tk.StringVar()
        

        controller = self.winfo_toplevel()
        Manage_obj = controller.frames[ManageContactPage]

        label_username= tk.Label(self,text="username").pack()
        self.username_entry = tk.Entry(self,textvariable=self.username)
        self.username_entry.pack()
       
        label_phoneno = tk.Label(self,text="Phone Number").pack()
        self.phone_entry = tk.Entry(self,textvariable=self.phoneno)
        self.phone_entry.pack()


        label_email = tk.Label(self,text="Email").pack()
        self.email_entry = tk.Entry(self,textvariable=self.emailv)
        self.email_entry.pack()
        
        
        label_city = tk.Label(self,text="City").pack()
        self.city_entry = tk.Entry(self,textvariable=self.cityv)
        self.city_entry.pack()

        button = tk.Button(self,text="Update",command=lambda:[self.execute_update(),controller.show_frame(ManageContactPage)]).pack()
        button = tk.Button(self, text='Delete',background="Red",command=lambda:[self.execute_delete(),controller.show_frame(ManageContactPage)]).pack()
        

    def execute_update(self):
       if cb.update_contacts(self.id.get(),self.username.get(),self.phoneno.get(),self.emailv.get(),self.cityv.get(),self.contact_id.get()):
           messagebox.showinfo(message="Contact Updated")
    
    def execute_delete(self):
        if cb.delete_contacts(self.contact_id.get(),self.id.get()):
            messagebox.showinfo(message="Contact Removed")
    
    def update_values(self,id,name,phone,email,city,contactid):
        
        self.id.set(id)
        self.username.set(name)
        self.phoneno.set(phone)
        self.emailv.set(email)
        self.cityv.set(city)
        self.contact_id.set(contactid)



        


# Page to Manage Contacts
class ManageContactPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Manage Contacts")
        label.pack(pady=10, padx=10)

        self.id=0
        self.name=0
        self.number=0
        self.email=0
        self.city=0
        self.contactid=0
       
        Homebutton = tk.Button(self, text='Home',command=lambda:controller.show_frame(HomePage))
        Homebutton.place(x=500,y=5)
        
        button = tk.Button(self, text='Edit',command=lambda:[controller.show_frame(UpdateContactPage)])
        button.place(x=700,y=10)
        
        self.contact_details =[]
    
    def details(self):
        self.treeview = ttk.Treeview(self)
        self.treeview["columns"] = ("Id","Name", "PhoneNumber","Email","City")
        self.treeview.heading("Id",text="Id")
        self.treeview.heading("Name", text="Name")
        self.treeview.heading("PhoneNumber", text="Phone")
        self.treeview.heading("Email",text="Email")
        self.treeview.heading("City",text="City")
       
        self.treeview.bind("<ButtonRelease-1>", self.on_tree_select)
        
        contact_detail = cb.manage_contacts()
        for contact_tuple in contact_detail:
            self.treeview.insert("","end",values=contact_tuple)

        scrollbar_vertical = ttk.Scrollbar(self, orient="vertical", command=self.treeview.yview)
        scrollbar_vertical.pack(side="right", fill="y")
        scrollbar_horizontal = ttk.Scrollbar(self, orient="horizontal", command=self.treeview.xview)
        scrollbar_horizontal.pack(side="bottom", fill="x")
    
        self.treeview.pack(expand=True, fill="both")
    
    def on_tree_select(self,event):
        # Get the selected item
        selected_item =self.treeview.selection()
        if selected_item:
            item_values = self.treeview.item(selected_item)['values']
            self.id = item_values[0]
            self.name = item_values[1]
            self.number = item_values[2]
            self.email = item_values[3]
            self.city = item_values[4]
            self.contactid = item_values[5]

            controller = self.winfo_toplevel()
            update_object = controller.frames[UpdateContactPage]
            update_object.update_values(self.id,self.name,self.number,self.email,self.city,self.contactid)

        
        
        

# Run the application
if __name__ == "__main__":
    app = ContactApp()
    app.geometry("900x700")
    app.mainloop()
