# Photo Crop Tool for 10x15/15x10 Prints

## Motivation

This tool was created to solve a common problem when ordering photo prints online. Many web applications for photo printing services do not provide adequate tools to crop images to the standard 10x15 cm (or 15x10 cm) aspect ratio. This can lead to unwanted automatic cropping, cutting off important parts of the photo.

This simple desktop application allows you to manually crop your photos with the correct aspect ratio *before* uploading them, ensuring your prints look exactly the way you want.

## Features

- **Graphical User Interface**: An easy-to-use interface for selecting a folder and cropping images.
- **Correct Aspect Ratio**: Automatically applies a 10x15 (portrait) or 15x10 (landscape) cropping frame.
- **Interactive Cropping**: Move the cropping frame around with your mouse or arrow keys to get the perfect composition.
- **Boundary Detection**: The cropping frame cannot be moved outside the image boundaries.
- **High-Resolution Output**: Cropped images are saved in Full HD (1920px on the longest side) to maintain high quality for printing.
- **Batch Processing**: Easily loop through all `.jpg` and `.jpeg` images in a selected folder.
- **Organized Output**: Cropped images are saved automatically into a new `edited` subfolder within your source directory.
- **Streamlined Workflow**:
    - The first image loads automatically after selecting a folder.
    - Simply press the `Enter` key to save and move to the next image.

## Prerequisites

- Python 3 must be installed on your system.

## Installation

1.  **Clone or download the repository.**
2.  **Install the required Python libraries:**
    Open your terminal, navigate to the project directory, and run the following command:
    ```bash
    pip install -r requirements.txt
    ```

## How to Use

1.  **Run the application:**
    Open your terminal, navigate to the project directory, and run:
    ```bash
    python main.py
    ```
2.  **Select a Folder:**
    Click the **"Select Folder"** button and choose the directory containing the photos you want to edit.
3.  **Crop Your Image:**
    - The first image will load automatically.
    - A red rectangle will appear, representing the crop area.
    - Use your **mouse** or the **arrow keys** to move the rectangle and frame your photo as desired.
4.  **Save and Continue:**
    - Once you are happy with the crop, press the **`Enter`** key or click the **"Next"** button.
    - The cropped image will be saved in the `edited` subfolder, and the next image will appear.
5.  **Complete the Process:**
    - Repeat the process for all your photos.
    - When you have edited the last photo, a message will inform you that the task is complete. You can then close the application.
6.  **Upload Your Photos:**
    You can now find your perfectly cropped, high-resolution images in the `edited` folder, ready to be uploaded to your photo printing service.
