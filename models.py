from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.dialects.mysql import FLOAT 

import os
from dotenv import load_dotenv
load_dotenv()

engine = create_engine(os.getenv("MYSQL_DB_URL"), echo = False)
engine

from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
import datetime

db = SessionLocal()


class Invoice(Base):

    __tablename__ = "invoice"

    #id = Column(Integer, primary_key=True, index=True) #YU{P}#you werent passing any value to this, shouldn't it be set on its own? then why youput auto incrmenet
    invoice_id = Column(Integer, primary_key=True, index = True,  autoincrement=True) 
    invoice_date = Column(DateTime, default=datetime.datetime.now()), #so it sets and increases it on its own duh ca have multiple primary keys tho
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



def createInvoice(invoice_date,
                  party_name,
                  party_address,
                  party_gst,
                  party_state,
                  party_state_code,
                  total,
                  total_cgst,
                  total_sgst,
                  purchase):
    try:
        inv = Invoice(
            invoice_date=invoice_date, party_name=party_name, 
            party_address=party_address, party_gst=party_gst, 
            party_state=party_state, party_state_code=party_state_code, 
            total=total, total_cgst=total_cgst, total_sgst=total_sgst, 
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