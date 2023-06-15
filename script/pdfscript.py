import os
import tabula
import pytesseract
from PIL import Image
import pandas as pd

# Set the Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_key_value_pairs(pdf_path):
    # Read the PDF and extract tabular data
    df_list = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
    
    if df_list:
        # Extract header data
        header_df = df_list[0]
        header_columns = header_df.columns.tolist()
        header_df = header_df.dropna().reset_index(drop=True)
        
        # Save header data to CSV
        header_df.to_csv('header_data.csv', index=False)
        
        # Extract tabular data
        table_dfs = df_list[1:]
        
        # Save tabular data to CSV
        for i, table_df in enumerate(table_dfs):
            table_columns = table_df.columns.tolist()
            table_df.columns = table_columns
            
            table_df.to_csv(f'tabular_data_{i}.csv', index=False)
    else:
        print("No tabular data found in the PDF.")


def extract_tabular_data(image_path):
    # Preprocess the image
    img = Image.open(image_path)
    img = img.convert('L')  # Convert to grayscale
    img = img.point(lambda x: 0 if x < 150 else 255, '1')  # Binarize the image
    
    # Perform OCR on the preprocessed image
    ocr_text = pytesseract.image_to_string(img, config='--psm 6')
    
    # Parse the OCR text and extract tabular data
    rows = [row.split('\t') for row in ocr_text.split('\n')]
    table_data = pd.DataFrame(rows[1:], columns=rows[0])
    
    return table_data


def extract_data(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.pdf':
        # Handle PDF file
        extract_key_value_pairs(file_path)
    elif file_extension == '.jpeg' or file_extension == '.jpg':
        # Handle JPEG file
        table_data = extract_tabular_data(file_path)
        table_data.to_csv('tabular_data.csv', index=False)
    else:
        # Unsupported file type
        print(f"Unsupported file type: {file_extension}")


# Specify the path to the file (PDF or JPEG)
file_path = 'sample2.jpg'

# Call the function to extract key-value pairs and tabular data
extract_data(file_path)
