from fpdf import FPDF

def purchase_report(DETAILS):
    
    pdf = FPDF('P', 'mm', 'A4')

    # Add new page. Without this you cannot create the document.
    pdf.add_page()

    pdf.set_font('Arial', 'B', 14.0)

    x, y = 140, 15

    pdf.text(x=80, y=y, txt='Rajeshree Marketing')
    pdf.ln(2)

    pdf.set_font('Arial', '', 10.0)
    pdf.text(
        x=50, y=22, txt='1/16, Vijay Nagar, Bandrekarwadi Jogeshwari, (East), Mumbai - 400 060.')

    pdf.set_font('Arial', 'B', 10.0)
    pdf.text(x=78, y=30, txt='GST No. :    27AKEPB0058K1ZE')

    pdf.line(10, 35, 200, 35)

    pdf.set_font('Arial', 'B', 12.0)
    pdf.text(x=85, y=43, txt=DETAILS['name'])

    pdf.line(10, 48, 200, 48)

    deets_w = {'Sr No': 5.5,
               'name': 20,
               'hsn': 10,
               'qty': 9.5,
               'rate': 7,
               'mrp': 7,
               'total': 10,
               'discount': 10,
               'taxable_amt': 16}
    pdf.ln(40)

    pdf.set_font('Times', 'IB', 9.0)

    for ii in deets_w:
        pdf.cell(deets_w[ii] * 2, 6, str(ii).replace("_", " ").title(),
                    border=1, align='C', fill=False)
    pdf.ln(2)

    pdf.set_font('Arial', '', 9.0)
    for row in [0 ,1, 2]:  # sets no. of rows
        pdf.ln(4)
        for field in deets_w:  # sets no. of cols
            pdf.cell(deets_w[field] * 2, 6, str(row),
                border=1, align='C', fill=False)
        pdf.ln(2)


    try:
        pdf.output('pur.pdf', 'F')
        print("Created.")
    except Exception as e:
        print(e)

DETAILS = {
    'name': 'PURCHASE REPORT'
}

if __name__ == '__main__':
    purchase_report(DETAILS)