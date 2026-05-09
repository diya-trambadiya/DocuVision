import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import os
import easyocr
from scan import DocScanner

reader = easyocr.Reader(['en'])

class DocuVisionApp:

    def __init__(self, root):
        self.root = root
        self.root.title("DocuVision – CV Based Document Scanner")
        self.root.state('zoomed')   # FULL SCREEN
        self.root.configure(bg="#E9ECF2")

        self.scanner = DocScanner()
        self.image_paths = []
        self.processed_images = []
        self.current_index = 0

        self.build_ui()

    # ================= UI =================

    def build_ui(self):

        # HEADER
        header = tk.Frame(self.root, bg="#2F4F90", height=90)
        header.pack(fill="x")

        tk.Label(header,
                 text="DocuVision – CV Based Document Scanner",
                 bg="#2F4F90",
                 fg="white",
                 font=("Segoe UI", 20, "bold")).pack(pady=25)

        # BUTTONS
        btn_frame = tk.Frame(self.root, bg="#E9ECF2")
        btn_frame.pack(pady=15)

        self.btn(btn_frame, "Upload Images", self.upload_images).grid(row=0, column=0, padx=10)
        self.btn(btn_frame, "Process All", self.process_all).grid(row=0, column=1, padx=10)
        self.green_btn(btn_frame, "Save Current", self.save_current).grid(row=0, column=2, padx=10)
        self.green_btn(btn_frame, "Save All", self.save_all).grid(row=0, column=3, padx=10)
        self.green_btn(btn_frame, "Save PDF", self.save_pdf).grid(row=0, column=4, padx=10)
        self.green_btn(
            btn_frame,
            "Extract Text",
            self.extract_text
        ).grid(row=0, column=5, padx=10)

        # IMAGE AREA
        display_frame = tk.Frame(self.root, bg="#E9ECF2")
        display_frame.pack(pady=10)

        self.original_box = self.create_image_box(display_frame, "Original Image")
        self.original_box.grid(row=0, column=0, padx=30)

        self.processed_box = self.create_image_box(display_frame, "Processed Image")
        self.processed_box.grid(row=0, column=1, padx=30)

        # ROTATE BUTTON (SINGLE)
        rotate_frame = tk.Frame(self.root, bg="#E9ECF2")
        rotate_frame.pack(pady=10)

        self.dark_btn(rotate_frame, "Rotate Image", self.rotate_image).grid(row=0, column=0, padx=20)

        # NAVIGATION
        nav_frame = tk.Frame(self.root, bg="#E9ECF2")
        nav_frame.pack(pady=10)

        self.dark_btn(nav_frame, "<< Previous", self.previous_image).grid(row=0, column=0, padx=40)
        self.dark_btn(nav_frame, "Next >>", self.next_image).grid(row=0, column=1, padx=40)

        # STATUS
        self.status = tk.Label(self.root, text="Ready", bg="#D0D3DA", anchor="w")
        self.status.pack(fill="x", side="bottom")

    # ================= BUTTON STYLES =================

    def btn(self, parent, text, cmd):
        return tk.Button(parent, text=text, command=cmd,
                         bg="#3B6FD8", fg="white",
                         font=("Segoe UI", 10, "bold"),
                         width=14, height=2, bd=0)

    def green_btn(self, parent, text, cmd):
        return tk.Button(parent, text=text, command=cmd,
                         bg="#1E9E49", fg="white",
                         font=("Segoe UI", 10, "bold"),
                         width=14, height=2, bd=0)

    def dark_btn(self, parent, text, cmd):
        return tk.Button(parent, text=text, command=cmd,
                         bg="#3C4251", fg="white",
                         font=("Segoe UI", 10, "bold"),
                         width=14, height=2, bd=0)

    # ================= IMAGE BOX =================

    def create_image_box(self, parent, title):
        frame = tk.Frame(parent, bg="white", width=450, height=460, bd=1, relief="solid")
        frame.pack_propagate(False)

        tk.Label(frame, text=title, bg="white",
                 font=("Segoe UI", 12, "bold")).pack(pady=10)

        canvas = tk.Label(frame, bg="#F7F7F7")
        canvas.pack(expand=True, fill="both", padx=10, pady=10)

        frame.canvas = canvas
        return frame

    # ================= DISPLAY =================

    def show_image(self, img, box):
        img.thumbnail((400, 380))  # FIXED SIZE → no cutting
        img_tk = ImageTk.PhotoImage(img)
        box.canvas.config(image=img_tk)
        box.canvas.image = img_tk

    def display_current(self):
        if not self.image_paths:
            return

        img = Image.open(self.image_paths[self.current_index])
        self.show_image(img, self.original_box)

        if self.processed_images:
            img2 = Image.fromarray(self.processed_images[self.current_index])
            self.show_image(img2, self.processed_box)

    # ================= FUNCTIONS =================

    def upload_images(self):
        paths = filedialog.askopenfilenames(filetypes=[("Images", "*.jpg *.png *.jpeg" "*.webp")])
        if paths:
            self.image_paths = list(paths)
            self.processed_images = []
            self.current_index = 0
            self.display_current() 

    def process_all(self):
        self.processed_images = []
        for path in self.image_paths:
            self.processed_images.append(self.scanner.scan(path))
        self.display_current()

    def rotate_image(self):
        if self.processed_images:
            self.processed_images[self.current_index] = cv2.rotate(
                self.processed_images[self.current_index],
                cv2.ROTATE_90_CLOCKWISE
            )
            self.display_current()

    def save_current(self):
        if not self.processed_images:
            return
        file = filedialog.asksaveasfilename(defaultextension=".png")
        if file:
            cv2.imwrite(file, self.processed_images[self.current_index])

    def save_all(self):
        folder = filedialog.askdirectory()
        if folder:
            for i, img in enumerate(self.processed_images):
                cv2.imwrite(os.path.join(folder, f"scan_{i}.png"), img)

    def save_pdf(self):
        if not self.processed_images:
            return

        file = filedialog.asksaveasfilename(defaultextension=".pdf")
        if not file:
            return

        pil_images = []
        for img in self.processed_images:
            pil_img = Image.fromarray(img).convert("RGB")
            pil_images.append(pil_img)

        pil_images[0].save(file, save_all=True, append_images=pil_images[1:])
        self.status.config(text="Saved as PDF")

    def previous_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.display_current()

    def next_image(self):
        if self.current_index < len(self.image_paths) - 1:
            self.current_index += 1
            self.display_current()

    def previous_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.display_current()

    def next_image(self):
        if self.current_index < len(self.image_paths) - 1:
            self.current_index += 1
            self.display_current()

    def extract_text(self):

        if not self.processed_images:
            messagebox.showerror(
                "Error",
                "Please process an image first."
            )
            return

        current_img = self.processed_images[self.current_index]

        result = reader.readtext(current_img)

        extracted_text = ""

        for detection in result:
            extracted_text += detection[1] + "\n"

        text_window = tk.Toplevel(self.root)

        text_window.title("OCR Output")
        text_window.geometry("700x500")

        text_box = tk.Text(
            text_window,
            width=80,
            height=25,
            font=("Segoe UI", 11)
        )

        text_box.pack(
            padx=10,
            pady=10
            
        )
        text_box.insert("1.0", extracted_text)

        save_btn = tk.Button(
            text_window,
            text="Save Extracted Text",
            command=lambda: self.save_extracted_text(extracted_text),
            bg="#1E9E49",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=10,
            pady=5
        )

        save_btn.pack(pady=10)
        

    def save_extracted_text(self, text):

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")]
        )

        if file_path:

            with open(file_path, "w", encoding="utf-8") as file:
                file.write(text)

            messagebox.showinfo(
                "Success",
                "Text file saved successfully."
            )


# ================= RUN =================

if __name__ == "__main__":
    root = tk.Tk()
    app = DocuVisionApp(root)
    root.mainloop()