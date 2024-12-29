import tkinter as tk
from tkinter import Label, Button, Entry, filedialog
from PIL import Image, ImageTk
import cv2
import pickle
import face_recognition
import sqlite3

# Initialize the database
def create_db():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS student (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            student_id TEXT,
            encoding BLOB
        )
    ''')
    conn.commit()
    conn.close()

# Create the database when the app starts
create_db()

# Fetch known faces and encodings from the database
def fetch_known_faces():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('SELECT name, encoding FROM student')
    rows = c.fetchall()
    conn.close()

    known_names = []
    known_encodings = []

    for name, encoding_blob in rows:
        # Deserialize encoding from binary
        encoding = pickle.loads(encoding_blob)
        known_names.append(name)
        known_encodings.append(encoding)

    return known_names, known_encodings

known_names, known_encodings = fetch_known_faces()

# Initialize webcam
video_capture = cv2.VideoCapture(0)

# Create the Tkinter window
root = tk.Tk()
root.title("Attendify")
root.geometry("800x600")
root.configure(bg="#C1E3E8")
root.resizable(False, False)

# Gray area for output feed
video_frame = tk.Frame(root, bg="#C1E3E8", width=800, height=500)
video_frame.pack_propagate(False)
video_frame.pack(pady=(30, 10))

video_label = Label(video_frame, bg="#C1E3E8")
video_label.pack(fill="both", expand=True)

# Buttons
button_frame = tk.Frame(root, bg="#C1E3E8")
button_frame.pack(side="bottom", pady=10)

add_button = Button(button_frame, text="Add Students", command=lambda: open_add_students(), bg="#7EE575", font=("Poppins", 12, "bold"), bd=0, borderwidth=1, relief="solid")
add_button.pack(side="left", padx=10)

remove_button = Button(button_frame, text="Remove Students", command=lambda: open_remove_students(), bg="#F38484", font=("Poppins", 12, "bold"), bd=0, borderwidth=1, relief="solid")
remove_button.pack(side="left", padx=10)

# Function to update the video feed
def update_frame():
    # Check if the main window is active
    if root.state() == "normal":  
        # Capture frame from webcam
        ret, frame = video_capture.read()
        if not ret:
            root.after(10, update_frame)
            return

        # Flip the frame for a mirror effect
        frame = cv2.flip(frame, 1)

        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Detect face locations and encodings
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_location, face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_names[first_match_index]

            # Draw rectangle and label
            top, right, bottom, left = face_location
            top, right, bottom, left = top * 4, right * 4, bottom * 4, left * 4
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        # Convert frame to ImageTk format
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb_frame)
        imgtk = ImageTk.PhotoImage(image=img)

        # Update the label with the new frame
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)

    # Schedule the next frame update
    root.after(33, update_frame)

update_frame()

# Function to open the Add Students window
def open_add_students():
    add_window = tk.Toplevel(root)
    add_window.title("Add Students")
    add_window.geometry("400x450")
    add_window.configure(bg="#C1E3E8")

    name_label = tk.Label(add_window, text="Student Name", bg="#C1E3E8", font=("Poppins", 12))
    name_label.pack(pady=10)
    name_entry = tk.Entry(add_window, font=("Poppins", 12))
    name_entry.pack(pady=5)

    id_label = tk.Label(add_window, text="Student ID", bg="#C1E3E8", font=("Poppins", 12))
    id_label.pack(pady=10)
    id_entry = tk.Entry(add_window, font=("Poppins", 12))
    id_entry.pack(pady=5)

    file_label = tk.Label(add_window, text="Select Image", bg="#C1E3E8", font=("Poppins", 12))
    file_label.pack(pady=10)

    file_name_label = tk.Label(add_window, text="No file selected", bg="#C1E3E8", font=("Poppins", 12))
    file_name_label.pack(pady=5)

    def browse_image():
        filename = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if filename:
            file_name_label.config(text=filename)
            image = face_recognition.load_image_file(filename)
            encoding = face_recognition.face_encodings(image)[0]

            # Add data to the database
            name = name_entry.get()
            student_id = id_entry.get()

            if not name or not student_id:
                tk.messagebox.showerror("Error", "Please fill in all fields.")
                return

            add_to_db(name, student_id, encoding)
            tk.messagebox.showinfo("Success", "Student added successfully!")
            add_window.destroy()

    browse_button = tk.Button(add_window, text="Browse", command=browse_image, font=("Poppins", 12, "bold"), bg="#7EE575", bd=0)
    browse_button.pack(pady=5)

    add_button = tk.Button(add_window, text="Add", command=lambda: tk.messagebox.showerror("Error", "Please select an image."), font=("Poppins", 12, "bold"), bg="#7EE575", bd=0)
    add_button.pack(pady=20)

# Function to add student data to the database
def add_to_db(name, student_id, encoding):
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    # Serialize encoding to binary
    serialized_encoding = pickle.dumps(encoding)
    c.execute('''
        INSERT INTO student (name, student_id, encoding)
        VALUES (?, ?, ?)
    ''', (name, student_id, serialized_encoding))
    conn.commit()
    conn.close()

# Function to open the Remove Students window
def open_remove_students():
    remove_window = tk.Toplevel(root)
    remove_window.title("Remove Students")
    remove_window.geometry("500x400")
    remove_window.configure(bg="#C1E3E8")

    def update_list():
        for widget in remove_window.winfo_children():
            widget.destroy()

        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute('SELECT * FROM student')
        students = c.fetchall()
        conn.close()

        # Display student entries
        row = 0
        for student in students:
            name_label = tk.Label(remove_window, text=f"ID: {student[2]}, Name: {student[1]}", bg="#C1E3E8", font=("Poppins", 12))
            name_label.grid(row=row, column=0, pady=5)

            def remove_student(student_id=student[0]):
                conn = sqlite3.connect('students.db')
                c = conn.cursor()
                c.execute('DELETE FROM student WHERE id=?', (student_id,))
                conn.commit()
                conn.close()
                update_list()

            remove_button = tk.Button(remove_window, text="Remove", command=remove_student, font=("Poppins", 12, "bold"), bg="#F38484", bd=0)
            remove_button.grid(row=row, column=1, padx=10)
            row += 1

    update_list()

root.mainloop()
video_capture.release()
