# Background Remover – Batch Image Processor

This tool automatically removes the background from every image inside a selected folder. It uses the **Rembg** machine-learning library to isolate the subject and generate clean, transparent PNG output files.

The script can be compiled into a standalone `.exe` so users can run it without Python installed.

---

## Features

- Bulk-process all images in an input folder  
- Removes backgrounds using the `rembg` AI model  
- Saves all processed images into an output folder  
- Automatically renames outputs using the pattern:

```
rmbg_<original_name>.png
```

- Accepts common image formats:
  - `.png`
  - `.jpg`
  - `.jpeg`
  - `.webp`

- Creates the output directory automatically if it does not exist  
- Logs each file as it is processed  

---

## Folder Structure

Your directory should look like this:

```
project/
│
├── main.exe              ← compiled program
├── README.md             ← this documentation
│
├── Input/                ← place images here
└── Output/               ← processed images are saved here
```

You may rename `Input` and `Output` as long as the executable is built with the correct paths.

---

## How It Works

When the program runs:

1. It reads every file inside the **Input** directory.  
2. It checks whether the file is a valid image type.  
3. It opens the image and runs it through `rembg.remove()`.  
4. It saves a new image in the **Output** directory named:

```
rmbg_<original_name>.png
```

5. It prints progress information to the console.

---

## Script Overview

```python
import os
from rembg import remove
from PIL import Image


def process_images(input_path: str, output_path: str) -> None:
    """
    Remove background from each image in the given directory and save as
    rmbg_<original_filename>.png.
    """

    # Normalize paths
    input_path = os.path.abspath(input_path)
    output_path = os.path.abspath(output_path)

    print(f"[INFO] Input directory:  {input_path}")
    print(f"[INFO] Output directory: {output_path}")

    if not os.path.isdir(input_path):
        raise NotADirectoryError(f"Input path is not a directory: {input_path}")

    os.makedirs(output_path, exist_ok=True)

    # Acceptable image extensions
    valid_exts = {".png", ".jpg", ".jpeg", ".webp"}

    count = 0
    for filename in os.listdir(input_path):
        name, ext = os.path.splitext(filename)

        if ext.lower() not in valid_exts:
            continue

        input_file = os.path.join(input_path, filename)
        output_file = os.path.join(output_path, f"rmbg_{name}.png")

        print(f"[INFO] Processing: {filename}")

        try:
            with Image.open(input_file) as inp:
                result = remove(inp)
                result.save(output_file)

            print(f"[OK] Saved: {output_file}")
            count += 1

        except Exception as e:
            print(f"[ERROR] Failed on {filename}: {e}")

    print(f"[DONE] Processed {count} image(s).")
```

---

## How to Use (End-User Instructions)

1. Place the images you want to process into the **Input** folder.  
2. Run `main.exe`.  
3. Wait while each image is processed.  
4. Open the **Output** folder to view the edited versions.  

You are free to delete or replace images in the Input folder at any time.

---

## Common Errors & Fixes

### **“Input path is not a directory”**
The program cannot find the `Input` folder.  
Make sure it exists in the same directory as the `.exe`.

---

### **“Failed on <filename>”**
The image may be:
- Corrupted  
- Zero bytes  
- A file type that cannot be opened  
- Locked by another program  

Try converting the image manually to PNG/JPG and try again.

---

### **No output files generated**
Check that the images are inside the **Input** folder and use one of the supported extensions.

---

## Converting to an Executable

If you plan to build the executable yourself:

```bash
pyinstaller --onefile main.py
```

Then copy the following into the distribution folder:

```
main.exe
README.md
Input/
Output/
```

---

## License & Permissions

This tool uses:

- **Rembg** (MIT License)  
- **ONNX Runtime** (MIT License)  
- **Pillow (PIL)**  

All required licenses allow packaging inside a commercial or private project.

---

## Support

If you need enhancements such as:

- GUI version  
- Drag-and-drop support  
- Progress bar interface  
- Auto-watch folder mode  
- GPU acceleration  

these can be added later—just ask.

---
