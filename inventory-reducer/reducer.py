from pathlib import Path
from lxml import etree


# Current working directory (do not change)
CURRENT_DIRECTORY = Path(__file__).parent
# Path to the master catalog file
MASTER_CATALOG_FILE_PATH = CURRENT_DIRECTORY / "masterCatalog.min.xml"
# Path to the inventory file
SITE_INVENTORY_FILE_PATH = CURRENT_DIRECTORY / "inventory.xml"
# Destination path for the reduced site catalog
REDUCED_SITE_INVENTORY_FILE_PATH = SITE_INVENTORY_FILE_PATH.with_suffix('.min.xml')
# Catalog XML schema to be used with lxml (do not change)
SFCC_CATALOG_SCHEMA = "{http://www.demandware.com/xml/impex/catalog/2006-10-31}"
# Inventory XML schema to be used with lxml (do not change)
SFCC_INVENTORY_SCHEMA = "{http://www.demandware.com/xml/impex/inventory/2007-05-31}"


# Check if files exist before attempting to read them
if not MASTER_CATALOG_FILE_PATH.exists() or not SITE_INVENTORY_FILE_PATH.exists():
    raise Exception('{} or {} file not found'.format(MASTER_CATALOG_FILE_PATH.name, SITE_INVENTORY_FILE_PATH.name))


print("Starting to parse master catalog\n{}".format(MASTER_CATALOG_FILE_PATH))
print("Please wait...")

master_tree = etree.parse(MASTER_CATALOG_FILE_PATH)

master_catalog_products = master_tree.findall('//{schema}product'.format(schema=SFCC_CATALOG_SCHEMA))
master_products_ids = []

for product in master_catalog_products:
    master_products_ids.append(product.get('product-id'))

print("Master catalog parsing done")

print("Starting to parse site inventory\n{}".format(SITE_INVENTORY_FILE_PATH))
print("Please wait...")

inventory_tree = etree.parse(SITE_INVENTORY_FILE_PATH)

site_inventory_products = inventory_tree.findall('//{schema}record'.format(schema=SFCC_INVENTORY_SCHEMA))

for product in site_inventory_products:
    pid = product.get('product-id')
    if pid not in master_products_ids:
        print("{} - Product not found in master catalog, removing...".format(pid))
        product.getparent().remove(product)
    else:
        # Set or create allocation
        try:
            product.find('{schema}allocation'.format(schema=SFCC_INVENTORY_SCHEMA)).text = '100'
        except AttributeError:
            pass

        # Set or create ats
        try:
            product.find('{schema}ats'.format(schema=SFCC_INVENTORY_SCHEMA)).text = '100'
        except AttributeError:
            pass

        # Set or create perpetual
        try:
            product.find('{schema}perpetual'.format(schema=SFCC_INVENTORY_SCHEMA)).text = 'true'
        except AttributeError:
            pass

minproducts = inventory_tree.findall('//{schema}record'.format(schema=SFCC_INVENTORY_SCHEMA))

print("\nDone")
print("Products count: {} -> {}".format(len(site_inventory_products), len(minproducts)))

f = open(REDUCED_SITE_INVENTORY_FILE_PATH, 'wb')
f.write(etree.tostring(inventory_tree, pretty_print=True, xml_declaration=True, encoding="UTF-8"))
f.close()
