import os
import zipfile

from bs4 import BeautifulSoup


def clean_epub_paragraphs(input_epub, output_epub):
    # Check if input file exists
    if not os.path.exists(input_epub):
        print(f"Error: Could not find {input_epub}")
        return

    print(f"Opening {input_epub} for cleaning...")

    # Open the original EPUB for reading and a new EPUB for writing
    with zipfile.ZipFile(input_epub, "r") as zin:
        with zipfile.ZipFile(output_epub, "w", zipfile.ZIP_DEFLATED) as zout:

            # Iterate through every file inside the EPUB archive
            for item in zin.infolist():
                # Read the file's raw bytes
                content = zin.read(item.filename)

                # Check if the file is an HTML or XHTML document
                if item.filename.lower().endswith((".html", ".xhtml", ".htm")):
                    # Parse the HTML content
                    soup = BeautifulSoup(content, "html.parser")

                    # Track how many paragraphs are removed in this specific file
                    removed_count = 0

                    for p in soup.find_all("p"):
                        text = p.get_text()

                        # Check if the paragraph is empty or only contains spaces/non-breaking spaces
                        if not text.strip(" \t\n\r\xa0"):
                            p.decompose()
                            removed_count += 1

                    if removed_count > 0:
                        print(
                            f"  - Removed {removed_count} empty paragraphs from {item.filename}"
                        )

                    # Convert the cleaned HTML back to bytes
                    cleaned_content = str(soup).encode("utf-8")

                    # Write the cleaned HTML to the new EPUB
                    zout.writestr(item, cleaned_content)
                else:
                    # If it's not an HTML file (e.g., an image, CSS, or metadata), copy it over untouched
                    zout.writestr(item, content)

    print(f"\nSuccess! Cleaned EPUB saved as: {output_epub}")


# --- How to use the script ---
if __name__ == "__main__":
    # Change these filenames to match your files
    INPUT_FILE = "Milan, Cameron - Towers Of Heaven 01 (2019).epub"
    OUTPUT_FILE = "my_book_cleaned.epub"

    clean_epub_paragraphs(INPUT_FILE, OUTPUT_FILE)
