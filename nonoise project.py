from PIL import Image, ImageTk, ImageFilter, ImageEnhance
import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from rembg import remove

# Custom font and font size
custom_font = ("DG Trika", 10)

# Variable to track the processed image
processed_image = None


def apply_edge_detection(image): #توفيق
        grayscale_image = image.convert('L')
        np_image = np.array(grayscale_image)
        blurred_image = cv2.GaussianBlur(np_image, (5, 5), 0)
        edges = cv2.Canny(blurred_image, 50, 150)
        edges_pil_image = Image.fromarray(edges)
        return edges_pil_image

    # دالة عند الضغط على زر اكتشاف الحواف
def handle_detect_edges_button_click():
        global processed_image
        if not processed_image:
            messagebox.showwarning("Warning", "No processed image available.")
            return

        edges_image = apply_edge_detection(processed_image)

        show_processed_image(edges_image)


#________________ضيف__________________
def apply_emboss(image):
    """Applies emboss filter to the image."""
    try:
        # Convert to grayscale (optional, emboss filter works on any mode)
        # grayscale_image = image.convert('L')

        # Apply the emboss filter
        embossed_image = image.filter(ImageFilter.EMBOSS)
        return embossed_image
    except Exception as e:
        print(f"Error applying emboss filter: {e}")
        return image  # Return original image on error


def apply_contour(image):
    """Applies a contour filter to the given PIL Image."""

    try:
        return image.filter(ImageFilter.CONTOUR)
    except Exception as e:
        print(f"Error applying contour filter: {e}")
        return image

def apply_brightness(image, factor=1.5):
    """Applies brightness adjustment to the given PIL Image."""
    try:
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(factor)
    except Exception as e:
        print(f"Error applying brightness adjustment: {e}")
        return image
#________________ضيف__________________
# Dictionary to map filter names to corresponding functions
filters = {
    "Edge Detection": apply_edge_detection,
    "Emboss": apply_emboss,
    "Contour": apply_contour,
    "Brightness": apply_brightness
}

# Function to handle applying selected filter
def apply_filter(filter_name):
    global processed_image
    if not image:
        messagebox.showwarning("Warning", "No processed image available.")
        return

    # Apply the selected filter to the image
    filtered_image = filters[filter_name](image)

    # Display the processed image in the UI
    show_processed_image(filtered_image)

    # Store the processed image
    processed_image = filtered_image

#احمد جلال
def convert_image(image):
    grayscale_image = image.convert('L')
    return grayscale_image

#احمد جلال
def denoise_image(image):
    np_image = np.array(image)
    denoised_image = cv2.fastNlMeansDenoisingColored(np_image, 7, 7, 5, 10)
    denoised_pil_image = Image.fromarray(denoised_image)
    return denoised_pil_image

# احمد عمارة
def blur_image(image):
    np_image = np.array(image)
    blurred_image = cv2.GaussianBlur(np_image, (15, 15), 0)
    blurred_pil_image = Image.fromarray(blurred_image)
    return blurred_pil_image

# احمد جلال
def handle_convert_button_click():
    global processed_image
    if not image:
        messagebox.showwarning("Warning", "No processed image available.")
        return

    grayscale_image = convert_image(image)
    show_processed_image(grayscale_image)
    processed_image = grayscale_image

# احمد طارق
def handle_remove_background_button_click():
    global image, processed_image
    if not image:
        messagebox.showwarning("Warning", "No processed image available.")
        return

    try:
        output = remove(image)
        show_processed_image(output)
        processed_image = output

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while processing the image: {str(e)}")
        return

# احمد جلال
def handle_denoise_button_click():
    global processed_image
    if not image:
        messagebox.showwarning("Warning", "Please select an input image.")
        return

    denoised_image = denoise_image(image)
    show_processed_image(denoised_image)
    processed_image = denoised_image

#عمارة
def handle_blur_button_click():
    global processed_image
    if not image:
        messagebox.showwarning("Warning", "Please select an input image.")
        return

    blurred_image = blur_image(image)
    show_processed_image(blurred_image)
    processed_image = blurred_image

# حفظ الصور
def handle_save_button_click():
    global processed_image
    if not processed_image:
        messagebox.showwarning("Warning", "No processed image available.")
        return

    output_filename = filedialog.asksaveasfilename(title="Choose File Name", defaultextension=".png",
                                                   filetypes=[("Images", "*.png")])
    if not output_filename:
        messagebox.showwarning("Warning", "Please specify a path to save the processed image.")
        return

    processed_image.save(output_filename)
    messagebox.showinfo("Success", "The processed image has been saved successfully.")

# Function to handle selecting input image
def handle_input_image_selection():
    global image, image_path, img_tk
    image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image", "*.jpg;*.png;*.gif;*.jpeg")])
    image = Image.open(image_path)
    img_tk = ImageTk.PhotoImage(image)
    input_image_label.config(image=img_tk)

# Function to display processed image
def show_processed_image(image):
    processed_img_tk = ImageTk.PhotoImage(image)
    processed_image_label.config(image=processed_img_tk)
    processed_image_label.image = processed_img_tk

# Function to create the main interface
def create_main_interface():
    root = tk.Tk()
    root.title("nonnoise")
    root.option_add("*Font", custom_font)

    input_frame = tk.Frame(root, padx=10, pady=10)
    input_label = tk.Label(input_frame, text="Select Image:")
    input_label.grid(row=0, column=0, padx=5, pady=5)
    input_button = tk.Button(input_frame, text="Browse", command=handle_input_image_selection)
    input_button.grid(row=0, column=10, padx=5, pady=5)
    input_image_frame = tk.Frame(root, padx=250, pady=10)
    input_image_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")

    global input_image_label
    input_image_label = tk.Label(input_image_frame)
    input_image_label.grid(row=0, column=0, padx=5, pady=5)

    processed_image_frame = tk.Frame(root, padx=10, pady=10)
    processed_image_frame.grid(row=2, column=0, pady=10, padx=10, sticky="nsew")
    global processed_image_label
    processed_image_label = tk.Label(processed_image_frame)
    processed_image_label.grid(row=0, column=0, padx=250, pady=5)

    button_frame = tk.Frame(root, padx=10, pady=10)
    button_frame.grid(row=3, column=0, pady=10, padx=10, sticky="nsew")

    convert_button = tk.Button(button_frame, text="Color removal", command=handle_convert_button_click,background='orange')
    convert_button.grid(row=0, column=0, padx=15, pady=5, sticky="ew")

    remove_bg_button = tk.Button(button_frame, text="Remove background", command=handle_remove_background_button_click,background='orange')
    remove_bg_button.grid(row=1, column=0, padx=15, pady=5, sticky="ew")

    denoise_button = tk.Button(button_frame, text="Noise removal", command=handle_denoise_button_click,background='orange')
    denoise_button.grid(row=0, column=1, padx=15, pady=5, sticky="ew")

    blur_button = tk.Button(button_frame, text="Image blur", command=handle_blur_button_click,background="orange")
    blur_button.grid(row=0, column=2, padx=5, pady=15, sticky="ew")

    brightness_button = tk.Button(button_frame, text="Brightness", command=lambda: apply_filter("Brightness"),background='orange')
    brightness_button.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

    emboss_button = tk.Button(button_frame, text="Emboss", command=lambda: apply_filter("Emboss"),background='orange')
    emboss_button.grid(row=1, column=1, padx=15, pady=5, sticky="ew")

    contour_button = tk.Button(button_frame, text="Contour", command=lambda: apply_filter("Contour"),background='orange')
    contour_button.grid(row=1, column=2, padx=15, pady=5, sticky="ew")



    EdgeDetection_button = tk.Button(button_frame, text="Edge Detection", command=lambda: apply_filter("Edge Detection"),background='orange')
    EdgeDetection_button.grid(row=1, column=3, padx=15, pady=5, sticky="ew")

    filter_frame = tk.Frame(root, padx=10, pady=10)
    filter_frame.grid(row=4, column=0, pady=10, padx=10, sticky="nsew")


    save_button = tk.Button(button_frame, text="save", command=handle_save_button_click, background='yellow')
    save_button.grid(row=0, column=4, padx=15, pady=5, sticky="ew")

    root.grid_rowconfigure(5, weight=5)
    root.grid_columnconfigure(0, weight=1)
    root.geometry("800x700")
    root.resizable(True, True)
    input_frame.grid(row=0, column=0, pady=5, padx=270, sticky="nsew")
    input_image_frame.grid(row=1, column=0, pady=5, padx=5, sticky="nsew")
    processed_image_frame.grid(row=2, column=0, pady=5, padx=5, sticky="nsew")
    button_frame.grid(row=3, column=0, pady=5, padx=5, sticky="nsew")
    filter_frame.grid(row=4, column=0, pady=5, padx=5, sticky="nsew")
    root.mainloop()
def start_main_interface():
    splash_screen.destroy()  # إغلاق شاشة الترحيب
    create_main_interface()  # فتح الواجهة الأساسية


# إنشاء شاشة الترحيب
splash_screen = tk.Tk()
splash_screen.title("nonnoise" )


# تطبيق الخط على شاشة الترحيب
splash_screen.option_add("*Font", custom_font)

# تعيين حجم شاشة الترحيب
splash_screen.geometry("800x700")

# صورة الشعار
logo_path = "C:\\Users\DELL\Desktop\dsp-project\\53.png" # ضع مسار صورة الشعار هنا
logo_image = Image.open(logo_path)
logo_image = logo_image.resize((400, 100))
logo_tk = ImageTk.PhotoImage(logo_image)

# إضافة صورة الشعار
logo_label = tk.Label(splash_screen, image=logo_tk)
logo_label.pack(pady=50)

# إضافة وصف للفكرة
description_label = tk.Label(splash_screen, text="PROJECT-Digital Signal processing-2024"
                                                 "\nاحمد محمدجلال"
                                                 "\nاحمد محمد ضيف"
                                                 "\nاحمد محمد توفيق"
                                                 "\nاحمد طارق حسين"
                                                 "\nاحمد اشرف السعيد"
                                                 "\nاحمد محمد عمارة"
                                                 "\nSECTION 1")
description_label.pack(pady=10)

#  زر "ابدأ"
start_button = tk.Button(splash_screen, text="start", command=start_main_interface ,background='orange')
start_button.pack(pady=20)

# تشغيل شاشة الترحيب
splash_screen.mainloop()



