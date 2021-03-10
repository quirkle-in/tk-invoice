from fpdf import FPDF
from datetime import datetime
# DETAILS = {
#     'name': 'PURCHASE REPORT',
#     'dets': [{'Sr No': 1, 'name': 'kvvg', 'hsn': 25, 'qty': 1351, 'rate': 3525421.0, 'mrp': 53.0, 'total': 474201, 'discount': 3215.0, 'taxable_amt': 470986.0}, {'Sr No': 2, 'name': 'sdjlblgds', 'hsn': 254, 'qty': 52, 'rate': 54.0, 'mrp': 54.0, 'total': 2808, 'discount': 54.0, 'taxable_amt': 2754.0}, {'Sr No': 3, 'name': 'kvugu', 'hsn': 25, 'qty': 54, 'rate': 534346.0, 'mrp': 46346.0, 'total': 28854684, 'discount': 634.0, 'taxable_amt': 28854050.0},
#              {'Sr No': 4, 'name': ',jhyf,j', 'hsn': 'lkib', 'qty': 354, 'rate': 354.0, 'mrp': 354.0, 'total': 125316, 'discount': 354.0, 'taxable_amt': 124962.0}]
# }


def purchase_report(DETAILS):

    FILENAME = DETAILS['name'] + '_' + \
        datetime.now().strftime('%d-%m-%Y_') + ".pdf"

    pdf = FPDF('P', 'mm', 'A4')

    # Add new page. Without this you cannot create the document.
    pdf.add_page()

    pdf.set_font('Arial', 'B', 14.0)

    x, y = 140, 15

    pdf.text(x=80, y=y, txt='Rajeshree Marketing')
    pdf.ln(2)

    pdf.set_font('Arial', '', 10.0)
    pdf.text(
        x=50, y=22, txt='1/16, Vijay Nagar, Bandrekarwadi Jogeshwari (East), Mumbai - 400 060.')

    pdf.set_font('Arial', 'B', 10.0)
    pdf.text(x=78, y=30, txt='GST No. :    27AKEPB0058K1ZE')

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
