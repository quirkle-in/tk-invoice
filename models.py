from enum import unique
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime

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
    name = Column(String(100), nullable=False)
    address = Column(String(200), default='')
    gst = Column(String(200), default=0)
    state = Column(String(25), default='')
    state_code = Column(Integer, default=0)
    total = Column(Float, default=0)
    total_cgst = Column(Float, default=0)
    total_sgst = Column(Float, default=0)
    purchase = Column(Boolean, default=True)
    reverse_charges = Column(Boolean, default = False)

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
    
class GSTValues(Base):
    __tablename__ = 'gstValues'

    cgst = Column(Float, nullable=False, primary_key=True)
    sgct = Column(Float, nullable=False)
    igst = Column(Float, nullable=False)
    


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


def createInvoice(
        invoice_date,
        name,
        address,
        gst,
        state,
        state_code,
        total,
        total_cgst,
        total_sgst,
        purchase,
        invoice_no,
        reverse_charges):
    try:
        inv = Invoice(
            invoice_no=invoice_no, invoice_date=invoice_date,
            name=name, address=address,
            state=state,
            state_code=state_code, total=total,
            total_cgst=total_cgst, total_sgst=total_sgst,
            purchase=purchase, reverse_charges = reverse_charges)
        db.add(inv)
        db.commit()
        # print(inv)
        return inv.invoice_id
    except Exception as e:
        print(e)
        db.rollback()
        return False


def createDetails(deet_no,
                invoice_id,
                  name,
                  hsn,
                  qty,
                  batch,
                  rate,
                  mrp,
                  total,
                  discount,
                  taxable_amt):
    try:
        det = Details(
            deet_no = deet_no, batch = batch,
            invoice_id=invoice_id, name=name, hsn=hsn,
            qty=qty, rate=rate, mrp=mrp, total=total,
            discount=discount, taxable_amt=taxable_amt
        )
        db.add(det)
        db.commit()
        print('Goods Details inserted')
        return det.deet_id
    except Exception as e:
        print(e)
        db.rollback()
        return False


def get_all_invoices():
    return db.query(Invoice).all()


def get_all_details():
    return db.query(Details).all()

def get_all_entities():
    return db.query(Entity).all()

def get_all_entity_names():
    return db.query(Entity).with_entities(Entity.name).all()

def get_entity_by_name(name):
    return db.query(Entity).filter_by(name = name).first()


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

    
def create_entity(
        name, address, gstin_uid,
        state, state_code, bank_name,
        a_c_no, ifc_code):
    E = Entity(
        name = name, address = address, gstin_uid = gstin_uid, 
        state = state, state_code = state_code, 
        bank_name = bank_name, a_c_no = a_c_no, ifc_code = ifc_code
    )

    try:
        db.add(E)
        db.commit()
        print('Added entity')
        return E.entity_id
    except Exception as e:
        print(e)
        db.rollback()
        return False

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