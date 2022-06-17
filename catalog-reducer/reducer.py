from pathlib import Path
from lxml import etree


# Current working directory (do not change)
CURRENT_DIRECTORY = Path(__file__).parent
# Path to the master catalog file
MASTER_CATALOG_FILE_PATH = CURRENT_DIRECTORY / "masterCatalog.xml"
# Destination path for the reduced catalog
REDUCED_CATALOG_FILE_PATH = MASTER_CATALOG_FILE_PATH.with_suffix('.min.xml')
# Catalog XML schema to be used with lxml (do not change)
SFCC_CATALOG_SCHEMA = "{http://www.demandware.com/xml/impex/catalog/2006-10-31}"


def is_online(product):
    online_flags = product.findall('{schema}online-flag'.format(schema=SFCC_CATALOG_SCHEMA))
    for online_flag in online_flags:
        if online_flag.text == 'true':
            return True
    return False


print("Starting to process catalog\n{}".format(MASTER_CATALOG_FILE_PATH))
print("Please wait...")

tree = etree.parse(MASTER_CATALOG_FILE_PATH)
root = tree.getroot()

# categories = tree.findall('//{schema}category'.format(schema=SFCC_CATALOG_SCHEMA))
products = tree.findall('//{schema}product'.format(schema=SFCC_CATALOG_SCHEMA))

for product in products:
    if not is_online(product):
        pid = product.get('product-id')
        # print("{} - not online, removing...".format(pid))
        root.remove(product)

minproducts = tree.findall('//{schema}product'.format(schema=SFCC_CATALOG_SCHEMA))

print("\nDone")
print("Products count: {} -> {}".format(len(products), len(minproducts)))

f = open(REDUCED_CATALOG_FILE_PATH, 'wb')
f.write(etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding="UTF-8"))
f.close()
