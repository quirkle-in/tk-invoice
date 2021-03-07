from sqlalchemy.dialects.mysql import Float
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from setup import SessionLocal, Base
import datetime

db = SessionLocal()


class Invoice(Base):

    __tablename__ = "invoice"

    id = Column(Integer, index=True)
    invoice_id = Column(Integer, primary_key=True, index=True)
    invoice_date = Column(DateTime, default=datetime.datetime.now())
    party_name = Column(String, nullable=False)
    party_address = Column(String(200), default='')
    party_gst = Column(String, default=0)
    party_state = Column(String(25), default='')
    party_state_code = Column(Integer, default=0)
    total = Column(Float, default=0)
    total_cgst = Column(Float, default=0)
    total_sgst = Column(Float, default=0)
    purchase = Column(Boolean, default=True)


class Details(Base):

    __tablename__ = "details"

    id = Column(Integer, index=True, primary_key=True)
    invoice_id = Column(Integer, ForeignKey('invoice.invoice_id'))
    name = Column(String(100))
    hsn = Column(Integer)
    qty = Column(Integer)
    rate = Column(Float)
    mrp = Colummn(Float)
    total = Column(Integer)
    discount = Column(Float)
    tax_value = Column(Float)


db.create_all()


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
        inv = Invoice(invoice_date=invoice_date, party_name=party_name, party_address=party_address, party_gst=party_gst,
                      party_state_code=party_state_code, total=total, total_cgst=total_cgst, total_sgst=total_sgst, purchase=purchase)
        db.session.add(inv)
        db.session.commit()
        return inv.invoice_id
    except Exception as e:
        print(e)
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
        det = Details(invoice_id=invoice_id, name=name, hsn=hsn, qty=qty, rate=rate,
                      mrp=mrp, total=total, discount=discount, tax_value=tax_value)
        db.session.add(det)
        db.session.commit()
        return det.id
    except Exception as e:
        print(e)
        return False
