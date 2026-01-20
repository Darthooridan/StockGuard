from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, Session, declarative_base

# --- DATABASE SETUP ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./stockguard.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- SQLALCHEMY MODELS (Tables) ---
class DBItem(Base):
    """
    Database model representing the 'items' table.
    """
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    quantity = Column(Integer)
    price = Column(Float)
    description = Column(String, nullable=True)

# Create tables
Base.metadata.create_all(bind=engine)

# --- PYDANTIC MODELS (Validation) ---
class ItemCreate(BaseModel):
    name: str
    quantity: int
    price: float
    description: Optional[str] = None

class ItemResponse(ItemCreate):
    id: int

    # New Pydantic V2 configuration to silence warnings
    model_config = ConfigDict(from_attributes=True)

# --- DEPENDENCY ---
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
    version="1.2.0"
)

# --- ENDPOINTS ---

@app.get("/")
def read_root():
    """Health check endpoint."""
    return {"message": "Welcome to StockGuard API - System is running"}

@app.post("/items", response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """Create a new item in the database."""
    db_item = DBItem(
        name=item.name, 
        quantity=item.quantity, 
        price=item.price, 
        description=item.description
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items", response_model=List[ItemResponse])
def get_all_items(db: Session = Depends(get_db)):
    """Retrieve all items."""
    return db.query(DBItem).all()

@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific item by ID."""
    item = db.query(DBItem).filter(DBItem.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Delete an item."""
    item = db.query(DBItem).filter(DBItem.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(item)
    db.commit()
    return {"message": "Item deleted successfully"}

@app.get("/reports/low-stock", response_model=List[ItemResponse])
def get_low_stock_items(threshold: int = 10, db: Session = Depends(get_db)):
    """
    Returns items with quantity below the threshold.
    """
    low_stock_items = db.query(DBItem).filter(DBItem.quantity < threshold).all()
    return low_stock_items