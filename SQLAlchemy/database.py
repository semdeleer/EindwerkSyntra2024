from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Company(Base):
    __tablename__ = "company"
    companynr = Column(Integer, primary_key=True)
    companyname = Column(Text)
    adress = Column(Text)
    postalcode = Column(String)
    location = Column(Text)
    country = Column(String)

class Articles(Base):
    __tablename__ = "articles"
    articlenr = Column(Integer, primary_key=True)
    producttype = Column(Text)
    design = Column(Text)
    companyname = Column(Text)
    size = Column(Text)
    quantity = Column(Integer, default=0)

class Designs(Base):
    __tablename__ = "designs"
    designnr = Column(Integer, primary_key=True)
    designname = Column(Text)

class ProductType(Base):
    __tablename__ = "producttype"
    typenr = Column(Integer, primary_key=True)
    typename = Column(Text)

class ReleaseYear(Base):
    __tablename__ = "releaseyear"
    releaseyear = Column(Integer, primary_key=True)

class Sizes(Base):
    __tablename__ = "sizes"
    sizenr = Column(Integer, primary_key=True)
    size = Column(Text)

class LimitedEdition(Base):
    __tablename__ = "limited_edition"
    lenr = Column(Integer, primary_key=True)
    le = Column(Text)

engine = create_engine("postgresql://postgres:mes2102@localhost:5432/rejectthesickness")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

def write_to_db_company(compnr, compname, adress, postalcode, location, country):
    session = Session()
    company = Company(companynr=compnr, companyname=compname, adress=adress, postalcode=postalcode, location=location, country=country)
    session.add(company)
    session.commit()
    session.close()
    print("Company record added.")

def write_to_db_articles(articlenr, producttype, design, companyname, size, quantity):
    session = Session()
    article = Articles(articlenr=articlenr, producttype=producttype, design=design, companyname=companyname, size=size, quantity=quantity)
    session.add(article)
    session.commit()
    session.close()
    print("Articles record added.")

def write_to_db_designs(designnr, designname):
    session = Session()
    design = Designs(designnr=designnr, designname=designname)
    session.add(design)
    session.commit()
    session.close()
    print("Designs record added.")

def write_to_db_producttype(typenr, typename):
    session = Session()
    product_type = ProductType(typenr=typenr, typename=typename)
    session.add(product_type)
    session.commit()
    session.close()
    print("ProductType record added.")

def write_to_db_releaseyear(releaseyear):
    session = Session()
    release_year = ReleaseYear(releaseyear=releaseyear)
    session.add(release_year)
    session.commit()
    session.close()
    print("ReleaseYear record added.")

def write_to_db_sizes(sizenr, size):
    session = Session()
    size_record = Sizes(sizenr=sizenr, size=size)
    session.add(size_record)
    session.commit()
    session.close()
    print("Sizes record added.")

def write_to_db_limited_edition(lenr, le):
    session = Session()
    limited_edition = LimitedEdition(lenr=lenr, le=le)
    session.add(limited_edition)
    session.commit()
    session.close()
    print("LimitedEdition record added.")

if __name__ == "__main__":
    write_to_db_company(1, "Test Company", "123 Test Address", "12345", "Test Location", "Test Country")
    write_to_db_articles(1, "Test Product Type", "Test Design", "Test Company", "M", 10)
    write_to_db_designs(1, "Test Design Name")
    write_to_db_producttype(1, "Test Product Type Name")
    write_to_db_releaseyear(2024)
    write_to_db_sizes(1, "M")
    write_to_db_limited_edition(1, "Limited Edition A")
