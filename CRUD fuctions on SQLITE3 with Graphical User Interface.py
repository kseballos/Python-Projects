from tkinter import *
from PIL import ImageTk,Image
import sqlite3

root=Tk()
root.title('Message box')
root.iconbitmap('circle-cropped.ico')
#root.geometry("350x400")

#Databases

#connectDB
conn = sqlite3.connect('address_book.db')
#create cursor
c = conn.cursor()

#create table
'''
c.execute("""CREATE TABLE addresses (
        first_name text,
        last_name text,
        address text,
        city text,
        state text,
        zipcode integer)""")
    
c.execute("DELETE FROM addresses")
'''
frameinput=LabelFrame(root,text="Fill in the following Textboxes")
frameinput.grid(row=0,column=0)
#create submit function
def submit():
    #connectDB
    conn = sqlite3.connect('address_book.db')
    #create cursor
    c = conn.cursor()
    #insert into table
 
    if len(fname.get()) == 0 or len(lname.get()) == 0 or len(address.get())== 0 or len(city.get())== 0 or len(state.get())== 0 or len(zipcode.get()) == 0:
        emptyfieldlbl = Label(frameinput, text="Make sure you did not skip any fields",justify=LEFT,fg="red")
        emptyfieldlbl.grid(row=6, column=0,columnspan=2, sticky=W)
        print(fname.get(),lname.get(),address.get(),city.get(),state.get(), zipcode.get())
    else:
        c.execute("INSERT INTO addresses VALUES(:fname,:lname, :address, :city, :state, :zipcode)",
                {
                    'fname':fname.get(),
                    'lname':lname.get(),
                    'address':address.get(),
                    'city':city.get(),
                    'state':state.get(),
                    'zipcode':zipcode.get()
                }
            )
            
    #commit changes and close
    conn.commit()
    conn.close()
    
    #clear textboxes
    fname.delete(0,END)
    lname.delete(0,END)
    address.delete(0,END)
    city.delete(0,END)
    state.delete(0,END)
    zipcode.delete(0,END)
swtch=0      
def query():
    #connectDB
    conn = sqlite3.connect('address_book.db')
    #create cursor
    c = conn.cursor()
    #insert into table
    c.execute("SELECT *,oid FROM addresses")
    records=c.fetchall()
    #print(records)
    #loop through results
    global framedata
    framedata = LabelFrame(root,text="This is your data")
    framedata.grid(row=1,column=0,pady=0)   
    fullname=''
    address_lbl=''
    ID_lbl=''
    zipcode_lbl=''
    tbl_fname = Label(framedata, text="Fullname")
    tbl_fname.grid(row=0,column=3, sticky=W)
    tbl_address = Label(framedata, text="Address")
    tbl_address.grid(row=0,column=4, sticky=W)
    tbl_ID = Label(framedata, text="ID")
    tbl_ID.grid(row=0,column=2, sticky=W)
    tbl_zipcode=Label(framedata, text ="Zipcode")
    tbl_zipcode.grid(row=0, column=5, sticky=W)
    for record in records:
        fullname += str(record[0])+" "+str(record[1])+"\n"
        ID_lbl += str(record[6]) +"\n"
        address_lbl += str(record[2]) +"\n" 
        zipcode_lbl += str(record[5])+"\n"
    query_fname= Label(framedata, text=fullname, justify=LEFT)
    query_fname.grid(row=1,column=3,sticky=W)
    query_ID = Label(framedata, text=ID_lbl,justify=LEFT)
    query_ID.grid(row=1,column=2,sticky=W)
    query_address = Label(framedata, text=address_lbl,justify=LEFT)
    query_address.grid(row=1,column=4,sticky=W)
    query_zipcode = Label(framedata, text=zipcode_lbl,justify=LEFT)
    query_zipcode.grid(row=1,column=5,sticky=W)
    #commit changes and close
    conn.commit()
    conn.close()

def delete():
    if len(deleteinput.get()) == 0 :
        emptyfieldlbl = Label(root, text="Please enter an ID",justify=LEFT,fg="red")
        emptyfieldlbl.grid(row=11, column=0,columnspan=2, sticky=W)
    else:
        conn = sqlite3.connect('address_book.db')
        #create cursor
        c = conn.cursor()
        #insert into table
        c.execute("DELETE FROM addresses WHERE oid ="+deleteinput.get())
        del_item = Label(frameinput, text="Item with ID: " + str(deleteinput.get())+"is deleted", justify=LEFT)
        del_item.grid(row=10,column=0,sticky=W)
        deleteinput.delete(0,END)
        del_item.grid_forget()
        framedata.destroy()
        #commit changes and close
        conn.commit()
        conn.close()
    
def edit():
    fullname=''
    address_lbl=''
    ID_lbl=''
    emptyfieldlbl=''
    global fname_editor
    global lname_editor
    global address_editor
    global city_editor
    global state_editor
    global zipcode_editor
    global updatewin
    if len(deleteinput.get()) == 0 :
        emptyfieldlbl = Label(root, text="Please enter an ID",justify=LEFT,fg="red")
        emptyfieldlbl.grid(row=11, column=0,columnspan=2, sticky=W)
    else:    
        conn = sqlite3.connect('address_book.db')
        #create cursor
        c = conn.cursor()
        record_id = deleteinput.get()
        #insert into table
        c.execute("SELECT *, oid FROM addresses WHERE oid ="+record_id)
        records=c.fetchall()
        for record in records:
            fullname += str(record[0])+" "+str(record[1])+"\n"
        #loop thru results
        updatewin=Toplevel()
        updatewin.title("Update Record of " +fullname.upper())
        updatewin.iconbitmap('circle-cropped.ico')
        frameinput=LabelFrame(updatewin,text="You can now edit the information")
        frameinput.grid(row=0,column=0)
        #create textboxes

        fname_editor=Entry(frameinput, width=30)
        fname_editor.grid(row=0,column=1)
        lname_editor=Entry(frameinput, width=30)
        lname_editor.grid(row=1,column=1)
        address_editor=Entry(frameinput, width=30)
        address_editor.grid(row=2,column=1)
        city_editor=Entry(frameinput, width=30)
        city_editor.grid(row=3,column=1)
        state_editor=Entry(frameinput, width=30)
        state_editor.grid(row=4,column=1)
        zipcode_editor=Entry(frameinput, width=30)
        zipcode_editor.grid(row=5,column=1)

        #create textboxes label
        fnamelbl_editor=Label(frameinput, text="First name:")
        fnamelbl_editor.grid(row=0,column=0)
        lnamelbl_editor=Label(frameinput, text="Last name:")
        lnamelbl_editor.grid(row=1,column=0)
        addresslbl_editor=Label(frameinput, text="Address:")
        addresslbl_editor.grid(row=2,column=0)
        citylbl_editor=Label(frameinput, text="City:")
        citylbl_editor.grid(row=3,column=0)
        statelbl_editor=Label(frameinput, text="State:")
        statelbl_editor.grid(row=4,column=0)
        zipcodelbl_editor=Label(frameinput, text="Zipcode:")
        zipcodelbl_editor.grid(row=5,column=0)

        for record in records:
            fname_editor.insert(0,record[0])
            lname_editor.insert(0,record[1])
            address_editor.insert(0,record[2])
            city_editor.insert(0,record[3])
            state_editor.insert(0,record[4])
            zipcode_editor.insert(0,record[5])
        

        #create button for submit
        submitbtn_editor=Button(frameinput, text="Update Information", command=update)
        submitbtn_editor.grid(row=7, column=0, columnspan=2,padx=10,pady=10,ipadx=90)
    

def update():
    #connectDB
    conn = sqlite3.connect('address_book.db')
    #create cursor
    c = conn.cursor()
    #insert into table
    record_id = deleteinput.get()
    c.execute("""UPDATE addresses SET 
                    first_name=:fname,
                    last_name=:lname,
                    address=:address,
                    city=:city,
                    state=:state,
                    zipcode=:zipcode
                    
                    WHERE oid = :oid""",
              {'fname':fname_editor.get(),
               'lname':lname_editor.get(),
               'address':address_editor.get(),
               'city':city_editor.get(),
               'state':state_editor.get(),
               'zipcode':zipcode_editor.get(),

               'oid':record_id
                }
            )
    #commit changes and close
    conn.commit()
    conn.close()
    updatewin.destroy()
    framedata.destroy()

#create textboxes

fname=Entry(frameinput, width=30)
fname.grid(row=0,column=1)
lname=Entry(frameinput, width=30)
lname.grid(row=1,column=1)
address=Entry(frameinput, width=30)
address.grid(row=2,column=1)
city=Entry(frameinput, width=30)
city.grid(row=3,column=1)
state=Entry(frameinput, width=30)
state.grid(row=4,column=1)
zipcode=Entry(frameinput, width=30)
zipcode.grid(row=5,column=1)

#create textboxes label
fnamelbl=Label(frameinput, text="First name:")
fnamelbl.grid(row=0,column=0)
lnamelbl=Label(frameinput, text="Last name:")
lnamelbl.grid(row=1,column=0)
addresslbl=Label(frameinput, text="Address:")
addresslbl.grid(row=2,column=0)
citylbl=Label(frameinput, text="City:")
citylbl.grid(row=3,column=0)
statelbl=Label(frameinput, text="State:")
statelbl.grid(row=4,column=0)
zipcodelbl=Label(frameinput, text="Zipcode:")

zipcodelbl.grid(row=5,column=0)

#create button for submit
submitbtn=Button(frameinput, text="Submit Information", command=submit)
submitbtn.grid(row=7, column=0, columnspan=2,padx=10,pady=10,ipadx=90)

#deletelabel
deletelabel=Label(frameinput, text="Input ID: ")
deletelabel.grid(row=9,column=0)
deleteinput=Entry(frameinput, width=30)
deleteinput.grid(row=9,column=1,padx=10,pady=10)
#delete button query
deletebtn = Button(frameinput, text="Delete Record", command=delete)
deletebtn.grid(row=10,column=0,ipadx=25, pady=10, sticky=W)

#update button
updatebtn = Button(frameinput, text="Edit Record", command=edit)
updatebtn.grid(row=10,column=1,ipadx=25, pady=10,sticky=E)

#button query
querybtn = Button(frameinput, text="Retrieve Data", command=query)
querybtn.grid(row=8, column=0, columnspan=2,pady=10,ipadx=108)
    
#commit changes
conn.commit()

#close connection
conn.close()
root.mainloop()
