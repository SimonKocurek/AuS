import tkinter


class Gui:

    def __init__(self):
        root = tkinter.Tk()
        root.title('Ubytovací Informačný Systém')
        root.geometry("800x600")

        label1 = tkinter.Label(root, text='Test')
        label1.pack()

        root.mainloop()