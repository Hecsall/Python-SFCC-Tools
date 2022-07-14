from doctest import master
from pathlib import Path
from lxml import etree


# Repo root directory (do not change)
ROOT_DIRECTORY = Path(__file__).parent.parent
# Path to the master catalog file
MASTER_CATALOG_FILE_PATH = ROOT_DIRECTORY / "masterCatalog.xml"
# Destination path for the reduced catalog
REDUCED_CATALOG_FILE_PATH = MASTER_CATALOG_FILE_PATH.with_suffix('.min.xml')
# Catalog XML schema to be used with lxml (do not change)
SFCC_CATALOG_SCHEMA = "{http://www.demandware.com/xml/impex/catalog/2006-10-31}"


# Check if files exist before attempting to read them
if not MASTER_CATALOG_FILE_PATH.exists():
    raise Exception('{} file not found'.format(MASTER_CATALOG_FILE_PATH.name))


def is_online(product):
    online_flags = product.findall('{schema}online-flag'.format(schema=SFCC_CATALOG_SCHEMA))
    for online_flag in online_flags:
        if online_flag.text == 'true':
            return True
    return False


def is_master(product):
    variants = product.findall('{schema}variations//{schema}variants//{schema}variant'.format(schema=SFCC_CATALOG_SCHEMA))
    if len(variants) > 0:
        return True
    return False
   

print("Starting to process catalog\n{}".format(MASTER_CATALOG_FILE_PATH))
print("Please wait...")

tree = etree.parse(MASTER_CATALOG_FILE_PATH)
root = tree.getroot()

products = tree.findall('//{schema}product'.format(schema=SFCC_CATALOG_SCHEMA))

# Creating arrays to store products in groups for later use.
master_products = []
deletable_products = []

for product in products:
    if is_master(product):
        master_products.append(product)
    elif not is_online(product):
        deletable_products.append(product)

# Search inside master products the ones that have only variants product-id present inside deletable_products.
for master in master_products:
    master_variants = master.find('{schema}variations//{schema}variants'.format(schema=SFCC_CATALOG_SCHEMA))
    single_variants = master_variants.findall('{schema}variant'.format(schema=SFCC_CATALOG_SCHEMA))
    for variant in single_variants:
        variant_id = variant.attrib['product-id']
        for deletable_product in deletable_products:
            if variant_id in deletable_product.attrib['product-id']:
                master_variants.remove(variant)
                break

# Delete Master products that have no more variants.
for master in master_products:
    variants = master.findall('{schema}variations//{schema}variants//{schema}variant'.format(schema=SFCC_CATALOG_SCHEMA))
    if len(variants) == 0:
        root.remove(master)

# Remove all variants that are not online.
for product in deletable_products:
    root.remove(product)

minproducts = tree.findall('//{schema}product'.format(schema=SFCC_CATALOG_SCHEMA))

print("\nDone")
print("Products count: {} -> {}".format(len(products), len(minproducts)))

f = open(REDUCED_CATALOG_FILE_PATH, 'wb')
f.write(etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding="UTF-8"))
f.close()
