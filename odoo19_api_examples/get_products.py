import requests
from config import ODOO_URL, HEADERS

# Endpoint para buscar y leer productos
model_name = "product.template"
url = f"{ODOO_URL}/json/2/{model_name}/search_read"

# Payload: buscar productos almacenables
payload = {
    "domain": [["is_storable", "=", True]],
    "fields": ["name", "default_code", "list_price"],
    "limit": 5,
    "context": {"lang": "es_ES"},
}

print("🔍 Buscando productos almacenables...")
response = requests.post(url, headers=HEADERS, json=payload)

# Verificar respuesta
if response.status_code == 200:
    products = response.json()
    print(f"\n✅ Se encontraron {len(products)} productos:\n")
    
    for product in products:
        print(f"ID: {product['id']}")
        print(f"Nombre: {product['name']}")
        print(f"SKU: {product.get('default_code', 'Sin SKU')}")
        print(f"Precio: ${product['list_price']}")
        print("-" * 50)
else:
    error = response.json()
    print(f"❌ Error: {error['message']}")