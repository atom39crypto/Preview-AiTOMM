import os
from docx import Document

def write_word(file_name, content):
    doc = Document()
    doc.add_paragraph(content)
    doc.save(file_name)
    print(f"Word document '{file_name}' has been created!")

def write_code(file_name, content):
    with open(file_name, "w") as file:
        file.write(content)
    print(f"'{file_name}' has been created successfully.")

def get_desktop_folder():
    desktop = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")  # For Windows
    if not os.path.exists(desktop):
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")  # For macOS/Linux
    return desktop

def write(a, b):
    print("<-------------------------- genarating the file --------------------------->")
    if a.endswith(".docx"):
        desktop_folder = os.path.join(get_desktop_folder(), "Generated_Files")
        if not os.path.exists(desktop_folder):
            os.makedirs(desktop_folder) 

        file_path = os.path.join(desktop_folder, a)
        write_word(file_path, b)
    
    else:

        current_dir = os.getcwd()
        code_folder = os.path.join(current_dir, "Generated_Files")
        if not os.path.exists(code_folder):
            os.makedirs(code_folder)

        file_path = os.path.join(code_folder, a)
        write_code(file_path, b)
    
    return "file created"

if __name__ == "__main__":
    write("aslhkflkhasflhas.py", "print('Hello, world!')")  
    write("new.docx", "This is content for the Word file.")  