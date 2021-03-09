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
        party_name,
        party_address,
        party_gst,
        party_state,
        party_state_code,
        total,
        total_cgst,
        total_sgst,
        purchase,
        invoice_no):
    try:
        inv = Invoice(
            invoice_no=invoice_no, invoice_date=invoice_date,
            party_name=party_name, party_address=party_address,
            party_gst=party_gst, party_state=party_state,
            party_state_code=party_state_code, total=total,
            total_cgst=total_cgst, total_sgst=total_sgst,
            purchase=purchase)
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
                  rate,
                  mrp,
                  total,
                  discount,
                  taxable_amount):
    try:
        det = Details(
            deet_no = deet_no,
            invoice_id=invoice_id, name=name, hsn=hsn,
            qty=qty, rate=rate, mrp=mrp, total=total,
            discount=discount, taxable_amount=taxable_amount
        )
        db.add(det)
        db.commit()
        print('commited deets')
        return det.deet_id
    except Exception as e:
        print(e)
        db.rollback()
        return False


def get_all_invoices():
    return db.query(Invoice).all()

def get_all_details():
    return db.query(Details).all()
