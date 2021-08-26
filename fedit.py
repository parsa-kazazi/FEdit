# -*- coding: utf-8 -*-
#
# FEdit: A pro text editor with tkinter library
# Coded by parsa kazazi
# GitHub: https://github.com/parsa-kazazi

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import os
import webbrowser


class TextEditor:
    def __init__(self) -> None:
        self.window = Tk()
        self.filename = "Untitled.txt"
        self.file = None
        self.file_data = None
        self.file_mode = "Plain Text"
        self.read_mode = "r"
        self.write_mode = "w"
        self.encoding = "utf-8"
        self.change_title()

        try:
            self.icon = PhotoImage(file="icon.png")
            self.window.iconphoto(False, self.icon)
        except:
            pass

        self.width = 1000
        self.height = 600

        self.window.configure(background="#ffffff")

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        left = (screen_width / 2) - (self.width / 2)
        top = (screen_height / 2) - (self.height / 2)

        self.window.geometry('%dx%d+%d+%d' % (self.width,
                                              self.height,
                                              left, top))
        
        self.menubar = Menu(self.window, bd=0, bg="#ffffff", fg="#000000", font=(None, 10))

        file_menu = Menu(self.menubar, tearoff=0, bg="#ffffff", fg="#000000", font=(None, 10))
        file_menu.add_command(label="Open...", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save)
        file_menu.add_command(label="Save as...", command=self.saveas)
        file_menu.add_command(label="Exit", command=self.exit_program)
        self.menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = Menu(self.menubar, tearoff=0, bg="#ffffff", fg="#000000", font=(None, 10))
        edit_menu.add_command(label="Undo", command=self.undo)
        edit_menu.add_command(label="Redo", command=self.redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Copy", command=self.copy)
        edit_menu.add_command(label="Cut", command=self.cut)
        edit_menu.add_command(label="Paste", command=self.paste)
        edit_menu.add_command(label="Select All", command=self.select_all)
        self.menubar.add_cascade(label="Edit", menu=edit_menu)

        theme_menu = Menu(self.menubar, tearoff=0, bg="#ffffff", fg="#000000", font=(None, 10))
        theme_menu.add_command(label="Light", command=lambda: self.apply_theme("light"))
        theme_menu.add_command(label="Dark", command=lambda: self.apply_theme("dark"))
        theme_menu.add_command(label="High contrast", command=lambda: self.apply_theme("high contrast"))
        self.menubar.add_cascade(label="Theme", menu=theme_menu)

        font_size_menu = Menu(self.menubar, tearoff=0, bg="#ffffff", fg="#000000", font=(None, 10))
        font_size_menu.add_command(label="Very small", command=lambda: self.apply_font_size(9))
        font_size_menu.add_command(label="Small", command=lambda: self.apply_font_size(10))
        font_size_menu.add_command(label="Medium", command=lambda: self.apply_font_size(11))
        font_size_menu.add_command(label="Large", command=lambda: self.apply_font_size(12))
        font_size_menu.add_command(label="Very large", command=lambda: self.apply_font_size(13))
        self.menubar.add_cascade(label="Font size", menu=font_size_menu)

        encoding_menu = Menu(self.menubar, tearoff=0, bg="#ffffff", fg="#000000", font=(None, 10))
        encoding_menu.add_command(label="UTF-8", command=lambda: self.change_encoding("utf-8"))
        encoding_menu.add_command(label="LATIN-1", command=lambda: self.change_encoding("latin-1"))
        self.menubar.add_cascade(label="Encoding", menu=encoding_menu)

        help_menu = Menu(self.menubar, tearoff=0, bg="#ffffff", fg="#000000", font=(None, 10))
        help_menu.add_command(label="About FEdit", command=self.show_about)
        help_menu.add_command(label="Web page", command=lambda: webbrowser.open("https://github.com/parsa-kazazi/FEdit"))
        self.menubar.add_cascade(label="Help", menu=help_menu)

        scroll_bar_y = Scrollbar(self.window, orient=VERTICAL, bg="#ffffff")
        scroll_bar_y.grid(row=0, column=1, sticky=N+S+E+W)

        scroll_bar_x = Scrollbar(self.window, orient=HORIZONTAL, bg="#ffffff")
        scroll_bar_x.grid(row=1, column=0, sticky=N+S+E+W)

        if os.name == "nt":
            self.font_name = "consolas"
        elif os.name == "posix":
            self.font_name = "monospace"

        self.text_input = Text(self.window, wrap=NONE, yscrollcommand=scroll_bar_y.set, xscrollcommand=scroll_bar_x.set, undo=True, bd=0)

        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        self.text_input.grid(sticky=N+E+S+W, row=0, column=0)

        scroll_bar_y.config(command=self.text_input.yview)
        scroll_bar_x.config(command=self.text_input.xview)

        self.info_label = Label(self.window, bg="#ffffff", fg="#000000")
        self.info_label.grid(sticky=W, row=2, column=0)
        self.info_label2 = Label(self.window, bg="#ffffff", fg="#000000")
        self.info_label2.grid(sticky=E, row=2, column=0)
    
    def open_file(self):
        self.fileaddr = filedialog.askopenfilename(title="Open File")
        self.load_file(self.fileaddr)
    
    def load_file(self, input_file):
        if self.fileaddr == () or self.fileaddr == "":
            pass
        else:
            if self.file_mode == "Binary":
                self.encoding = "utf-8"
            try:
                self.file = open(input_file, "r", encoding=self.encoding)
            except Exception as error_msg:
                messagebox.showerror("Error", str(error_msg))
                self.file = None
            else:
                try:
                    file_data = self.file.read()
                except UnicodeDecodeError:
                    open_file = messagebox.askyesno("File is binary", "This file is binary. do you want to open?")
                    if open_file:
                        self.read_mode = "rb"
                        self.write_mode = "wb"
                        self.file_mode = "Binary"
                        self.encoding = "Unknown"
                        self.file = open(input_file, self.read_mode)
                        file_data = self.file.read()
                    elif not open_file:
                        self.file = None
                except Exception as error_msg:
                    messagebox.showerror("Error", str(error_msg))
                    self.file = None
                else:
                    self.file_mode = "Plain Text"
                if self.file != None:
                    self.text_input.delete(0.0, END)
                    self.text_input.insert(END, file_data)
                    self.filename = os.path.basename(input_file)
                    self.file.close()
                    self.change_title()
                    self.show_file_info()
    
    def save(self):
        if self.file == None:
            self.saveas()
        else:
            try:
                self.file = open(self.fileaddr, self.write_mode)
                self.file.write(self.text_input.get(1.0, END))
                self.file.close()
            except Exception as error_msg:
                messagebox.showerror("Error", str(error_msg))
        self.show_file_info()
    
    def saveas(self):
        self.fileaddr = filedialog.asksaveasfilename(initialfile=self.filename)
        
        try:
            self.file = open(self.fileaddr, self.write_mode)
            self.file.write(self.text_input.get(0.0, END))
            self.filename = os.path.basename(self.fileaddr)
            self.file.close()
        except:
            pass
        
        self.change_title()
        self.show_file_info()
    
    def change_title(self):
        self.window.title(self.filename + " - FEdit")
    
    def show_file_info(self):
        if self.file == None:
            pass
        else:
            file_size = os.stat(self.fileaddr).st_size
            lines = open(self.fileaddr, self.read_mode).readlines()
            file_lines = 0

            for line in lines:
                file_lines += 1
            
            self.info_label.configure(text="File \"" + self.fileaddr + "\" : " + str(file_size) + " Byte(s) , " + str(file_lines) + " Line(s)  -  File mode: " + self.file_mode)
            self.info_label2.configure(text="Encoding: " + self.encoding)
    
    def change_encoding(self, _encoding):
        if self.file_mode == "Binary":
            messagebox.showerror("File is binary", "This file is binary. cannot change encoding.")
        else:
            self.encoding = _encoding
            try:
                s = self.text_input.get(0.0, END)
                self.load_file(self.fileaddr)
                self.text_input.delete(0.0, END)
                self.text_input.insert(END, s)
            except:
                pass
    
    def apply_theme(self, theme: str):
        if theme == "light":
            self.text_input.configure(bg="#ffffff", fg="#000000", insertbackground="#000000")
        elif theme == "dark":
            self.text_input.configure(bg="#202025", fg="#ffffff", insertbackground="#ffffff")
        elif theme == "high contrast":
            self.text_input.configure(bg="#000000", fg="#ffffff", insertbackground="#ffffff")
    
    def apply_font_size(self, font_size: int):
        self.text_input.configure(font=(self.font_name, font_size))
    
    def show_about(self):
        messagebox.showinfo("About", "FEdit: A pro text editor with tkinter library.\n\nGithub:\ngithub.com/parsa-kazazi/FEdit")
    
    def undo(self):
        try:
            self.text_input.edit_undo()
        except:
            pass
    
    def redo(self):
        try:
            self.text_input.edit_redo()
        except:
            pass
    
    def copy(self):
        self.text_input.event_generate("<<Copy>>")

    def cut(self):
        self.text_input.event_generate("<<Cut>>")
    
    def paste(self):
        self.text_input.event_generate("<<Paste>>")
    
    def select_all(self):
        self.text_input.event_generate("<<SelectAll>>")
    
    def exit_program(self):
        if self.file == None:
            save_file = messagebox.askyesno("Warning", "File is not saved. do you want to save it before exiting?")
            if save_file:
                self.save()
                self.window.quit()
                exit()
            elif not save_file:
                self.window.quit()
                exit()
        elif open(self.fileaddr, self.read_mode).read() != self.text_input.get(0.0, END):
            save_file = messagebox.askyesno("Warning", "File is not saved. do you want to save it before exiting?")
            if save_file:
                self.save()
                self.window.quit()
                exit()
            elif not save_file:
                self.window.quit()
                exit()
        else:
            self.window.quit()
            exit()

    def run(self):
        self.window.config(menu=self.menubar)
        self.apply_font_size(11)
        self.apply_theme("dark")
        self.window.mainloop()


if __name__ == "__main__":
    TextEditor().run()
