from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

import os
from dotenv import load_dotenv
load_dotenv()


engine = create_engine(os.getenv("SQLITE_URL"), echo=False)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
db = SessionLocal()

class Invoice(Base):

    __tablename__ = "invoice"

    invoice_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    invoice_no = Column(Integer, unique=True, autoincrement=True)
    invoice_date = Column(Date, nullable=False)
    reverse_charges = Column(Boolean, default = False)
    state = Column(String(100), default='')
    state_code = Column(Integer, default=0)
    
    name = Column(String(100), nullable=False)
    address = Column(String(200), default='')
    gst = Column(String(200), default=0)
    party_state = Column(String(100), default='')
    party_code = Column(Integer, default=0)

    purchase = Column(Boolean, default=True)
    rupees_in_words = Column(String(100))
    bank_name = Column(String(100))
    account_no = Column(String(100))
    ifsc = Column(String(100))
    
    total_before_tax = Column(Float, default = 0.00)
    total_igst = Column(Float, default = 0.00)
    total_cgst = Column(Float, default=0)
    total_sgst = Column(Float, default=0)
    total_tax_amt = Column(Float, default = 0.00)
    total_after_tax = Column(Float, default = 0.00)
    gst_reverse_charge = Column(String(100))



class Details(Base):

    __tablename__ = "details"

    deet_id = Column(Integer, index=True, primary_key=True)
    deet_no = Column(Integer)
    invoice_id = Column(Integer, ForeignKey(Invoice.invoice_id))
    name = Column(String(100))
    batch = Column(String(100), nullable=False)
    hsn = Column(Integer)
    qty = Column(Integer)
    rate = Column(Float)
    mrp = Column(Float)
    total = Column(Integer)
    discount = Column(Float)
    taxable_amt = Column(Float)


class Entity(Base):

    __tablename__ = "entity"

    entity_id = Column(Integer, index = True, primary_key = True)
    name = Column(String(100), unique = True)
    address = Column(String(200))
    gstin_uid = Column(String(100))
    state = Column(String(100))
    state_code = Column(String(100))
    bank_name = Column(String(100))
    a_c_no = Column(String(100))
    ifc_code = Column(String(100))
    

''' INVOICE FUNTIONS '''


def get_all_invoices():
    return db.query(Invoice).all()


def get_last_invoice():
    x = db.query(Invoice).order_by(
        Invoice.invoice_id.desc()
    ).first()
    if not x:
        x = 1
    return x.invoice_no + 1


def get_last_invoice():
    x = db.query(Invoice).order_by(
        Invoice.invoice_id.desc()
    ).first()
    if not x:
        return 1
    return x.invoice_no + 1


def createInvoice(invoice_data):
    try:
        inv = Invoice(**invoice_data)
        db.add(inv)
        db.commit()
        return inv.invoice_id
    except Exception as e:
        print(e)
        db.rollback()
        return False


''' DETAILS FUNCTIONS '''

def get_all_details():
    return db.query(Details).all()


def createDetails(detail_data):
    try:
        det = Details(**detail_data)
        db.add(det)
        db.commit()
        print('Goods Details inserted')
        return det.deet_id
    except Exception as e:
        print(e)
        db.rollback()
        return False


''' ENTITY FUNCTIONS '''

def get_all_entities():
    return db.query(Entity).all()


def get_all_entity_names():
    return db.query(Entity).with_entities(Entity.name).all()


def get_entity_by_name(name):
    return db.query(Entity).filter_by(name = name).first()


def create_entity(data):
    E = Entity(**data)
    try:
        db.add(E)
        db.commit()
        print('Added entity')
        return E.entity_id
    except Exception as e:
        print(e)
        db.rollback()
        return False


''' EXTRAS '''


def filtered_view(table, type):
    res = None
    if table == "Invoices":
        res = db.query(Invoice)     

        if type == "Purchases": x = [1]
        elif type == "Sales": x = [0]
        else: x = [1, 0]

        res = res.filter(Invoice.purchase.in_(x))

    elif table == "Details":
        res = db.query(Details)
    
    elif table == "Entities":
        res = db.query(Entity)

    if not res:
        return []
    return res.all()


def get_table_row(table, _id):
    if table == "Invoices":
        x = Invoice
        res = db.query(x).filter_by(invoice_id = _id).first()
        print(res.name)
    elif table == "Details":
        x = Details
        res = db.query(x).filter_by(deet_id = _id).first()
        print(res)
    elif table == "Entities":
        x = Entity
        res = db.query(x).filter_by(entity_id = _id).first()    
    return res


def delete_table_row(table, _id):
    if table == "Invoices":
        x = Invoice
        res = db.query(x).filter_by(invoice_id = _id).first()
    elif table == "Details":
        x = Details
        res = db.query(x).filter_by(deet_id = _id).first()
    elif table == "Entities":
        x = Entity
        res = db.query(x).filter_by(entity_id = _id).first()    

    try:
        db.delete(res)
        db.commit()
        return True
    except:
        return False


def get_invoice_by_id(_id):
    details = None
    invoice = db.query(Invoice).filter_by(invoice_id = _id).first()
    if invoice:
        details = db.query(Details).filter_by(
            invoice_id = invoice.invoice_id
        ).all()
        if details != None:
            return invoice, details
    return None, None


def purchase_report():
    details = []
    data = db.query(Invoice).filter_by(purchase = True).all()
    s_no = 1
    for x in data:
        detail_data = db.query(Details).filter_by(invoice_id = x.invoice_id).all()
        for y in detail_data:
            details_dict = {'Sr No': s_no,
               'name': y.name,
               'hsn': y.hsn,
               'qty': y.qty,
               'rate': y.rate,
               'mrp': y.mrp,
               'total': y.total,
               'discount': y.discount,
               'taxable_amt': y.taxable_amt}
            details.append(details_dict)
            s_no += 1
    return (details)   


def sales_report():
    details = []
    data = db.query(Invoice).filter_by(purchase = False).all()
    s_no = 1
    for x in data:
        detail_data = db.query(Details).filter_by(invoice_id = x.invoice_id).all()
        for y in detail_data:
            details_dict = {
                'Sr No': s_no,
               'name': y.name,
               'hsn': y.hsn,
               'qty': y.qty,
               'rate': y.rate,
               'mrp': y.mrp,
               'total': y.total,
               'discount': y.discount,
               'taxable_amt': y.taxable_amt}
            details.append(details_dict)
            s_no += 1
    return (details)   
