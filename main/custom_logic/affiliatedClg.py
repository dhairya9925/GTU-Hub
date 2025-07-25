import os
import pdfplumber
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import shutil


download_dir = os.path.join(os.path.dirname(__file__), "affiliated_college_lists")


def get_colleges():
    try:
        download_affiliated_college_list()    
        process_college_pdf()
    except Exception as e:
        print(f"Exception occured during WHile getting or Processing the Pdf.\n\n{e}")
    


# DOWNLOAD PDF OF AFFILIATED COLLEGE OF DIFFERENT COURSES
def download_affiliated_college_list():
    # Set download directory
    print(f"Download Dir = {download_dir}")
    if os.listdir(download_dir):
        return

    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "plugins.always_open_pdf_externally": True,  # Don't open PDF in browser
        "download.prompt_for_download": False,
        "download.directory_upgrade": True
    })

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.gtu.ac.in/AffiliatedColleges.aspx")

    time.sleep(2)
    blocks = driver.find_elements(By.CLASS_NAME, "d-block")
    
    links = blocks[1].find_elements(By.XPATH, "./a[@target='_blank']")

    for link in links:
        link.click()
        time.sleep(2)

    print(f"Length: {len(blocks)}")
    print(f"Length: {len(links)}")
    driver.quit()



def extract_pdf_table(pdf_path, excel_path, file_name):
    all_rows = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    # Ignore empty or too-short rows
                    if row and any(cell and cell.strip() for cell in row):
                        all_rows.append(row)

    if not all_rows:
        print(f"⚠️ No valid rows found in: {file_name}")
        return

    # Normalize rows to the length of the longest row
    max_cols = max(len(r) for r in all_rows)
    normalized_rows = [r + [''] * (max_cols - len(r)) for r in all_rows]

    df = pd.DataFrame(normalized_rows)

    # Save to Excel
    df.to_excel(excel_path, index=False, header=False)
    # print(f"✅ Saved: {excel_path}")


def process_college_pdf():
    files = os.listdir(download_dir)
    print(f"\nCurrent path: {download_dir}\n")
    error_in = []

    # Ensure output directory exists and is a folder
    output_dir = f"{download_dir}/outputs"
    if os.path.exists(output_dir) and not os.path.isdir(output_dir):
        print(f"Error: '{output_dir}' exists and is not a directory. Please delete or rename it.")
        return
    elif not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if os.listdir(output_dir):
        print(f"'{output_dir}' is not Empty.")
        return

    # Process each PDF file
    for index, file in enumerate(files):
        try:
            if not file.lower().endswith(".pdf"):
                continue

            file_path = os.path.join(download_dir, file)

            # Generate output Excel file path
            excel_file_name = os.path.splitext(file)[0] + ".xlsx"
            excel_output_path = os.path.join(os.path.abspath(output_dir), excel_file_name)

            # Convert PDF to Excel using pdfplumber
            extract_pdf_table(file_path, excel_output_path, file)

            print(f"{index + 1}. {file}")
        except Exception as e:
            print(f"\n❌ Exception in file: {file}\n   {e}\n")
            error_in.append(file)

    if error_in:
        print("\nErrors occurred in the following files:")
        for f in error_in:
            print(f" - {f}")
    else:
        print("\n✅ All files processed successfully.")


if __name__ == "__main__":
    process_college_pdf()