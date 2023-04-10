from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog,messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
import cv2
from tkinter import RAISED
import math

    # khai bao ham
alphabet = " abcdefghijklmnopqrstuvwxyz,.#"
length_alphabet = len(alphabet)
x = 0
y = 0
a = 0
index = 0
dulieu = []

root = tk.Tk()
def MaHoa():
    global index,dulieu
    img = cv2.imread(filename)
    px = img[x,y]
    for i in range(3):
        if index==len(dulieu):
            break
        a = dulieu[index]-px[i]%length_alphabet
        if px[i]%length_alphabet==dulieu[index]:
            px[i] = px[i]
        elif abs(a) <(length_alphabet/2) and px[i] + a>=0 and px[i] + a<=255:
            px[i] = px[i] + a
        elif px[i]<length_alphabet:
            if dulieu[index] > px[i]:
                px[i]+=abs(px[i]-dulieu[index])
            else:
                px[i] -= abs(a)
        else:
            while px[i]%length_alphabet!=dulieu[index]:
                px[i]-=1
        index+=1
    img[x,y] = px
    cv2.imwrite(filename,img)


def openfn():
    filename = filedialog.askopenfilename(title='open')
    return filename
def open_img():
    global img,w,h,img_cv
    x = openfn()
    img = Image.open(x)
    w = img.width
    h = img.height
    img_cv = cv2.imread(img.filename)
    img = img.resize((300, 300))
    img = ImageTk.PhotoImage(img)
    panel = tk.Label(root, image=img)
    panel.image = img
    panel.grid(row=0,column=0,rowspan=3,sticky='NS')


def save_img():
    try:
        global img_cv,filename,dulieu,w,h,x,y
        """Save the current file as a new file."""
        filename = asksaveasfilename(
            defaultextension=".png",
            filetypes=[("Text Files", "*.png"), ("All Files", "*.*")],
        )
        if not filename:
            return
        else:
            cv2.imwrite(filename,img_cv)
            text = frm_vanban.get(1.0,"end-1c")
            text +='#'
            chuthuong = text.lower()

            i=0
            while i<len(text):
                so = alphabet.find(chuthuong[i])
                dulieu += [so]
                i+=1
            k = int(frm_k.get())
            for i in range(math.ceil(len(chuthuong)/3)):
                MaHoa() 
                if x +k < h:
                    x+=k
                else:
                    x = 0
                    y += 3
        messagebox.showinfo("Complete", "Encode Complete")
    except :
        messagebox.showwarning("Warning", "Kiem tra lai anh va key cua ban")

def giai_ma():
    try:
        global w,h,length_alphabet,img_cv
        img_new = img_cv
        x1=0
        y1=0
        k = int(frm_k.get())
        run = True
        px1 = img_new[x1,y1]
        dulieu = []
        gm = ''
        while run:
            for i in range(3):
                if px1[i]%length_alphabet == length_alphabet-1:
                    run =False
                    break
                else:
                    dulieu +=[px1[i]]
            if x1 +k < h:
                x1+=k
                px1 = img_new[x1,y1]
            else:
                x1 = 0
                y1+= 3
                px1 = img_new[x1,y1]

        for i in dulieu:
            gm += alphabet[i%length_alphabet]
        frm_vanban.delete(1.0,tk.END)
        frm_vanban.insert(tk.END, gm.title())
        messagebox.showinfo("Complete", "Decryption Complete")
    except :
        messagebox.showwarning("Warning", "Kiem tra lai anh va key cua ban")

label_key = tk.Label(text="Key")
label_note = tk.Label(text="*Note: Key phai la 1 so tu nhien")
label_vanBan = tk.Label(text="Van ban")
frm_k = tk.Entry()
frm_vanban = tk.Text(root,height=25,width=50)


# create a button to trigger the save_image function
root.rowconfigure(0, minsize=25, weight=1)
root.columnconfigure(0, minsize=25, weight=1)

frm_buttons = tk.Frame(root, relief=RAISED, borderwidth=0)
btn_open = tk.Button(frm_buttons, text="Select image", command=open_img)
btn_save = tk.Button(frm_buttons, text="Encode & Save", command=save_img)
btn_decryption = tk.Button(frm_buttons, text="Decryption", command=giai_ma)

btn_open.grid(row=3, column=1, padx=5, pady=5)
btn_decryption.grid(row=3, column=2,padx=5)
btn_save.grid(row=3, column=3,padx=5)
frm_buttons.grid(columnspan=3,row=3,column=0, sticky='E')

label_key.grid(row=0, column=1, padx=5, pady=5,sticky='NEW')
frm_k.grid(row=0, column=2, padx=5, pady=5,sticky='NEW')
label_note.grid(row=1, column=2, padx=5, pady=5,sticky='W')

label_vanBan.grid(row=2, column=1, padx=5, pady=5,sticky='NEW')
frm_vanban.grid(row=2, column=2, padx=5,pady=5,sticky='NEWS')

root.geometry("800x510")
root.title("Welcome to Myapp")
root.resizable(width=True, height=True)
root.mainloop()