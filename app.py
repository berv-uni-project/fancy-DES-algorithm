import tkinter.filedialog as filedialog
import tkinter as tk
from fancyDES.fancyDES import FancyDES
import binascii


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.labelVar = tk.StringVar()
        self.outputVar = tk.StringVar()
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.find_file = tk.Button(self, text="Find File", command=self.find_file_event)
        self.find_file.pack(side="top")
        self.password = tk.Entry(self, show="*")
        self.password.pack()
        self.encrypt = tk.Button(self, text="Encrypt", command = self.encrypt_data)
        self.encrypt.pack()
        self.labelFile = tk.Label(self, textvariable = self.labelVar, relief = tk.RAISED)
        self.labelFile.pack()
        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")
        self.outputMessage = tk.Label(self, textvariable = self.outputVar, relief = tk.RAISED)
        self.outputMessage.pack(side="bottom")

    def find_file_event(self):
        self.filename = filedialog.askopenfilename()
        self.labelVar.set("Filename {}".format(self.filename))
        print(self.filename)

    def encrypt_data(self):
        filename = self.filename
        passwd = self.password.get()
        if (filename is not None) and (passwd is not None):
            MODE = "OFB"
            fancyDES = FancyDES(
                path=filename, key=passwd, fromFile=True
            )
            cipher = fancyDES.generate_cipher(mode=MODE)
            result = binascii.hexlify(cipher)
            self.outputVar.set(result)
            print(len(cipher))

root = tk.Tk()
app = Application(master=root)
app.mainloop()
