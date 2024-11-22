import os
import re
from PIL import Image

# Define folder paths and size percentages
BASE_DIR = "PNG"
SIZE_OPTIONS = {
    "extra-small": 0.02,  # 2% of original width
    "small": 0.1,         # 10% of original width
    "medium": 0.3,        # 30% of original width
    "large": 0.5          # 50% of original width
}
INDEX_HTML_PATH = "index.html"

def clean_filename(filename):
    """Remove any appended size dimensions from the filename."""
    return re.sub(r"_\d+w_\d+h", "", filename)

def rename_original_with_size(image_path):
    """Rename the original image to include its dimensions."""
    try:
        img = Image.open(image_path)
        original_width, original_height = img.size
        base_filename, ext = os.path.splitext(os.path.basename(image_path))
        # Clean the filename to avoid appending dimensions multiple times
        clean_base_filename = clean_filename(base_filename)
        new_filename = f"{clean_base_filename}_{original_width}w_{original_height}h{ext}"
        new_path = os.path.join(os.path.dirname(image_path), new_filename)
        os.rename(image_path, new_path)
        print(f"Renamed original image: {new_path}")
        return new_path
    except Exception as e:
        print(f"Error processing original image {image_path}: {e}")
        return image_path

def resize_and_save(image_path, output_dir, scale):
    """Resize the image to a percentage of its original width and save it with new dimensions in the filename."""
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        img = Image.open(image_path)
    except Exception as e:
        print(f"Error opening image {image_path}: {e}")
        return

    print(f"Processing: {image_path}")
    original_width, original_height = img.size
    if original_width == 0 or original_height == 0:
        print(f"Skipping {image_path}: Image has zero dimensions.")
        return

    new_width = max(int(original_width * scale), 1)
    new_height = max(int(original_height * scale), 1)
    print(f"New dimensions: {new_width}x{new_height}")

    try:
        img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        base_filename, ext = os.path.splitext(os.path.basename(image_path))
        # Clean the filename to avoid appending dimensions multiple times
        clean_base_filename = clean_filename(base_filename)
        resized_filename = f"{clean_base_filename}_{new_width}w_{new_height}h{ext}"
        output_path = os.path.join(output_dir, resized_filename)
        img_resized.save(output_path, format="PNG")
        print(f"Saved resized image: {output_path}")
    except Exception as e:
        print(f"Error resizing image {image_path}: {e}")

def generate_index_html(base_dir):
    """Generate the index.html file."""
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Amplemarket Brand Assets</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            background-color: #f9fafb;
            color: #111827;
        }
        header {
            padding: 2rem;
            text-align: center;
            background-color: #f6f5f3;
            border-bottom: 1px solid #e5e7eb;
        }
        header img {
            max-width: 300px;
            height: auto;
        }
        header h1 {
            margin: 1rem 0 0;
            font-size: 1.5rem;
            font-weight: 600;
            color: #374151;
        }
        main {
            max-width: 800px;
            margin: 2rem auto;
            padding: 0 1rem;
        }
        section {
            margin-bottom: 2rem;
        }
        section h2 {
            font-size: 1.25rem;
            font-weight: 500;
            margin-bottom: 1rem;
            color: #374151;
            border-bottom: 1px solid #e5e7eb;
            padding-bottom: 0.25rem;
        }
        ul {
            list-style: none;
            padding: 0;
        }
        ul li {
            margin: 0.5rem 0;
        }
        ul li.folder > a {
            font-weight: 600;
            color: #111827;
            cursor: pointer;
        }
        ul li.folder ul {
            display: none; /* Hide by default */
            margin-left: 1.5rem;
        }
        ul li.folder.open ul {
            display: block; /* Show when folder is open */
        }
        ul li.asset {
            margin-left: 1.5rem;
        }
        ul li.asset a {
            color: #2563eb;
            text-decoration: none;
        }
        ul li.asset a:hover {
            text-decoration: underline;
        }
    </style>
    <script>
        document.addEventListener('DOMContentLoaded', function () {
            document.querySelectorAll('li.folder > a').forEach(function (folderLink) {
                folderLink.addEventListener('click', function (e) {
                    e.preventDefault();
                    const folder = e.target.parentElement;
                    folder.classList.toggle('open');
                });
            });
        });
    </script>
</head>
<body>
    <header>
        <img src="SVG/amplemarket-full-black-combination-mark.svg" alt="Amplemarket Logo">
        <h1>Brand Assets</h1>
    </header>
    <main>
"""

    # Generate PNG section
    html_content += '<section>\n<h2>PNG</h2>\n<ul>\n'

    # List original files directly
    for file in sorted(os.listdir(base_dir)):
        file_path = os.path.join(base_dir, file)
        if os.path.isfile(file_path) and file.endswith(".png"):
            file_link = f"{base_dir}/{file}".replace("\\", "/")
            html_content += f'    <li class="asset"><a href="{file_link}">{file}</a></li>\n'

    # Add resized folders
    for size_name in ["extra-small", "small", "medium", "large"]:
        size_path = f"{base_dir}/{size_name}"
        if os.path.exists(size_path):
            html_content += f'    <li class="folder"><a href="#">{size_name}/</a>\n'
            html_content += "        <ul>\n"
            for file in sorted(os.listdir(size_path)):
                if file.endswith(".png"):
                    file_link = f"{size_path}/{file}".replace("\\", "/")
                    html_content += f'            <li class="asset"><a href="{file_link}">{file}</a></li>\n'
            html_content += "        </ul>\n"
            html_content += "    </li>\n"

    html_content += "</ul>\n</section>\n"

    # Generate SVG section
    svg_path = "SVG"
    if os.path.exists(svg_path):
        html_content += '<section>\n<h2>SVG</h2>\n<ul>\n'
        for file in sorted(os.listdir(svg_path)):
            if file.endswith(".svg"):
                file_link = f"{svg_path}/{file}".replace("\\", "/")
                html_content += f'    <li class="asset"><a href="{file_link}">{file}</a></li>\n'
        html_content += "</ul>\n</section>\n"

    html_content += "</main>\n</body>\n</html>"

    # Write to index.html
    with open(INDEX_HTML_PATH, "w") as f:
        f.write(html_content)

def main():
    # Ensure the base directory exists
    if not os.path.exists(BASE_DIR):
        print(f"Error: Base directory '{BASE_DIR}' not found.")
        return

    # Rename originals with dimensions
    renamed_files = []
    for file in os.listdir(BASE_DIR):
        file_path = os.path.join(BASE_DIR, file)
        if os.path.isfile(file_path) and file.endswith(".png"):
            renamed_file = rename_original_with_size(file_path)
            renamed_files.append(renamed_file)

    # Process resized images
    for file_path in renamed_files:
        for size_name, scale in SIZE_OPTIONS.items():
            output_dir = os.path.join(BASE_DIR, size_name)
            resize_and_save(file_path, output_dir, scale)

    # Generate the index.html file
    generate_index_html(BASE_DIR)
    print(f"Resizing complete and {INDEX_HTML_PATH} updated!")

if __name__ == "__main__":
    main()