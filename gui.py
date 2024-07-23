from tkinter import *
from tkinter import ttk
import database

database.CONNECT(database.host, database.username, database.password)
if not database.CHECK_CONNECTION():
    print("Cannot connect to database")
    input("Press enter to continue...")

TABLES = database.GET_TABLES(database.db_name)
TABLE = None

root = Tk()
root.title("GUI for database")
root.geometry("1200x400")

tables_var = Variable(value=TABLES)
tables_listbox = Listbox(listvariable= tables_var, activestyle= DOTBOX)
tables_listbox.grid(row=0, column=0, columnspan=2, sticky=EW, padx=5, pady=5)




view_table = Frame(root)
view_table.grid(row=0, column=6, columnspan=2, sticky=EW, padx=5, pady=5)
view_table_scroll_y = Scrollbar(view_table)
view_table_scroll_y.pack(side=RIGHT, fill=Y)
view_table_scroll_x = Scrollbar(view_table, orient="horizontal")
view_table_scroll_x.pack(side=BOTTOM, fill=X)
tree_table = ttk.Treeview(view_table,yscrollcommand=view_table_scroll_y.set, xscrollcommand =view_table_scroll_x.set,
                          selectmode="browse")
tree_table.pack()

TextInputs: list[Entry] = []
TextOutputs: list[Label] = []
TextVars: list[StringVar] = []

def AddRow():
    row = []
    for inp in TextInputs:
        s = inp.get()
        if (s==""): row.append(None)
        else: row.append(s)
    database.WRITE_ROW(database.db_name, TABLE, tuple(row))
    update_table(1)

def DeleteRow():
    row = tree_table.item(tree_table.selection()[0])["values"]
    database.DELETE_ROW(database.db_name, TABLE, row)
    update_table(1)


DeleteButton = Button(root, text="Delete row", command=DeleteRow)
DeleteButton.grid_forget()

AddButton = Button(root, text="Add row", command=AddRow)
AddButton.grid(row=3, column=0, columnspan=2, sticky=EW, padx=5, pady=5)


def showDeleteButton(text:str):
    global DeleteButton
    DeleteButton.grid(row=2, column=0, columnspan=2, sticky=EW, padx=5, pady=5)

def hiddeDeleteButton():
    global DeleteButton
    DeleteButton.grid_forget()

def update_table(event) -> None:
    global TABLE, DeleteButton
    for item in tree_table.selection():
        tree_table.selection_remove(item)
    tree_table.delete(*tree_table.get_children())
    if TABLE==None: 
        hiddeDeleteButton()
        return
    fields = database.GET_FIELDS(database.db_name, TABLE)
    field_names = []
    for field in fields:
        field_names.append(field[0])
    #print(field_names)
    tree_table['columns'] = tuple(field_names)
    tree_table.column("#0", width=0,  stretch=NO)
    tree_table.heading("#0",text="",anchor=CENTER)
    j = 0
    for name in field_names:
        tree_table.column(name, anchor= W, width= 50)
        tree_table.heading(name, text= name, anchor= W)
        if (j >= len(TextInputs) or len(TextInputs)==0):
            entry = Entry(root)
            entry.place(x=j*200+140, y=280, width=170, height=20)
            var = StringVar(value= name)
            text = Label(root, textvariable=var)
            text.place(x=j*200+140, y=320, width=170, height=20)
            TextInputs.append(entry)
            TextOutputs.append(text)
            TextVars.append(var)
        else:
            TextInputs[j].delete(0, END)
            TextVars[j].set(name)
        j += 1
    while (len(TextInputs)>j):
        TextInputs[len(TextInputs)-1].place_forget()
        TextInputs.pop()
        TextOutputs[len(TextOutputs)-1].place_forget()
        TextOutputs.pop()
        TextVars.pop()
    #print(len(TextInputs))
    rows = database.READ_ALL(database.db_name, TABLE)
    i = 0
    for row in rows:
        tree_table.insert(parent='',index='end',iid=i,text='', values=row)
        i += 1 
    if i!=0:
        showDeleteButton("Delete " + field_names[0] + " "+ str(rows[len(rows)-1][0]))
        tree_table.selection_set([i-1])
    else:
        hiddeDeleteButton()
    

def table_selected(event) -> None:
    global TABLE
    if len(tables_listbox.curselection())==0:
        return
    TABLE = tables_listbox.get(tables_listbox.curselection())
    #print("selected")
    update_table(event)

def selectItemTree(event) -> None:
    if len(tree_table.selection())==0:
        return
    fields = database.GET_FIELDS(database.db_name, TABLE)
    showDeleteButton("Delete " + fields[0][0] + " " + str(tree_table.item(tree_table.selection()[0])["values"][0]))

tables_listbox.bind("<<ListboxSelect>>", table_selected)
tree_table.bind("<<TreeviewSelect>>", selectItemTree)


update_table(0)
root.mainloop()

database.DISCONNECT()