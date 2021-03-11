from fpdf import FPDF
from datetime import datetime


def purchase_report(DETAILS, SETTINGS):

    FILENAME = f"{DETAILS['name']}_{DETAILS['start_date']}_{DETAILS['end_date']}.pdf"

    pdf = FPDF('P', 'mm', 'A4')

    # Add new page. Without this you cannot create the document.
    pdf.add_page()

    pdf.set_font('Arial', 'B', 14.0)

    x, y = 140, 15

    pdf.text(x=80, y=y, txt=str(SETTINGS["pdf_title"]))
    pdf.ln(2)

    pdf.set_font('Arial', '', 10.0)
    pdf.text(
        x=50, y=22, txt=str(SETTINGS["pdf_address"]))

    pdf.set_font('Arial', 'B', 10.0)
    pdf.text(x=78, y=30, txt=f'GST No. : {SETTINGS["pdf_gst_no"]}')

    pdf.line(10, 35, 200, 35)

    pdf.set_font('Arial', 'B', 12.0)
    pdf.text(x=85, y=43, txt=DETAILS['name'])

    pdf.line(10, 48, 200, 48)

    deets_w = {'Sr No': 5.5,
               'name': 20,
               'hsn': 10,
               'qty': 7.5,
               'rate': 9,
               'mrp': 7,
               'total': 10,
               'discount': 10,
               'taxable_amt': 16}
    pdf.ln(40)

    pdf.set_font('Arial', "", 9)
    if DETAILS["start_date"] == "All":
        pdf.cell(100, 6, "From: Start")
    else:
        pdf.cell(100, 6, "From: " + DETAILS["start_date"])
    pdf.ln(6)
    if DETAILS["end_date"] == "All":
        pdf.cell(100, 6, "To: Now")
    else:
        pdf.cell(100, 6, "To: " + DETAILS["end_date"])
    pdf.ln(10)

    pdf.set_font('Times', 'IB', 9.0)

    for ii in deets_w:
        pdf.cell(deets_w[ii] * 2, 6, str(ii).replace("_", " ").title(),
                 border=1, align='C', fill=False)
    pdf.ln(2)

    pdf.set_font('Arial', '', 9.0)

    for row in DETAILS['dets']:  # sets no. of rows
        pdf.ln(4)
        print(row)
        for field in deets_w:  # sets no. of cols
            pdf.cell(deets_w[field] * 2, 6, str(row[field]),
                     border=1, align='C', fill=False)
        pdf.ln(2)

    try:
        pdf.output(DETAILS['path'] + "/" + FILENAME, 'F')
        print("Created.")
        return True
    except Exception as e:
        print(e)
        return False
