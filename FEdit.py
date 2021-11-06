# FEdit: A pro text editor with tkinter library
# Coded by parsa kazazi
# GitHub: https://github.com/parsa-kazazi

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import os
import time
import webbrowser


class FEdit:
    def __init__(self) -> None:
        self.window = Tk(className="FEdit")
        self.filename = "Untitled.txt"
        self.file = None
        self.file_data = None
        self.encoding = "UTF-8"
        self.change_title()

        try:
            self.icon = PhotoImage(file="icon.png")
            self.window.iconphoto(False, self.icon)
        except:
            pass

        self.width = 1000; self.height = 600

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        left = (screen_width / 2) - (self.width / 2)
        top = (screen_height / 2) - (self.height / 2)

        self.window.geometry('%dx%d+%d+%d' % (self.width, self.height, left, top))
        
        self.font = (None, 10)
        self.wrap = True
        
        self.menubar = Menu(self.window, bd=0, font=self.font)

        file_menu = Menu(self.menubar, tearoff=0, font=self.font)
        file_menu.add_command(label="Open...", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save)
        file_menu.add_command(label="Save as...", command=self.saveas)
        file_menu.add_command(label="Reload", command=self.reload)
        file_menu.add_command(label="New window", command=lambda: FEdit().run())
        file_menu.add_command(label="Close", command=self.close)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_program)
        self.menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = Menu(self.menubar, tearoff=0, font=self.font)
        edit_menu.add_command(label="Undo", command=self.undo)
        edit_menu.add_command(label="Redo", command=self.redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Copy", command=self.copy)
        edit_menu.add_command(label="Cut", command=self.cut)
        edit_menu.add_command(label="Paste", command=self.paste)
        edit_menu.add_command(label="Paste selection", command=self.paste_selection)
        edit_menu.add_command(label="Select All", command=self.select_all)
        edit_menu.add_separator()
        edit_menu.add_command(label="Find...", command=self.find)
        edit_menu.add_separator()
        edit_menu.add_command(label="Time / Date", command=self.insert_timedate)
        self.menubar.add_cascade(label="Edit", menu=edit_menu)

        theme_menu = Menu(tearoff=0, font=self.font)
        theme_menu.add_command(label="Light", command=lambda: self.apply_theme("light"))
        theme_menu.add_command(label="Dark", command=lambda: self.apply_theme("dark"))
        theme_menu.add_command(label="High contrast", command=lambda: self.apply_theme("high contrast"))

        font_size_menu = Menu(tearoff=0, font=self.font)
        font_size_menu.add_command(label="Very small", command=lambda: self.apply_font_size(9))
        font_size_menu.add_command(label="Small", command=lambda: self.apply_font_size(10))
        font_size_menu.add_command(label="Medium", command=lambda: self.apply_font_size(11))
        font_size_menu.add_command(label="Large", command=lambda: self.apply_font_size(12))
        font_size_menu.add_command(label="Very large", command=lambda: self.apply_font_size(13))

        encoding_menu = Menu(tearoff=0, font=self.font)
        encoding_menu.add_command(label="UTF-8 (Default)", command=lambda: self.change_encoding("UTF-8"))
        encoding_menu.add_command(label="UTF-16", command=lambda: self.change_encoding("UTF-16"))
        encoding_menu.add_command(label="UTF-32", command=lambda: self.change_encoding("UTF-32"))
        encoding_menu.add_command(label="LATIN 1", command=lambda: self.change_encoding("LATIN-1"))
        encoding_menu.add_command(label="ASCII", command=lambda: self.change_encoding("ASCII"))
        encoding_menu.add_command(label="ISO 8859-1", command=lambda: self.change_encoding("ISO-8859-1"))
        encoding_menu.add_command(label="Windows-1250", command=lambda: self.change_encoding("Windows-1250"))
        encoding_menu.add_command(label="GBK", command=lambda: self.change_encoding("GBK"))
        encoding_menu.add_command(label="ISO-2022-JP-2004", command=lambda: self.change_encoding("ISO-2022-JP-2004"))
        encoding_menu.add_command(label="KS X 1001", command=lambda: self.change_encoding("KS-X-1001"))
        encoding_menu.add_command(label="BIG 5", command=lambda: self.change_encoding("BIG5"))

        settings_menu = Menu(self.menubar, self.menubar, tearoff=0, font=self.font)
        settings_menu.add_cascade(label="Theme", menu=theme_menu)
        settings_menu.add_cascade(label="Font size", menu=font_size_menu)
        settings_menu.add_cascade(label="Encoding", menu=encoding_menu)
        self.menubar.add_cascade(label="Settings", menu=settings_menu)

        help_menu = Menu(self.menubar, tearoff=0, font=self.font)
        help_menu.add_command(label="About FEdit", command=self.show_about)
        help_menu.add_command(label="Web page", command=lambda: webbrowser.open("https://github.com/parsa-kazazi/FEdit"))
        self.menubar.add_cascade(label="Help", menu=help_menu)

        scroll_bar_y = Scrollbar(self.window, orient=VERTICAL)
        scroll_bar_y.grid(row=0, column=1, sticky=N+S+E+W)

        scroll_bar_x = Scrollbar(self.window, orient=HORIZONTAL)
        scroll_bar_x.grid(row=1, column=0, sticky=N+S+E+W)

        if os.name == "nt":
            self.editor_font = "consolas"
        elif os.name == "posix":
            self.editor_font = "monospace"

        self.text_input = Text(self.window, wrap=NONE, yscrollcommand=scroll_bar_y.set, xscrollcommand=scroll_bar_x.set, undo=True, bd=1)

        self.text_input.bind("<Button-3>", self.rightclick_menu)

        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        self.text_input.grid(row=0, column=0, sticky=N+E+S+W)

        scroll_bar_y.config(command=self.text_input.yview)
        scroll_bar_x.config(command=self.text_input.xview)

        self.info_label = Label(self.window)
        self.info_label.grid(sticky=W, row=2, column=0)
        self.info_label2 = Label(self.window)
        self.info_label2.grid(sticky=E, row=2, column=0)

        self.show_info()
    
    def open_file(self):
        self.fileaddr = filedialog.askopenfilename(title="Open File")
        self.load_file(self.fileaddr)
    
    def load_file(self, input_file):
        if self.fileaddr == () or self.fileaddr == "":
            pass
        else:
            try:
                self.file = open(input_file, "r", encoding=self.encoding)
                self.filename = os.path.basename(input_file)
            except Exception as error_msg:
                messagebox.showerror("Error", str(error_msg))
                self.file = None
            else:
                try:
                    file_data = self.file.read()
                except UnicodeDecodeError:
                    messagebox.showerror("Error", self.encoding + " codec can't decode file \"" + self.filename + "\"")
                    self.file = None
                except Exception as error_msg:
                    messagebox.showerror("Error", str(error_msg))
                    self.file = None
                else:
                    self.text_input.delete(0.0, END)
                    self.text_input.insert(END, file_data)
                    self.file.close()
                    self.change_title()
                    self.show_info()
    
    def save(self):
        if self.file == None:
            self.saveas()
        else:
            try:
                self.file = open(self.fileaddr, "w", encoding=self.encoding)
                self.file.write(self.text_input.get(1.0, END))
                self.file.close()
            except Exception as error_msg:
                messagebox.showerror("Error", str(error_msg))
        self.show_info()
    
    def saveas(self):
        self.fileaddr = filedialog.asksaveasfilename(initialfile=self.filename)
        
        try:
            self.file = open(self.fileaddr, "w", encoding=self.encoding)
            self.file.write(self.text_input.get(0.0, END))
            self.filename = os.path.basename(self.fileaddr)
            self.file.close()
        except:
            pass

        self.show_info()
    
    def reload(self): self.load_file(self.fileaddr)
    
    def close(self):
        self.file = None
        self.filename = "Untitled.txt"
        self.text_input.delete(0.0, END)
        self.change_title()
        self.info_label.configure(text="")
    
    def change_title(self): self.window.title(self.filename + " - FEdit")
    
    def rightclick_menu(self, event):
        menu = Menu(self.window, tearoff=0, cursor="left_ptr")
        menu.add_command(label="Copy", command=self.copy)
        menu.add_command(label="Cut", command=self.cut)
        menu.add_command(label="Paste", command=self.paste)
        menu.add_command(label="Paste Selection", command=self.paste_selection)
        menu.add_command(label="Select All", command=self.select_all)
        menu.add_separator()
        menu.add_command(label="Cancel", command=menu.destroy)

        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    def show_info(self):
        self.info_label2.configure(text="Encoding: " + self.encoding)
        if self.file == None:
            pass
        else:
            file_size = os.stat(self.fileaddr).st_size
            file_lines = len(open(self.fileaddr, "r", encoding=self.encoding).readlines())
            
            self.info_label.configure(text="File \"" + self.fileaddr + "\" : " + str(file_size) + " Byte(s) , " + str(file_lines) + " Line(s)")
    
    def change_encoding(self, _encoding):
        self.encoding = _encoding

        try:
            self.load_file(self.fileaddr)
        except:
            self.show_info()

    def apply_theme(self, theme: str):
        if theme == "light":
            self.text_input.configure(bg="#ffffff", fg="#000000", insertbackground="#000000")
            self.theme = "light"
        elif theme == "dark":
            self.text_input.configure(bg="#202020", fg="#ffffff", insertbackground="#ffffff")
            self.theme = "dark"
        elif theme == "high contrast":
            self.text_input.configure(bg="#000000", fg="#ffffff", insertbackground="#ffffff")
            self.theme = "high contrast"
    
    def apply_font_size(self, font_size: int):
        self.text_input.configure(font=(self.editor_font, font_size))
    
    def show_about(self):
        messagebox.showinfo("About", "FEdit: A pro text editor using tkinter library.\n\nGithub:\ngithub.com/parsa-kazazi/FEdit")

    def copy(self): self.text_input.event_generate("<<Copy>>")

    def cut(self): self.text_input.event_generate("<<Cut>>")

    def paste(self): self.text_input.event_generate("<<Paste>>")

    def paste_selection(self): self.text_input.event_generate("<<Copy>>"); self.text_input.event_generate("<<Paste>>")
    
    def select_all(self): self.text_input.event_generate("<<SelectAll>>")
    
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
    
    def find(self):
        self.find_window = Tk()
        self.find_window.title("Find")
        self.find_window.geometry("300x70")

        Label(self.find_window, text="Find: ", font=self.font).grid(row=0, column=0)

        self.find_entry = Entry(self.find_window, font=self.font)
        self.find_entry.grid(row=0, column=1)

        Button(self.find_window, text="Find", font=self.font, command=self.find_in_text).grid(row=0, column=2)
        Button(self.find_window, text="Close", font=self.font, command=self.close_find_window).grid(row=1, column=1)

        self.find_window.mainloop()
    
    def find_in_text(self):
        self.text_input.tag_remove("found", "1.0", END)
        search = self.find_entry.get()
        if search:
            idx = "1.0"
            while 1:
                idx = self.text_input.search(search, idx, nocase=1, stopindex=END)
                if not idx:
                    break
                lastidx = "%s+%dc" % (idx, len(search))
                self.text_input.tag_add("found", idx, lastidx)
                idx = lastidx
            self.text_input.tag_config("found", background="red")
        else:
            pass
        self.find_entry.focus_set()
    
    def close_find_window(self):
        self.text_input.tag_delete("found")
        self.find_window.destroy()
    
    def insert_timedate(self):
        time_and_date = time.strftime("%Y/%m/%d %H:%M:%S")
        self.text_input.insert(END, time_and_date + " ")
    
    def exit_program(self):
        if self.file == None:
            save_file = messagebox.askyesnocancel("Warning", "File is not saved. do you want to save it before exiting?")

            if save_file:
                self.save()
                self.window.quit()
                exit()
            elif not save_file:
                self.window.quit()
                exit()
            elif save_file == None:
                pass
        elif open(self.fileaddr, "r", encoding=self.encoding).read() != self.text_input.get(0.0, END):
            save_file = messagebox.askyesnocancel("Warning", "File is not saved. do you want to save it before exiting?")

            if save_file:
                self.save()
                self.window.quit()
                exit()
            elif not save_file:
                self.window.quit()
                exit()
            elif save_file == None:
                pass
        else:
            self.window.quit()
            exit()

    def run(self):
        self.window.config(menu=self.menubar)
        self.apply_font_size(11)
        self.apply_theme("dark")
        self.window.mainloop()


if __name__ == "__main__":
    FEdit().run()
