import os
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox, StringVar, Text, Toplevel, Scrollbar, END
from tkinter.font import Font
from PIL import Image

# Set up GUI colors
BACKGROUND_COLOR = "#2C2C2C"  # Dark Gray
TEXT_COLOR = "#00FF00"  # Green Text
SECONDARY_TEXT_COLOR = "#FFFF00"  # Yellow Secondary Text
BUTTON_COLOR = "#8B0000"  # Dark Red Buttons
BUTTON_HOVER_COLOR = "#FF0000"  # Blood Red (Hover Effect)
ENTRY_COLOR = "#1E1E1E"  # Black for Entry Background
ENTRY_TEXT_COLOR = "#FFFFFF"  # White Entry Text

DOCUMENTATION_FILE = "ileices_image2icon_documentation.txt"  # Default file for internal documentation


class ImageToIconApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ileices Image2Icon Converter")
        self.root.geometry("600x500")
        self.root.configure(bg=BACKGROUND_COLOR)

        # Input and Output Paths
        self.input_path = StringVar()
        self.output_path = StringVar()

        # Title Label
        Label(root, text="Ileices Image2Icon Converter", fg=SECONDARY_TEXT_COLOR, bg=BACKGROUND_COLOR, font=("Impact", 16)).pack(pady=10)

        # Input File Selection
        Label(root, text="Input Image Path:", fg=TEXT_COLOR, bg=BACKGROUND_COLOR, font=("Helvetica", 12)).pack()
        self.input_entry = Entry(root, textvariable=self.input_path, bg=ENTRY_COLOR, fg=ENTRY_TEXT_COLOR, font=("Helvetica", 10), width=50)
        self.input_entry.pack(pady=5)
        Button(root, text="Browse", command=self.select_input_file, bg=BUTTON_COLOR, fg=TEXT_COLOR, activebackground=BUTTON_HOVER_COLOR).pack()

        # Output Directory Selection
        Label(root, text="Output Directory:", fg=TEXT_COLOR, bg=BACKGROUND_COLOR, font=("Helvetica", 12)).pack(pady=10)
        self.output_entry = Entry(root, textvariable=self.output_path, bg=ENTRY_COLOR, fg=ENTRY_TEXT_COLOR, font=("Helvetica", 10), width=50)
        self.output_entry.pack(pady=5)
        Button(root, text="Browse", command=self.select_output_directory, bg=BUTTON_COLOR, fg=TEXT_COLOR, activebackground=BUTTON_HOVER_COLOR).pack()

        # Convert Button
        Button(root, text="Convert to Icon Formats", command=self.convert_to_icons, bg=BUTTON_COLOR, fg=TEXT_COLOR, activebackground=BUTTON_HOVER_COLOR).pack(pady=20)

        # Documentation Button
        Button(root, text="Documentation", command=self.open_documentation, bg=BUTTON_COLOR, fg=TEXT_COLOR, activebackground=BUTTON_HOVER_COLOR).pack(pady=5)

        # Copyright
        copyright_font = Font(underline=True)
        copyright_label = Label(root, text="The God Factory | Project Ileices | Roswan Miller", fg="#FF4500",
                                bg=BACKGROUND_COLOR, font=("Helvetica", 10, "italic"))
        copyright_label.pack(side="bottom", pady=5)
        copyright_label.bind("<Button-1>", lambda e: self.open_url("https://youtube.com/thegodfactory"))

    def select_input_file(self):
        """Open file dialog to select an image file."""
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.tiff;*.webp")]
        )
        if file_path:
            self.input_path.set(file_path)

    def select_output_directory(self):
        """Open file dialog to select an output directory."""
        directory = filedialog.askdirectory()
        if directory:
            self.output_path.set(directory)

    def convert_to_icons(self):
        """Convert the input image to multiple icon formats."""
        input_file = self.input_path.get()
        output_dir = self.output_path.get()

        if not os.path.isfile(input_file):
            messagebox.showerror("Error", "Invalid input file path.")
            return
        if not os.path.isdir(output_dir):
            messagebox.showerror("Error", "Invalid output directory path.")
            return

        try:
            # Open the image
            img = Image.open(input_file)
            base_name = os.path.splitext(os.path.basename(input_file))[0]

            # Define sizes for various formats
            icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256), (512, 512)]

            # Save as .ico
            for size in icon_sizes:
                output_file = os.path.join(output_dir, f"{base_name}_{size[0]}x{size[1]}.ico")
                img.resize(size, Image.Resampling.LANCZOS).save(output_file, format="ICO")

            # Save as .icns (for macOS)
            icns_file = os.path.join(output_dir, f"{base_name}.icns")
            img.resize((512, 512), Image.Resampling.LANCZOS).save(icns_file, format="ICNS")

            # Save as .png for universal icon use
            for size in icon_sizes:
                output_file = os.path.join(output_dir, f"{base_name}_{size[0]}x{size[1]}.png")
                img.resize(size, Image.Resampling.LANCZOS).save(output_file, format="PNG")

            messagebox.showinfo("Success", "Image converted to all icon formats successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def open_documentation(self):
        """Open the documentation editor."""
        doc_window = Toplevel(self.root)
        doc_window.title("Documentation Editor")
        doc_window.geometry("600x400")
        doc_window.configure(bg=BACKGROUND_COLOR)

        Label(doc_window, text="Documentation Editor", fg=SECONDARY_TEXT_COLOR, bg=BACKGROUND_COLOR, font=("Helvetica", 14)).pack(pady=10)

        # Documentation Text Area
        scrollbar = Scrollbar(doc_window)
        scrollbar.pack(side="right", fill="y")
        text_area = Text(doc_window, bg=ENTRY_COLOR, fg=ENTRY_TEXT_COLOR, font=("Helvetica", 10), yscrollcommand=scrollbar.set)
        text_area.pack(expand=True, fill="both")
        scrollbar.config(command=text_area.yview)

        # Load existing documentation if available
        if os.path.exists(DOCUMENTATION_FILE):
            with open(DOCUMENTATION_FILE, "r") as doc_file:
                text_area.insert(END, doc_file.read())

        # Save Button
        Button(doc_window, text="Save Documentation", command=lambda: self.save_documentation(text_area), bg=BUTTON_COLOR, fg=TEXT_COLOR, activebackground=BUTTON_HOVER_COLOR).pack(pady=5)

    def save_documentation(self, text_area):
        """Save the documentation to a file."""
        content = text_area.get("1.0", END).strip()
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("Markdown Files", "*.md")])
        if save_path:
            with open(save_path, "w") as doc_file:
                doc_file.write(content)
            # Save internally as well
            with open(DOCUMENTATION_FILE, "w") as internal_file:
                internal_file.write(content)
            messagebox.showinfo("Saved", "Documentation saved successfully!")

    @staticmethod
    def open_url(url):
        """Open a URL in the default web browser."""
        import webbrowser
        webbrowser.open(url)


# Run the application
if __name__ == "__main__":
    root = Tk()
    app = ImageToIconApp(root)
    root.mainloop()
