# main.py

# importing the database and analysis and visualization function
from modules.database import add_category, get_category_id, add_transaction,create_tables
from modules.analysis import spending_by_category, monthly_spending_trend
from modules.visualization import plot_spending_by_category, plot_monthly_spending_trend
from logging.handlers import RotatingFileHandler#used to do over modification to the logger


# Importing required modules
import os 
# Needed to use the basic io functions and access the file system
import logging
from datetime import datetime

# If the folder exists then dont create else create the folder named following
os.makedirs("data", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# Create a rotating log handler (max 1MB per file, keep 2 backups)
handler = RotatingFileHandler(
    filename="logs/app.log",
    maxBytes=1024*1024,  # 1MB per file
    backupCount=2,       # Keep 2 backup logs (app.log.1, app.log.2) after some it willlbe deleted
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[handler]  # Use RotatingFileHandler instead of basic file logging to use the handler like macBytes and backup count
)
# Example of logging and formatting the structure
logging.info("Application started at " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# the create table if not exists
create_tables()

# add dummy transactions - only once, then comment after running
try:
    # Add categories to the categories table
    add_category("Food")
    add_category("Transport")
    add_category("Groceries")
    add_category("Rent")

    # fetch category IDs for the categories
    food_id = get_category_id("Food")
    transport_id = get_category_id("Transport")
    groceries_id = get_category_id("Groceries")
    rent_id = get_category_id("Rent")

    # Add transactions with the correct category_id
    add_transaction(food_id, 500, "2025-04-14", "Lunch at cafe")
    add_transaction(transport_id, 300, "2025-04-15", "Bus fare")
    add_transaction(groceries_id, 1200, "2025-04-13", "Weekly shopping")
    add_transaction(food_id, 650, "2025-03-28", "Dinner with friends")
    add_transaction(rent_id, 8000, "2025-03-01", "Monthly rent")
except Exception as e:
    # Prevents duplicate insertion
    logging.warning(f"Sample data not added: {e}")

#: print the analysis result on terminal
print("\n--- Summary by Category ---")
spending_by_category()

print("\n--- Monthly Summary ---")
monthly_spending_trend()

# show the graph
plot_spending_by_category()
plot_monthly_spending_trend()
