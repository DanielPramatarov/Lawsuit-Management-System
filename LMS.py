from tkinter import *
import sqlite3
import tkinter.ttk as ttk
from tkinter import messagebox
from datetime import datetime
from datetime import date
import re

root = Tk()

def showInfo():
	info = Toplevel(root) 
	info.title("Data") 
	info.geometry("600x600")
	info.grab_set() 
	Fact = """
	[+]The date must be in this format DD-MM-YYYY
 	[+]ID can not be change 
	
	"""
	T = Text(info, height = 20, width = 70,) 
	
	l = Label(info, text = "Information for using the program", justify=LEFT) 
	l.config(font =("Courier", 14)) 
	

	b2 = Button(info, text = "Exit", 
				command = info.destroy)  
	T.tag_configure("left", justify='center')
	T.insert(END,Fact)

	l.pack() 
	T.pack() 
	b2.pack() 


root.title('Lawsuite Database')
root.geometry("430x600")


menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="info", command=showInfo)


filemenu.add_separator()

menubar.add_cascade(label="Help", menu=filemenu)
editmenu = Menu(menubar, tearoff=0)


root.config(menu=menubar)
conn = sqlite3.connect('lawsuits.db')

c = conn.cursor()


try:
    c.execute("""CREATE TABLE lawsuits (
                id VARCHAR(20) PRIMARY KEY ,
                prosecutors_office VARCHAR(100) ,
                name_prosecutor VARCHAR(60) ,
                article VARCHAR(30) ,
                date DATE ,
                notes MEDIUMTEXT,
                sended_to VARCHAR(90),
                sended_cartons BOOLEAN
                )""")
except:
    pass

def update():
	conn = sqlite3.connect('lawsuits.db')
	c = conn.cursor()

	record_id = delete_box.get()
	delete_btn = delete_box.get()
	if len(delete_btn) == 0:
		messagebox.showerror ('Empty ID field','Edit ID option can not be empty',icon = 'warning')
	else:
		MsgBox = messagebox.askquestion ('Delete Lawsuite','Are you sure you want to update this lawsuite',icon = 'warning')
		if MsgBox == 'yes':

			try:
				c.execute("""UPDATE lawsuits SET
				id = :lawsuit_id_editor,
				prosecutors_office = :prosecutors_office_editor,
				name_prosecutor = :name_prosecutor,
				article = :article,
				date = :date,
				notes = :notes,
				sended_to = :sended_to ,
				sended_cartons = :send_cartons

				WHERE id = :lawsuit_id_editor""",
				{
				'lawsuit_id_editor': lawsuit_id_editor.get(),
				'prosecutors_office_editor': prosecutors_office_editor.get(),
				'name_prosecutor': name_prosecutor_editor.get(),
				'article': article_editor.get(),
				'date': Date_editor.get(),
				'notes': note_editor.get(),
				'sended_to': send_with_opinion_editor.get(),
				'send_cartons': Sended_Cartons_label_editor.get(),

				})
			except Exception as ex:
				print(str(ex))
			delete_box.delete(0, END)
		else:
			pass

	conn.commit()

	conn.close()

	editor.destroy()
	root.deiconify()


def close():
	editor.destroy()
	root.deiconify()
	delete_box.delete(0,END)
def edit():

	conn = sqlite3.connect('lawsuits.db')
	c = conn.cursor()

	record_id = delete_box.get()
	delete_btn = delete_box.get()
	if len(delete_btn) == 0:
		messagebox.showerror ('Empty ID field','Edit ID option can not be empty',icon = 'warning')
		
	if len(delete_btn) > 0:
		root.withdraw()
		global editor
		editor = Tk()
		editor.title('Update A Lawsuite')
		editor.geometry("450x300")
		c.execute("SELECT * FROM lawsuits WHERE id = " + record_id)
		records = c.fetchall()
		
		global lawsuit_id_editor
		global prosecutors_office_editor
		global name_prosecutor_editor
		global article_editor
		global note_editor
		global send_with_opinion_editor

		global Sended_Cartons_label_editor
		global Date_editor


		lawsuit_id_editor = Entry(editor, width=30)
		prosecutors_office_editor = Entry(editor, width=30)
		prosecutors_office_editor.grid(row=1, column=1)
		name_prosecutor_editor = Entry(editor, width=30)
		name_prosecutor_editor.grid(row=2, column=1)
		article_editor = Entry(editor, width=30)
		article_editor.grid(row=3, column=1)
		note_editor = Entry(editor, width=30)
		note_editor.grid(row=4, column=1)
		send_with_opinion_editor = Entry(editor, width=30)
		send_with_opinion_editor.grid(row=5, column=1)


		Sended_Cartons_label_editor = Entry(editor, width=30)
		Sended_Cartons_label_editor.grid(row=6, column=1)

		Date_editor = Entry(editor, width=30)
		Date_editor.grid(row=7, column=1)
		
		lawsuit_id_label = Label(editor, text="ID")
		prosecutors_office_label = Label(editor, text="Prosecutor's office")
		prosecutors_office_label.grid(row=1, column=0)
		name_prosecutor_label = Label(editor, text="Prosecutor's name")
		name_prosecutor_label.grid(row=2, column=0)
		article_label = Label(editor, text="article")
		article_label.grid(row=3, column=0)
		note_label = Label(editor, text="note")
		note_label.grid(row=4, column=0)
		send_with_opinion_label = Label(editor, text="send TO")
		send_with_opinion_label.grid(row=5, column=0)


		Sended_Cartons_label_editor_label = Label(editor, text="sended cartons")
		Sended_Cartons_label_editor_label.grid(row=6, column=0)
		Date_editor_label = Label(editor, text="Date")
		Date_editor_label.grid(row=7, column=0)
		for record in records:
			lawsuit_id_editor.insert(0, record[0])
			prosecutors_office_editor.insert(0, record[1])
			name_prosecutor_editor.insert(0, record[2])
			article_editor.insert(0, record[3])
			Date_editor.insert(0, record[4])
			send_with_opinion_editor.insert(0, record[5])
			Sended_Cartons_label_editor.insert(0, record[6])
			note_editor.insert(0, record[7])

		

			
		edit_btn = Button(editor, text="Save Record", command=update,bg='green')
		edit_btn.grid(row=8, column=0, columnspan=2, pady=10, padx=10, ipadx=145)
		exit_button = Button(editor, text="Exit", command=close,bg='red') 
		exit_button.grid(row=9, column=0, columnspan=2, pady=10, padx=10, ipadx=110)



def delete():
	conn = sqlite3.connect('lawsuits.db')
	c = conn.cursor()

	delete_btn = delete_box.get()
	if len(delete_btn) == 0:
		messagebox.showerror ('Empty ID field','Edid/Delete ID option can not be empty',icon = 'warning')
	else:
		MsgBox = messagebox.askquestion ('Delete Lawsuite','Are you sure you want to delete lawsuite',icon = 'warning')
		if MsgBox == 'yes':
			c.execute("DELETE from lawsuits WHERE id = :id",{'id': delete_box.get()})

			delete_box.delete(0, END)
		else:
			delete_box.delete(0, END)



	conn.commit()

	conn.close()



def submit():
	conn = sqlite3.connect('lawsuits.db')
	c = conn.cursor()

	dash = []
	date = Date.get()
	for i in date:

		if i == "-":
			dash.append(i)

	if len(lawsuit_id.get()) == 0:
		messagebox.showerror("Error", f"Enter ID of the lawsuite")
		lawsuit_id.delete(0, END)
    		
	if len(dash) < 2 or len(dash) > 2:
		messagebox.showerror("Error", f"Enter proper Date EX. 28-05-1990")
		Date.delete(0, END)

	else:

		try:
			c.execute("INSERT INTO lawsuits VALUES  (:id, :prosecutors_office, :name_prosecutor, :article, :date, :notes, :sended_to, :send_cartons )",
			{
			'id': lawsuit_id.get(),
			'prosecutors_office': prosecutors_office.get(),
			'name_prosecutor': name_prosecutor.get(),
			'article': article.get(),
			"date": Date.get(),
			'notes': note.get(),
			'sended_to': send_with_opinion.get() ,
			'send_cartons': Sended_Cartons.get()

			})
			lawsuit_id.delete(0, END)
			prosecutors_office.delete(0, END)
			name_prosecutor.delete(0, END)
			article.delete(0, END)
			note.delete(0, END)
			send_with_opinion.delete(0, END)
			Sended_Cartons.delete(0, END)
			Date.delete(0, END)
		except Exception as ex:
			if str(ex) == "UNIQUE constraint failed: lawsuits.id":
    				# messagebox.showerror("Error", f"There is already lawsuite with this ID")
					pass


        

	conn.commit()

	conn.close()



def query():
	conn = sqlite3.connect('lawsuits.db')
	c = conn.cursor()

	showWIN = Toplevel(root) 
	showWIN.title("Data") 
	showWIN.geometry("1920x1080")
	showWIN.grab_set()
	ttk.Button(showWIN,text='CLOSE',width=10,command=showWIN.destroy).pack(pady=8)

	c.execute("SELECT *, oid FROM lawsuits")
	records = c.fetchall()

	print_records = ''
	Label(showWIN,text='All Lawsuites',width=500).pack()

	area=('ID',"Prosecutor's office", "Prosecutor's name", 'Article', 'Date Exipration', 'Note', 'Sended to', 'Cartons')
	ac=('all','n','e','s','ne','nw','sw','c')

	


	sales_data = []

	for record in records:
		law = (record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7])
		sales_data.append(law)

	tv=ttk.Treeview(showWIN,columns=ac,show='headings',height=45)
	for i in range(8):
		tv.column(ac[i],width=200,anchor='center')
		tv.heading(ac[i],text=area[i])


	tv.pack()

	vsb = ttk.Scrollbar(showWIN, orient="vertical", command=tv.yview)
	vsb.place(x=1760, y=65, height=925)

	tv.configure(yscrollcommand=vsb.set)


	for i in range(len(sales_data)):
    		tv.insert('','end',values=sales_data[i])
	
	root.mainloop()


	

	conn.commit()

	conn.close()





def expirable():
	conn = sqlite3.connect('lawsuits.db')
	c = conn.cursor()

	showWIN = Toplevel(root) 
	showWIN.title("Data") 
	showWIN.geometry("1920x1080")
	showWIN.grab_set()
	ttk.Button(showWIN,text='CLOSE',width=10,command=showWIN.destroy).pack(pady=8)




	expiring_lawsuits = []

	c.execute("SELECT *, oid FROM lawsuits")


	all_lawsuits = c.fetchall()


	for suite in all_lawsuits:
		expired_args = suite[4].split("-")
		expired_day = int(expired_args[0])
		expired_mounth = int(expired_args[1])
		expired_year = int(expired_args[2])



		today_date_generate = datetime.today().strftime('%d-%m-%Y')
		today_args = today_date_generate.split('-')
		today_day = int(today_args[0])
		today_mounth = int(today_args[1])
		today_year = int(today_args[2])


		expired_date = datetime(expired_year,expired_mounth,expired_day)
		today_date = datetime(today_year,today_mounth,today_day)
		difference = expired_date - today_date
		if difference.days <= 7:
			expiring_lawsuits.append(suite)

	
 

	print_records = ''
	Label(showWIN,text='All Expirable Lawsuites',width=500).pack()

	area=('ID',"Prosecutor's office", "Prosecutor's name", 'Article', 'Date Exipration', 'Note', 'Sended to', 'Cartons')
	ac=('all','n','e','s','ne','nw','sw','c')

	


	sales_data = []

	for record in expiring_lawsuits:
		law = (record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7])
		sales_data.append(law)

	tv=ttk.Treeview(showWIN,columns=ac,show='headings',height=45)
	for i in range(8):
		tv.column(ac[i],width=200,anchor='center')
		tv.heading(ac[i],text=area[i])


	tv.pack()

	vsb = ttk.Scrollbar(showWIN, orient="vertical", command=tv.yview)
	vsb.place(x=1760, y=65, height=925)

	tv.configure(yscrollcommand=vsb.set)


	for i in range(len(sales_data)):
		tv.insert('','end',values=sales_data[i],tags = ('oddrow',))
		tv.tag_configure('oddrow', background='orange')

	root.mainloop()


	

	conn.commit()

	conn.close()


lawsuit_id = Entry(root, width=30)
lawsuit_id.grid(row=0, column=1, padx=20, pady=(10, 0))

prosecutors_office = Entry(root, width=30)
prosecutors_office.grid(row=1, column=1)

name_prosecutor = Entry(root, width=30)
name_prosecutor.grid(row=2, column=1)

article = Entry(root, width=30)
article.grid(row=3, column=1)

send_with_opinion = Entry(root, width=30)
send_with_opinion.grid(row=4, column=1)

note = Entry(root, width=30)
note.grid(row=5, column=1)

Sended_Cartons = Entry(root, width=30)
Sended_Cartons.grid(row=6, column=1)

Date = Entry(root, width=30)
Date.insert(0, 'DD-MM-YYYY') 
Date.grid(row=7, column=1)


delete_box = Entry(root, width=25)
delete_box.grid(row=11, column=1, pady=5)



lawsuit_id_label = Label(root, text="lawsuit ID")
lawsuit_id_label.grid(row=0, column=0, pady=(10, 0))

prosecutors_office_label = Label(root, text="Prosecutor's office")
prosecutors_office_label.grid(row=1, column=0)

name_prosecutor_label = Label(root, text="name prosecutor")
name_prosecutor_label.grid(row=2, column=0)

article_label = Label(root, text="article")
article_label.grid(row=3, column=0)

send_with_opinion_label = Label(root, text="sended TO")
send_with_opinion_label.grid(row=4, column=0)

note_label = Label(root, text="note")
note_label.grid(row=5, column=0)

Sended_Cartons_label = Label(root, text="Sended Cartons")
Sended_Cartons_label.grid(row=6, column=0)

Date_label = Label(root, text="Date")
Date_label.grid(row=7, column=0)



delete_box_label = Label(root, text="Select ID")
delete_box_label.grid(row=11, column=0, pady=5)

submit_btn = Button(root, text="Add  Lawsuite To Database", command=submit,bg='grey')
submit_btn.grid(row=9, column=0, columnspan=2, pady=10, padx=10, ipadx=85)

query_btn = Button(root, text="Show all Lawsuite records", command=query,bg='grey')
query_btn.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=90)

edit_btn = Button(root, text="Edit Lawsuite", command=edit,bg='grey')
edit_btn.grid(row=12, column=0, columnspan=2, pady=10, padx=10, ipadx=130)

delete_btn = Button(root, text="Delete Lawsuite", command=delete,bg='grey')
delete_btn.grid(row=13, column=0, columnspan=2, pady=10, padx=10, ipadx=120)


sevenDays = Button(root, text="Expirable Lawsuites", command=expirable,bg='grey')
sevenDays.grid(row=14, column=0, columnspan=2, pady=10, padx=10, ipadx=110)

exit_button = Button(root, text="Exit", command=root.destroy ,bg='red') 
exit_button.grid(row=15, column=0, columnspan=2, pady=10, padx=10, ipadx=110)



conn.commit()

conn.close()

root.mainloop()
