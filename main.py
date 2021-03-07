from models import Base, engine

if not engine.dialect.has_table(engine, 'Invoice'):
    print('Creating tables')
    Base.metadata.create_all(bind = engine) 
else:
    print('Table Exists')

from models import createInvoice, createDetails

resp = createInvoice(
    invoice_date = '2021-03-07',
    party_name = 'First Party',
    party_address = 'Jaisalllllllll Apartments New, Mumbai 40006.',
    party_gst = 'ABC1234QWERTY',
    party_state = 'LIQUID',
    party_state_code = '12084',
    total = 19847.98,
    total_cgst = 347.33,
    total_sgst = 342.1,
    purchase = True
)

print('resp: ', resp)

resp_det = createDetails(
    invoice_id = resp,
    name = 'Jaisal Bhai Shah',
    hsn = 789,
    qty = 700,
    rate = 2.2,
    mrp =  0.1,
    total = 23,
    discount = 90.2,
    tax_value = 23847.3
)

print('resop_det',resp_det)