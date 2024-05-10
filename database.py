from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Item, Sale

# Initialize SQLAlchemy engine
engine = create_engine('sqlite:///inventory.db')

# Create all tables defined in models.py
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Optional: Add initial data to the database if needed
# e.g., session.add(Item(name='Product 1', price=10.99, quantity=100))
#       session.add(Sale(date=datetime.now(), total_amount=50.0))
#       session.commit()

# Close the session when done
# session.close()
