from email.mime import image
from tkinter import*
from tkinter import ttk, Menu,colorchooser,filedialog,messagebox 
from PIL import Image,ImageTk
import PIL.ImageGrab as ImageGrab
import tkinter as tk
import os


# Create root master with the Tk constructor
root=Tk()
root.title('Whiteboard')
root.geometry('1050x570+130+50')
root.resizable(0,0)


current_x = 0
current_y = 0
color = 'black'
erase_clr = 'white'


# location on board to draw
def locate_xy(work):
    global current_y,current_x
    current_x = work.x
    current_y = work.y

# create drawing
def add_line(work):
    global current_y,current_x
    board.create_line((current_x,current_y,work.x,work.y),width=get_current_value(),fill=color)
    current_x,current_y = work.x,work.y

# activate choosen color
def show_color(new_clr):
    global color
    color = new_clr

def marker_clr_palette():
    color_choose=colorchooser.askcolor()
    show_color(color_choose[1])

# background clr change btn event
def board_color():
    global bg_color
    global erase_clr
    bg_color = colorchooser.askcolor()
    board.config(background=bg_color[1])
    bg_clr.config(bg=bg_color[1])
    erase_clr = bg_color[1]

#clear btn event
def new_board():
    global erase_clr 
    board.delete("all")
    board.config(background='white')
    bg_clr.config(bg="white")
    erase_clr = 'white'

# erase btn event
def erase():
    global color
    color = erase_clr

# save event
def save_board():
    try:
        filename = filedialog.asksaveasfilename(defaultextension='jpg',
        filetypes=[("All files","*.*"),('JPG file','*.jpg')])
        x = root.winfo_rootx()+board.winfo_x()
        y = root.winfo_rooty()+board.winfo_y()
        x1 = x + board.winfo_width()
        y1 = y + board.winfo_height()
        ImageGrab.grab().crop((x,y,x1,y1)).save(filename)
        messagebox.showinfo("image is saved as"+str(filename))
    except:
        messagebox.showerror("unable to save image \n something went wrong")


# view event
def show_image():
    try:
        filename=filedialog.askopenfilename(initialdir=os.getcwd(),title="Select Image File",
            filetypes=(('JPG file','*.jpg'),('All File','*.*')))
        img=Image.open(filename)
        img=ImageTk.PhotoImage(img)
        lbl=Label(root,image=img,width=930,height=500)
        lbl.image=img
        lbl.place(x=100,y=10)
    except:
        messagebox.showerror("SORRY! File not found")




# creating menu
my_menu = Menu(root,)
file_menu = Menu(my_menu,tearoff='off',)
file_menu.add_command(label='Save',command=save_board)
file_menu.add_command(label='View',command=show_image)
my_menu.add_cascade(label='File',menu=file_menu)

my_menu2 = Menu(root)
file_menu = Menu(my_menu2,tearoff='off')
file_menu.add_command(label='Brush Color',command=marker_clr_palette)
file_menu.add_command(label='Background Color',command=board_color)
my_menu.add_cascade(label='Options',menu=file_menu,)

root.config(menu=my_menu)

# logo
logo = PhotoImage(file='logo.png')
root.iconphoto(False,logo)

# color palette
color_palette=PhotoImage(file='color section.png')
Label(root,image=color_palette,).place(x=10,y=10)

# eraser button
eraser = PhotoImage(file='eraser.png')
Button(root,image=eraser,command=erase).place(x=30,y=380)

# clear button
clear = PhotoImage(file='clear.png')
Button(root,image=clear,width=35,height=28,command=new_board).place(x=30,y=425)

# background color change button
bg_clr = Button(root,bg='white',width=5,command=board_color)
bg_clr.place(x=30,y=500)

# color palette canvas
colors= Canvas(root,width=37,height=310,bg='#f2f3f5',border=10,bd=0)
colors.place(x=30,y=60)

# Board
board=Canvas(root,background='white',width=930,height=500,cursor="hand2")
board.place(x=100,y=10)

# binding board with button
board.bind("<Button-1>",locate_xy)
board.bind("<B1-Motion>",add_line)

# fill color in color palette
def create_palette():
    color_list = ["black", "#bf9f47", "#75286c", "#0ff2db", "#95c9a0", 
                    "#f20fae", "#736e14", "#122966", "#f26907", "#f2e707"]
    for i, clr in enumerate(color_list):
        y = 10 + (i * 30)
        id = colors.create_rectangle(10, y, 30, y + 20, fill=clr)
        colors.tag_bind(id, "<Button-1>", lambda x, c = clr: show_color(c))
   
create_palette()

# add slider
current_value = tk.DoubleVar()

def get_current_value():
    return f'{current_value.get():.2f}'

def slider_change(event):
    slider_value.config(text=get_current_value())


slider = ttk.Scale(root,from_=0,to=100,orient='horizontal',command=slider_change,variable=current_value)
slider.place(x=30,y=530)

slider_value = ttk.Label(root,text=get_current_value())
slider_value.place(x=30,y=540)

# main event loop
root.mainloop()





# References
# https://youtu.be/mNqPLIM90ts
# https://youtu.be/8-l1KjTj2qw
# https://youtu.be/bozzPsdja4o
# https://youtu.be/uW-NLL9dlBs