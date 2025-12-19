import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

class ImageCropper(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Cropper")
        self.geometry("800x600")

        self.folder_path = ""
        self.image_files = []
        self.current_image_index = 0
        self.edited_folder_path = ""

        self.create_widgets()

    def create_widgets(self):
        # Frame for controls
        control_frame = tk.Frame(self)
        control_frame.pack(pady=10)

        # Folder selection
        select_folder_button = tk.Button(control_frame, text="Select Folder", command=self.select_folder)
        select_folder_button.pack(side=tk.LEFT, padx=5)

        # Start button
        start_button = tk.Button(control_frame, text="Start", command=self.start_processing)
        start_button.pack(side=tk.LEFT, padx=5)

        # Image display canvas
        self.canvas = tk.Canvas(self, bg="gray")
        self.canvas.pack(expand=True, fill=tk.BOTH)

        # Navigation buttons
        nav_frame = tk.Frame(self)
        nav_frame.pack(pady=10)

        next_button = tk.Button(nav_frame, text="Next", command=self.save_and_next)
        next_button.pack(side=tk.LEFT, padx=5)

        quit_button = tk.Button(nav_frame, text="Quit", command=self.quit)
        quit_button.pack(side=tk.LEFT, padx=5)

    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            self.image_files = [f for f in os.listdir(self.folder_path) if f.lower().endswith(('.jpg', '.jpeg'))]
            if not self.image_files:
                messagebox.showinfo("No Images Found", "No JPEG images found in the selected folder.")
            else:
                self.current_image_index = 0
                self.edited_folder_path = os.path.join(self.folder_path, "edited")
                os.makedirs(self.edited_folder_path, exist_ok=True)
                self.start_processing()

    def start_processing(self):
        if not self.folder_path:
            messagebox.showwarning("No Folder Selected", "Please select a folder first.")
            return
        if not self.image_files:
            messagebox.showinfo("No Images Found", "No JPEG images to process.")
            return
        
        self.display_image()
        self.bind("<Return>", lambda event: self.save_and_next())

    def display_image(self):
        if self.current_image_index < len(self.image_files):
            image_path = os.path.join(self.folder_path, self.image_files[self.current_image_index])
            self.original_image = Image.open(image_path)
            
            self.canvas.delete("all")
            self.show_image_on_canvas()

    def show_image_on_canvas(self):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        img_width, img_height = self.original_image.size
        
        # Determine aspect ratio (10x15 or 15x10)
        self.aspect_ratio = 1.5 if img_width > img_height else 1/1.5

        # Fit image to canvas
        if canvas_width / img_width < canvas_height / img_height:
            new_width = canvas_width
            new_height = int(new_width * img_height / img_width)
        else:
            new_height = canvas_height
            new_width = int(new_height * img_width / img_height)

        self.display_image_pil = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.display_image_tk = ImageTk.PhotoImage(self.display_image_pil)
        
        self.canvas.create_image(canvas_width // 2, canvas_height // 2, anchor=tk.CENTER, image=self.display_image_tk)

        self.setup_crop_rectangle()

    def setup_crop_rectangle(self):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        disp_img_width = self.display_image_pil.width
        disp_img_height = self.display_image_pil.height

        if self.aspect_ratio > 1:  # Landscape 15x10
            # Max width is the displayed image width
            if disp_img_width / 1.5 <= disp_img_height:
                rect_width = disp_img_width
                rect_height = disp_img_width / 1.5
            # Max height is the displayed image height
            else:
                rect_height = disp_img_height
                rect_width = disp_img_height * 1.5
        else:  # Portrait 10x15
            # Max height is the displayed image height
            if disp_img_height / 1.5 <= disp_img_width:
                rect_height = disp_img_height
                rect_width = disp_img_height / 1.5
            # Max width is the displayed image width
            else:
                rect_width = disp_img_width
                rect_height = disp_img_width * 1.5
        
        self.rect_width = rect_width
        self.rect_height = rect_height

        self.crop_rect = self.canvas.create_rectangle(
            (canvas_width - rect_width) / 2,
            (canvas_height - rect_height) / 2,
            (canvas_width + rect_width) / 2,
            (canvas_height + rect_height) / 2,
            outline="red", width=2
        )
        self.canvas.tag_bind(self.crop_rect, "<B1-Motion>", self.move_crop_rectangle)
        self.canvas.focus_set()
        self.canvas.bind("<Left>", lambda event: self.move_with_keys(event, -5, 0))
        self.canvas.bind("<Right>", lambda event: self.move_with_keys(event, 5, 0))
        self.canvas.bind("<Up>", lambda event: self.move_with_keys(event, 0, -5))
        self.canvas.bind("<Down>", lambda event: self.move_with_keys(event, 0, 5))

    def move_with_keys(self, event, dx, dy):
        x1, y1, x2, y2 = self.canvas.coords(self.crop_rect)
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        img_x_offset = (canvas_width - self.display_image_pil.width) / 2
        img_y_offset = (canvas_height - self.display_image_pil.height) / 2

        # Boundary checks
        if x1 + dx < img_x_offset:
            dx = img_x_offset - x1
        if y1 + dy < img_y_offset:
            dy = img_y_offset - y1
        if x2 + dx > img_x_offset + self.display_image_pil.width:
            dx = img_x_offset + self.display_image_pil.width - x2
        if y2 + dy > img_y_offset + self.display_image_pil.height:
            dy = img_y_offset + self.display_image_pil.height - y2
            
        self.canvas.move(self.crop_rect, dx, dy)

    def move_crop_rectangle(self, event):
        x, y = event.x, event.y
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        img_x_offset = (canvas_width - self.display_image_pil.width) / 2
        img_y_offset = (canvas_height - self.display_image_pil.height) / 2

        # Boundary checks
        if x - self.rect_width / 2 < img_x_offset:
            x = img_x_offset + self.rect_width / 2
        if y - self.rect_height / 2 < img_y_offset:
            y = img_y_offset + self.rect_height / 2
        if x + self.rect_width / 2 > img_x_offset + self.display_image_pil.width:
            x = img_x_offset + self.display_image_pil.width - self.rect_width / 2
        if y + self.rect_height / 2 > img_y_offset + self.display_image_pil.height:
            y = img_y_offset + self.display_image_pil.height - self.rect_height / 2

        self.canvas.moveto(self.crop_rect, x - self.rect_width / 2, y - self.rect_height / 2)

    def save_and_next(self):
        if self.current_image_index < len(self.image_files):
            self.save_cropped_image()
            self.current_image_index += 1
            if self.current_image_index < len(self.image_files):
                self.display_image()
            else:
                messagebox.showinfo("Done", "All images have been processed.")
                self.quit()

    def save_cropped_image(self):
        # Get crop box coordinates relative to the displayed image
        x1, y1, x2, y2 = self.canvas.coords(self.crop_rect)
        
        # Convert canvas coordinates to original image coordinates
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        img_x_offset = (canvas_width - self.display_image_pil.width) / 2
        img_y_offset = (canvas_height - self.display_image_pil.height) / 2

        scale_factor = self.original_image.width / self.display_image_pil.width

        crop_x1 = (x1 - img_x_offset) * scale_factor
        crop_y1 = (y1 - img_y_offset) * scale_factor
        crop_x2 = (x2 - img_x_offset) * scale_factor
        crop_y2 = (y2 - img_y_offset) * scale_factor

        cropped_image = self.original_image.crop((crop_x1, crop_y1, crop_x2, crop_y2))
        
        # Save the cropped image
        output_filename = self.image_files[self.current_image_index]
        output_path = os.path.join(self.edited_folder_path, output_filename)
        cropped_image.save(output_path, quality=95)


if __name__ == "__main__":
    app = ImageCropper()
    app.mainloop()
