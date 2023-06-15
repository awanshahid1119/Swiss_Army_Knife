import os
import tabula
import pytesseract
from PIL import Image
import pandas as pd

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_key_value_pairs(pdf_path):
    df_list = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
    if df_list:
        header_df = df_list[0]
        header_columns = header_df.columns.tolist()
        header_df = header_df.dropna().reset_index(drop=True)
        header_df.to_csv('header_data.csv', index=False)
        table_dfs = df_list[1:]
        for i, table_df in enumerate(table_dfs):
            table_columns = table_df.columns.tolist()
            table_df.columns = table_columns
            table_df.to_csv(f'tabular_data_{i}.csv', index=False)
    else:
        print("No tabular data found in the PDF.")

def extract_tabular_data(image_path):
    img = Image.open(image_path)
    img = img.convert('L')
    img = img.point(lambda x: 0 if x < 150 else 255, '1')
    ocr_text = pytesseract.image_to_string(img, config='--psm 6')
    rows = [row.split('\t') for row in ocr_text.split('\n')]
    table_data = pd.DataFrame(rows[1:], columns=rows[0])
    return table_data
