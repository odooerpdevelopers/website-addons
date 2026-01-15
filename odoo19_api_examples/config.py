import os
from dotenv import load_dotenv

load_dotenv()

ODOO_URL = os.getenv("ODOO_URL")
ODOO_DB = os.getenv("ODOO_DB")
ODOO_API_KEY = os.getenv("ODOO_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {ODOO_API_KEY}",
    "X-Odoo-Database": ODOO_DB,
    "Content-Type": "application/json",
}
