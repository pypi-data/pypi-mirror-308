import glob
import pandas as pd
import os 
from fpdf import FPDF
from pathlib import Path

def generate(source_path: str, dest_path: str, image_path: str, product_id: str, product_name: str,
             amount_purchased: str, price_per_unit: str, total_price: str) -> None:
    """
    This function converts Excel files with inoice information into PDF invoices.

    :param source_path: path to the folder containing the excel files (without the trailing slash)
    :param dest_path: path to the folder where the pdf files will be saved (without the trailing slash)
    :param image_path: path to the image file that will be added to the pdf
    :param product_id: column name in Excel files containing the product id
    :param product_name: column name in Excel files containing the product name
    :param amount_purchased: column name in Excel files containing the amount purchased
    :param price_per_unit: column name in Excel files containing the price per unit
    :param total_price: column name in Excel files containing the total price
    """
    filepaths = glob.glob(f"{source_path}/*.xlsx")
    for filepath in filepaths:
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        filename = Path(filepath).stem
        invoice_nr, date = filename.split("-")

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Invoice nr.{invoice_nr}", ln=1)

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Date: {date}", ln=1)

        df = pd.read_excel(filepath, sheet_name="Sheet 1")

        # Add a header
        columns = df.columns
        columns = [item.replace("_", " ").title() for item in columns]
        pdf.set_font(family="Times", size=10, style="B")
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt=columns[0], border=1)
        pdf.cell(w=70, h=8, txt=columns[1], border=1)
        pdf.cell(w=30, h=8, txt=columns[2], border=1)
        pdf.cell(w=30, h=8, txt=columns[3], border=1)
        pdf.cell(w=30, h=8, txt=columns[4], border=1, ln=1)

        # Add rows to the table
        for index, row in df.iterrows():
            pdf.set_font(family="Times", size=10)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(w=30, h=8, txt=str(row[product_id]), border=1)
            pdf.cell(w=70, h=8, txt=str(row[product_name]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[amount_purchased]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[price_per_unit]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[total_price]), border=1, ln=1)

        total_sum = df["total_price"].sum()
        pdf.set_font(family="Times", size=10)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=70, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt=str(total_sum), border=1, ln=1)

        # Add total sum sentence
        pdf.set_font(family="Times", size=10, style="B")
        pdf.cell(w=30, h=8, txt=f"The total price is {total_sum}", ln=1)

        # Add company name and logo
        pdf.set_font(family="Times", size=14, style="B")
        pdf.cell(w=25, h=8, txt=f"PythonHow")
        pdf.image(image_path, w=10)


        os.makedirs(dest_path, exist_ok=True)
        pdf.output(f"{dest_path}/{filename}.pdf")

if __name__ == "__main__":
    generate("invoices", "PDFs", "./pythonhow.png", "product_id", "product_name",
             "amount_purchased", "price_per_unit", "total_price")
