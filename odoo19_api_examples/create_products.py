import requests
from config import ODOO_URL, HEADERS

# Endpoint para crear productos
url = f"{ODOO_URL}/json/2/product.template/create"

# Payload: crear 2 productos de golpe
payload = {
    "vals_list": [
        {
            "name": "Producto API Demo 1",
            "default_code": "API-DEMO-001",
            "list_price": 99.99,
        },
        {
            "name": "Producto API Demo 2",
            "default_code": "API-DEMO-002",
            "list_price": 149.99,
        },
    ]
}

print("📦 Creando 2 productos en batch...")
response = requests.post(url, headers=HEADERS, json=payload)

# Verificar respuesta
if response.status_code == 200:
    product_ids = response.json()
    print(f"\n✅ Productos creados exitosamente!")
    print(f"IDs generados: {product_ids}")
    
    for i, product_id in enumerate(product_ids, 1):
        print(f"  - Producto {i}: ID {product_id}")
else:
    error = response.json()
    print(f"❌ Error: {error['message']}")
    if "debug" in error:
        print(f"\n📋 Traceback:\n{error['debug']}")