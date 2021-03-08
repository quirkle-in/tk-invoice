from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.dialects.mysql import FLOAT 

import os
from dotenv import load_dotenv
from sqlalchemy.sql.sqltypes import Date
load_dotenv()

engine = create_engine(os.getenv("SQLITE_URL"), echo = False)
#engine

from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
import datetime

db = SessionLocal()


class Invoice(Base):

    __tablename__ = "invoice"

    invoice_id = Column(Integer, primary_key=True, index = True,  autoincrement=True) 
    invoice_no = Column(Integer, unique = True, autoincrement=True) 
    invoice_date = Column(DateTime, default=datetime.datetime.now()), 
    party_name = Column(String(100), nullable=False)
    party_address = Column(String(200), default='')
    party_gst = Column(String(200), default=0)
    party_state = Column(String(25), default='')
    party_state_code = Column(Integer, default=0)
    total = Column(FLOAT, default=0)
    total_cgst = Column(FLOAT, default=0)
    total_sgst = Column(FLOAT, default=0)
    purchase = Column(Boolean, default=True)


class Details(Base):

    __tablename__ = "details"

    deet_id = Column(Integer, index=True, primary_key=True)
    invoice_id = Column(Integer, ForeignKey(Invoice.invoice_id))
    name = Column(String(100))
    hsn = Column(Integer)
    qty = Column(Integer)
    rate = Column(FLOAT)
    mrp = Column(FLOAT)
    total = Column(Integer)
    discount = Column(FLOAT)
    tax_value = Column(FLOAT)


def get_last_invoice():
    x = db.query(Invoice).order_by(
        Invoice.invoice_id.desc()
    ).first()
    if not x: x = 1
    return x.invoice_no + 1

def get_last_invoice():
    x = db.query(Invoice).order_by(
        Invoice.invoice_id.desc()
    ).first()
    if not x: return 1
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
            invoice_no=invoice_no,invoice_date=invoice_date,
            party_name=party_name, party_address=party_address,
            party_gst=party_gst, party_state=party_state, 
            party_state_code=party_state_code, total=total, 
            total_cgst=total_cgst, total_sgst=total_sgst, 
            purchase=purchase)
        db.add(inv)
        db.commit()
        #print(inv)
        return inv.invoice_id
    except Exception as e:
        print(e)
        db.rollback()
        return False


def createDetails(invoice_id,
                  name,
                  hsn,
                  qty,
                  rate,
                  mrp,
                  total,
                  discount,
                  tax_value):
    try:
        det = Details(
            invoice_id=invoice_id, name=name, hsn=hsn, 
            qty=qty, rate=rate, mrp=mrp, total=total, 
            discount=discount, tax_value=tax_value
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