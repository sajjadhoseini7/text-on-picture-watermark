from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from tkinter.colorchooser import askcolor
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont
import os, time

root =Tk()
root.title('Watermark Photos')
root.resizable(0,0)
displaycanvas = Canvas(root,width = 320, height = 450)#height=550 if textbox.place
displaycanvas.pack()

def app_guide():
    messagebox.showinfo('app guide','''1. Enter your desired text
2. Enter your font size
3. Click on Choose font color and choose a color you want
4. Click on Choose your font and choose a font file(*.ttf)
5. Click on Choose your pictures' folder path and choose the wanted folder
6. Click on Choose a folder path to save watermarked images
7. Choose a position to locate the watermark on your pictures
8. Choose a margin to keep a distance between the watermark and margins of the photo
9. Click on WaterMark to start the process
''')
def app_creator():
    messagebox.showinfo('app creator','This app is created by Sajjad Hoseini & all rights reserved.')

menubar= Menu(root)
creditmenu=Menu(menubar,tearoff=0)
creditmenu.add_command(label='How to use the app?',command=app_guide)
creditmenu.add_separator()
creditmenu.add_command(label='Credit',command=app_creator)
menubar.add_cascade(label='Menu',menu=creditmenu)
root.config(menu=menubar)

textbox = Text(root,height=10,width=36)
#textbox.place(x=10,y=380)
textbox.pack(side='left',fill=Y)
scroll_bar=Scrollbar(root)
#scroll_bar.place(x=302,y=380)
scroll_bar.pack(side='right',fill=Y)
textbox.configure(yscrollcommand=scroll_bar.set)
scroll_bar.configure(command=textbox.yview)

t_var=StringVar()
Label(root,text='Enter your text:').place(x=10,y=10)
Entry(root,textvariable=t_var,width=50).place(x=10,y=30)

fs_var=IntVar()
Label(root,text='Enter your font size:').place(x=10,y=60)
Entry(root,textvariable=fs_var,width=50).place(x=10,y=80)

def choose_color():
    color = askcolor()
    r=int(color[0][0])
    g=int(color[0][1])
    b=int(color[0][2])
    fc = f'{r},{g},{b}'
    fc_entry.delete(0,END)
    fc_entry.insert(0 , fc)
    
fc_var=StringVar()
fc_entry=Entry(root,textvariable=fc_var,width=50)
fc_entry.place(x=10,y=135)
ttk.Button(root , text="Choose font color" , command=choose_color).place(x=10,y=110)

def browse_font():
    filename = filedialog.askopenfilename(
        initialdir="/",  # Optional: Set initial directory
        title="Select a File",
        filetypes=[("All Files", "*.ttf*")]  # Optional: Filter file types
    )

    if filename:
        fp_entry.delete(0,END)
        fp_entry.insert(0,filename)

fp_var=StringVar()
fp_entry=Entry(root,textvariable=fp_var,width=50)
fp_entry.place(x=10,y=190)
ttk.Button(root, text="Choose your font", command=browse_font).place(x=10,y=165)

def browse_files_folder():
    folder_dir = filedialog.askdirectory(
        initialdir="/",  # Optional: Set initial directory
    )
    if folder_dir:
        op_entry.delete(0,END)
        op_entry.insert(0,folder_dir)
        
op_var=StringVar()
op_entry=Entry(root,textvariable=op_var,width=50)
op_entry.place(x=10,y=245)
ttk.Button(root, text="Choose your pictures' folder path", command=browse_files_folder).place(x=10,y=220)

def browse_folder_to_save():
    folder_dir = filedialog.askdirectory(
        initialdir="/",  # Optional: Set initial directory
    )
    if folder_dir:
        wp_entry.delete(0,END)
        wp_entry.insert(0,folder_dir)
        
wp_var=StringVar()
wp_entry=Entry(root,textvariable=wp_var,width=50)
wp_entry.place(x=10,y=300)
ttk.Button(root, text="Choose a folder path to save watermarked images", command=browse_folder_to_save).place(x=10,y=275)

Label(root,text='Position of Watermark:').place(x=10,y=330)
pos_var=StringVar()
position=ttk.Combobox(root,width=47,textvariable=pos_var)
position['values']=('top left','top center','top right',
                    'center left','center','center right',
                    'bottom left','bottom center','bottom right')
position.place(x=10,y=350)
position.current(8)

Label(root,text='Margin:').place(x=10,y=380)
mar_var=IntVar()
Spinbox(root,width=48,from_=0, to=100,textvariable=mar_var).place(x=10,y=400)

def watermark():
    t1 = time.time()
    folder_path = op_var.get()
    image_extensions = ('.jpg', '.JPG','.JPEG','.jpeg','png','PNG')
    text = t_var.get()
    font_size = fs_var.get()
    font_path = fp_var.get()
    font = ImageFont.truetype(font_path, font_size)
    text_length = int(font.getlength(text))
    fc = fc_var.get().split(',')
    font_color = (int(fc[0]),int(fc[1]),int(fc[2]))
    watermarked_pics_path=wp_var.get()
    pos=pos_var.get()
    margin=mar_var.get()
    i=1
    length = len(os.listdir(folder_path))
    textbox.configure(state=NORMAL)
    textbox.delete('1.0',END)
    textbox.tag_configure('left',justify='left',font=('Times New Roman',10))
    textbox.insert(END,length)
    textbox.insert(END,'\n')
    textbox.tag_add('left',1.0,'end')
    root.update()
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(image_extensions):
            image_path = os.path.join(folder_path, filename)
            im = Image.open(image_path)
            width, height = im.size
            draw = ImageDraw.Draw(im)
            if pos=='top left':
                x = margin
                y = margin
            elif pos=='top center':
                x = (width//2)-(text_length//2)
                y = margin
            elif pos=='top right':
                x = width - (text_length + margin)
                y = margin
            elif pos=='center left':
                x = margin
                y = height//2
            elif pos=='center':
                x = (width//2)-(text_length//2)
                y = height//2
            elif pos=='center right':
                x = width - (text_length + margin)
                y = height//2
            elif pos=='bottom left':
                x = margin
                y = height - (font_size + margin)
            elif pos=='bottom center':
                x = (width//2)-(text_length//2)
                y = height - (font_size + margin)
            elif pos=='bottom right':
                x = width - (text_length + margin)
                y = height - (font_size + margin)

            draw.text((x, y), text, font=font, fill=font_color)
            im.save(f'{watermarked_pics_path}\watermarked {filename}')
            percent = round((i/length*100),2)
            textbox.insert(END,f'{filename}, Percentage completed: {percent}%')
            textbox.insert(END,'\n')
            textbox.tag_add('left',1.0,'end')
            i+=1
            root.update()
    t2 = time.time()
    exec_time = round(t2-t1,2)
    textbox.insert(END,f'Execution time: {exec_time} seconds')
    textbox.tag_add('left',1.0,'end')
    textbox.configure(state=DISABLED)
    root.update()

ttk.Button(root ,text = "WaterMark" ,command=watermark).place(x=115,y=425)

root.mainloop()

#author: Sajjad Hoseini
