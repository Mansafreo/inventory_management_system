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
