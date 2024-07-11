from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mongodb+srv://sushanttarapure:c5WIPD6KYtcw5YGJ@sushantati1.derguct.mongodb.net/"

engine = create_engine(DATABASE_URL)
metadata = MetaData()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
