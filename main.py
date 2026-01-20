from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, Session, declarative_base

# --- DATABASE SETUP ---
# Create a simple SQLite database file named 'stockguard.db'
SQLALCHEMY_DATABASE_URL = "sqlite:///./stockguard.db"

# engine is the connection point to the database
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal is the factory for creating database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our database models
Base = declarative_base()

# --- SQLALCHEMY MODELS (Tables) ---
class DBItem(Base):
    """
    This class represents the 'items' table in the database.
    Each attribute corresponds to a column in the table.
    """
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    quantity = Column(Integer)
    price = Column(Float)
    description = Column(String, nullable=True)

# Create the tables in the database
Base.metadata.create_all(bind=engine)

# --- PYDANTIC MODELS (Data Validation) ---
# Used for reading/writing data via API
class ItemCreate(BaseModel):
    name: str
    quantity: int
    price: float
    description: Optional[str] = None

class ItemResponse(ItemCreate):
    id: int

    # Configuration to allow Pydantic to read data from SQLAlchemy objects
    class Config:
        from_attributes = True

# --- DEPENDENCY ---
# This function ensures we open a DB session for a request and close it afterwards
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- API APP ---
app = FastAPI(
    title="StockGuard API",
    description="Warehouse management system with SQLite database",
    version="1.1.0"
)

@app.post("/items", response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """
    Create a new item in the database.
    """
    # Create a database object (DBItem) from the input data (ItemCreate)
    db_item = DBItem(
        name=item.name, 
        quantity=item.quantity, 
        price=item.price, 
        description=item.description
    )
    # Add to session and commit (save) changes
    db.add(db_item)
    db.commit()
    # Refresh to get the generated ID
    db.refresh(db_item)
    return db_item

@app.get("/items", response_model=List[ItemResponse])
def get_all_items(db: Session = Depends(get_db)):
    """Retrieve all items from the database."""
    return db.query(DBItem).all()

@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific item by ID."""
    item = db.query(DBItem).filter(DBItem.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.get("/reports/low-stock", response_model=List[ItemResponse])
def get_low_stock_items(threshold: int = 10, db: Session = Depends(get_db)):
    """
    Returns a list of items with quantity below the specified threshold.
    Default threshold is 10 units.
    Useful for restocking alerts.
    """
    # Filter items where quantity is less than the threshold
    low_stock_items = db.query(DBItem).filter(DBItem.quantity < threshold).all()
    
    return low_stock_items

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Delete an item from the database."""
    item = db.query(DBItem).filter(DBItem.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(item)
    db.commit()
    return {"message": "Item deleted successfully"}