from fpdf import FPDF
from datetime import datetime


def create_invoice_pdf(INVOICE, DETAILS, FILEPATH):
    print(INVOICE)
    print(DETAILS)

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
    pdf.text(x=90, y=43, txt='TAX INVOICE')

    pdf.line(10, 48, 200, 48)

    pdf.line(10, 58, 200, 58)

    pdf.set_font('Arial', 'B', 9.0)
    number = '21'
    pdf.text(x=15, y=64, txt='Invoice Number: ')
    pdf.text(x=60, y=64, txt= str(INVOICE["invoice_no"]) )

    pdf.set_font('Arial', 'B', 9.0)
    date = '21/03/2021'
    pdf.text(x=15, y=72, txt='Invoice Date:')
    pdf.text(x=60, y=72, txt = str(INVOICE["invoice_date"].strftime("%d/%m/%Y")))

    pdf.set_font('Arial', 'B', 9.0)
    reverse_charges = 'Yes' if INVOICE["reverse_charges"] else "No"
    pdf.text(x=15, y=80, txt='Reverse Charges (Y/N): ')
    pdf.text(x=60, y=80, txt=str(reverse_charges))

    pdf.set_font('Arial', 'B', 9.0)
    state = INVOICE['state']
    pdf.text(x=15, y=88, txt='State: ')
    pdf.text(x=30, y=88, txt=str(state))

    pdf.set_font('Arial', 'B', 9.0)
    code = INVOICE['state_code']
    pdf.text(x=60, y=88, txt='Code: ')
    pdf.text(x=75, y=88, txt=str(code))

    # Vertical Line
    pdf.line(105, 48, 105, 93)

    '''
        Right side bill to party

    '''
    pdf.set_font('Arial', 'B', 9.0)
    pdf.text(x=143, y=54, txt='BILL TO PARTY')

    pdf.set_font('Arial', 'B', 9.0)
    number = '27'
    pdf.text(x=115, y=64, txt='Name: ')
    pdf.text(x=130, y=64, txt=str(INVOICE["name"]))

    pdf.set_font('Arial', 'B', 9.0)
    # date = '21/03/2021'
    pdf.text(x=115, y=70, txt='Address:')  # Address
    pdf.text(x = 130, y = 69, txt = INVOICE['address'])
    pdf.line(130, 70, 200, 70)
    pdf.line(115, 76, 200, 76)
    pdf.set_font('Arial', 'B', 9.0)
    gst_in = '27AADCB2230M1ZT'
    pdf.text(x=115, y=82, txt='GSTIN No: ')
    pdf.text(x=160, y=82, txt=str(INVOICE["gst"]))

    pdf.set_font('Arial', 'B', 9.0)
    state = 'Goa'
    pdf.text(x=115, y=88, txt='State: ')
    pdf.text(x=130, y=88, txt=str(INVOICE["state"]))

    pdf.set_font('Arial', 'B', 9.0)
    code = '487'
    pdf.text(x=160, y=88, txt='Code: ')
    pdf.text(x=175, y=88, txt=str(INVOICE["state_code"]))

    pdf.line(10, 93, 200, 93)

    '''
    Table
    '''

    deets_w = {'deet_no': 5.5,
               'name': 20,
               'hsn': 10,
               'qty': 9.5,
               'rate': 7,
               'mrp': 7,
               'total': 10,
               'discount': 10,
               'taxable_amt': 16}
    pdf.ln(88)

    pdf.set_font('Times', 'IB', 9.0)

    for ii in deets_w:
        pdf.cell(deets_w[ii] * 2, 6, str(ii).replace("_", " ").title(),
                    border=1, align='C', fill=False)
    pdf.ln(2)

    pdf.set_font('Arial', '', 9.0)
    for row in DETAILS:  # sets no. of rows
        pdf.ln(4)
        for field in deets_w:  # sets no. of cols
            pdf.cell(deets_w[field] * 2, 6, str(row[field]),
                border=1, align='C', fill=False)
        pdf.ln(2)

    '''
    Lower
    '''

    '''
    lower left
    '''

    rs = 'Twenty Ruppees only /-'
    pdf.text(x=10, y=230, txt='Rs. in words: ')
    pdf.text(x=30, y=230, txt=str(INVOICE["rupees_in_words"]))

    pdf.line(10, 235, 100, 235)

    label = 'AYURVEDIC PROP. MEDICINE '
    pdf.text(x=30, y=240, txt=label)

    pdf.line(10, 242, 100, 242)

    bank_name = 'Bank Of Baroda'
    pdf.text(x=10, y=250, txt='Bank Name: ')
    pdf.text(x=55, y=250, txt=str(INVOICE["bank_name"]))

    ac_no = '1234567897932XX'
    pdf.text(x=10, y=255, txt='Account Number: ')
    pdf.text(x=55, y=255, txt=str(INVOICE["account_no"]))

    ifsc_code = 'GSGS5425425454'
    pdf.text(x=10, y=260, txt='IFSC Code: ')
    pdf.text(x=55, y=260, txt=str(INVOICE["ifsc_code"]))

    pdf.line(10, 265, 100, 265)

    pdf.set_font('Times', 'IB', 9.0)
    notice = 'Goods once sold will not be taken back or replaced'
    pdf.text(x=20, y=270, txt=notice)

    '''
    Total tables
    '''

    pdf.line(105, 230, 105, 290)

    right_bottom_headers = [
        'total_before_tax', 'total_cgst', 'total_sgst',
        'total_igst', 'total_tax_amt', 'total_after_tax',
        'gst_reverse_charge'
    ]

    pdf.ln(3)
    for field in right_bottom_headers:
        pdf.ln(4)
        pdf.set_font('Times', 'IB', 9.0)
        pdf.cell(118)
        pdf.cell(18 * 2, 6, field.replace("_", " ").title(),
                 border=1, align='R', fill=False)
        pdf.set_font('Arial', '', 9.0)
        pdf.cell(18 * 2, 6, str(INVOICE[field]),
                 border=1, align='C', fill=False)
        pdf.ln(2)

    '''
    Signature Section
    '''
    pdf.line(110, 270, 195, 270)
    pdf.set_font('Times', 'IB', 9.0)
    sign_text = 'For Rajeshree Marketing'
    pdf.text(x=155, y=275, txt=sign_text)

    pdf.set_font('Times', 'B', 8.0)
    pdf.text(x=115, y=288, txt='E & O.E.')

    pdf.text(x=160, y=288, txt='Authorized Signature')

    pdf.line(10, 290, 200, 290)

    try:
        pdf.output(FILEPATH, 'F')
        print("Created.")
    except Exception as e:
        print(e)

if __name__ == '__main__':
    create_invoice_pdf()
