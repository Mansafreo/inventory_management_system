# Inventory Management System
A simple CLI project using Python that manages the inventory for a small shop or business. <br>
The CLI has two main menus:
- Stock
- Sales

The stock has the items that the shop has, it also has options to add,edit,view,view_all and delete items. <br>
The sales are what has been sold <br>
There is a one-many relationship between the sales and items since one sale can have many items

## Dependencies
1. pipenv
2. sqlalchemy(as the ORM)
3. click (to manage CLI operations)

## Step-By-Step Guide
### Step0
Make sure you have python installed on your computer. I was using `version 3.12.0` for this project
### Step1: Project Setup
1. Create a directory for your project
2. Install pipenv using 
```python
pip install pipenv
```
3. Initialize pipenv(Replace the version with yours)
```python
pipenv --python 3.12 
```
5. Install the other dependencies
```python
pipenv install sqlalchemy click
```
6. Activate the pipenv shell
```python
pipenv shell
```
### Step2:Define the data models
1. Create the database using the query below (sqlite) or you can just copy the 'inventory.db' file included in this repo
```sql
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY,
    name TEXT,
    price REAL,
    quantity INTEGER
);

CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY,
    date TIMESTAMP,
    total_amount REAL
);

ALTER TABLE sales ADD COLUMN item_id INTEGER;

```
2. Create a `models.py ` file and add create the models
```py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    quantity = Column(Integer)

    sales = relationship("Sale", back_populates="item")

class Sale(Base):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    total_amount = Column(Float)

    items = relationship("Item", back_populates="sale")

    def __repr__(self):
        return f"<Sale(id={self.id}, date={self.date}, total_amount={self.total_amount})>"
```

### Step 3: Setting up the ORM (SQLAlchemy)
create a `database.py` file
```py
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    quantity = Column(Integer)

    sales = relationship("Sale", back_populates="item")

class Sale(Base):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.now)
    total_amount = Column(Float)

    item_id = Column(Integer, ForeignKey('items.id'))
    item = relationship("Item", back_populates="sales")

# Define your engine and create tables
engine = create_engine('sqlite:///inventory.db')
Base.metadata.create_all(engine)
```
### Step4: Createing the CLI interface
Create a `cli.py` with the necessary menus
```py
import click
from sqlalchemy.orm import sessionmaker
from database import engine, Item, Sale

Session = sessionmaker(bind=engine)

@click.group()
def cli():
    pass

@cli.group()
def stock():
    pass

@cli.group()
def sales():
    pass

@stock.command()
def view_all_items():
    session = Session()
    items = session.query(Item).all()
    click.echo("\nAll Items:")
    for item in items:
        click.echo(f"{item.id}. {item.name} - Quantity: {item.quantity}, Price: {item.price}")
    session.close()

@stock.command()
@click.argument('item_id', type=int)
def view_item(item_id):
    session = Session()
    item = session.query(Item).filter_by(id=item_id).first()
    if item:
        click.echo(f"\nItem ID: {item.id}")
        click.echo(f"Name: {item.name}")
        click.echo(f"Price: {item.price}")
        click.echo(f"Quantity: {item.quantity}")
    else:
        click.echo("Item not found.")
    session.close()

@stock.command()
@click.argument('name')
@click.argument('price', type=float)
@click.argument('quantity', type=int)
def add_item(name, price, quantity):
    session = Session()
    item = Item(name=name, price=price, quantity=quantity)
    session.add(item)
    session.commit()
    click.echo("Item added successfully.")
    session.close()

# Implement other stock commands (delete-item, edit-item) similarly

@sales.command()
@click.argument('sale_id', type=int)
def delete_sale(sale_id):
    session = Session()
    sale = session.query(Sale).filter_by(id=sale_id).first()
    if sale:
        session.delete(sale)
        session.commit()
        click.echo("Sale deleted successfully.")
    else:
        click.echo("Sale not found.")
    session.close()

@sales.command()
def view_all_sales():
    session = Session()
    sales = session.query(Sale).all()
    click.echo("\nAll Sales:")
    for sale in sales:
        click.echo(f"{sale.id}. Date: {sale.date}, Total Amount: {sale.total_amount}")
    session.close()

@sales.command()
@click.argument('date')
@click.argument('total_amount', type=float)
def add_sale(date, total_amount):
    session = Session()
    sale = Sale(date=date, total_amount=total_amount)
    session.add(sale)
    session.commit()
    click.echo("Sale added successfully.")
    session.close()

@sales.command()
@click.argument('sale_id', type=int)
@click.argument('date')
@click.argument('total_amount', type=float)
def edit_sale(sale_id, date, total_amount):
    session = Session()
    sale = session.query(Sale).filter_by(id=sale_id).first()
    if sale:
        sale.date = date
        sale.total_amount = total_amount
        session.commit()
        click.echo("Sale edited successfully.")
    else:
        click.echo("Sale not found.")
    session.close()

@sales.command()
@click.argument('sale_id', type=int)
def view_sale(sale_id):
    session = Session()
    sale = session.query(Sale).filter_by(id=sale_id).first()
    if sale:
        click.echo(f"\nSale ID: {sale.id}")
        click.echo(f"Date: {sale.date}")
        click.echo(f"Total Amount: {sale.total_amount}")
    else:
        click.echo("Sale not found.")
    session.close()

if __name__ == '__main__':
    cli()
```
## Running the project
Open your terminal in pipenv as shown in step 1
Run the command `python cli.py` followed by the arguments created e.g `python cli.py sales` will go to sales

### Points to Note
This project does not includes dicttionaries(dict), lists or tuples
   

