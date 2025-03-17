import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, Label, Button
from PIL import Image, ImageTk

# Function to load and process image
def convert_to_8bit():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not file_path:
        return

    # Load image and resize
    image = cv2.imread(file_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (256, 256), interpolation=cv2.INTER_NEAREST)

    # Reduce color palette (8-bit effect)
    Z = image.reshape((-1, 3))
    Z = np.float32(Z)
    K = 16  # Number of colors
    _, labels, centers = cv2.kmeans(Z, K, None, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0), 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    quantized = centers[labels.flatten()]
    output_image = quantized.reshape(image.shape)

    # Convert to PIL format for display
    img_pil = Image.fromarray(output_image)
    img_tk = ImageTk.PhotoImage(img_pil)

    # Show image in GUI
    label.config(image=img_tk)
    label.image = img_tk

    # Save image
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
    if save_path:
        img_pil.save(save_path)

# GUI Setup
root = tk.Tk()
root.title("8-Bit Image Converter")
root.geometry("400x500")

Label(root, text="Upload an image to convert to 8-bit", font=("Arial", 12)).pack(pady=10)
Button(root, text="Select Image", command=convert_to_8bit).pack(pady=10)
label = Label(root)
label.pack(pady=10)

root.mainloop()
