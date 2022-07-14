from pathlib import Path
from lxml import etree


# Repo root directory (do not change)
ROOT_DIRECTORY = Path(__file__).parent.parent
# Path to the master catalog file
MASTER_CATALOG_FILE_PATH = ROOT_DIRECTORY / "masterCatalog.min.xml"
# Path to the site catalog file
SITE_CATALOG_FILE_PATH = ROOT_DIRECTORY / "siteCatalog.xml"
# Destination path for the reduced site catalog
REDUCED_SITE_CATALOG_FILE_PATH = SITE_CATALOG_FILE_PATH.with_suffix('.min.xml')
# Catalog XML schema to be used with lxml (do not change)
SFCC_CATALOG_SCHEMA = "{http://www.demandware.com/xml/impex/catalog/2006-10-31}"


# Check if files exist before attempting to read them
if not MASTER_CATALOG_FILE_PATH.exists() or not SITE_CATALOG_FILE_PATH.exists():
    raise Exception('{} or {} file not found'.format(MASTER_CATALOG_FILE_PATH.name, SITE_CATALOG_FILE_PATH.name))


print("Starting to parse master catalog\n{}".format(MASTER_CATALOG_FILE_PATH))
print("Please wait...")

master_tree = etree.parse(MASTER_CATALOG_FILE_PATH)

master_catalog_products = master_tree.findall('//{schema}product'.format(schema=SFCC_CATALOG_SCHEMA))
master_products_ids = []

for product in master_catalog_products:
    master_products_ids.append(product.get('product-id'))

print("Master catalog parsing done")

print("Starting to parse site catalog\n{}".format(SITE_CATALOG_FILE_PATH))
print("Please wait...")

site_tree = etree.parse(SITE_CATALOG_FILE_PATH)
site_root = site_tree.getroot()

site_catalog_category_assignments = site_tree.findall('//{schema}category-assignment'.format(schema=SFCC_CATALOG_SCHEMA))

for assignment in site_catalog_category_assignments:
    pid = assignment.get('product-id')
    if pid not in master_products_ids:
        # print("{} - Product not found in master catalog, removing...".format(pid))
        site_root.remove(assignment)

site_catalog_recommendations = site_tree.findall('//{schema}recommendation'.format(schema=SFCC_CATALOG_SCHEMA))

for recommendation in site_catalog_recommendations:
    sid = recommendation.get('source-id')
    tid = recommendation.get('target-id')
    if sid not in master_products_ids or tid not in master_products_ids:
        # print("{}/{} - Recommendation products not found in master catalog, removing...".format(sid, tid))
        site_root.remove(recommendation)

minassignments = site_tree.findall('//{schema}category-assignment'.format(schema=SFCC_CATALOG_SCHEMA))
minrecommendations = site_tree.findall('//{schema}recommendation'.format(schema=SFCC_CATALOG_SCHEMA))

print("\nDone")
print("Products count: {} -> {}".format(len(site_catalog_category_assignments), len(minassignments)))
print("Recommendations count: {} -> {}".format(len(site_catalog_recommendations), len(minrecommendations)))

f = open(REDUCED_SITE_CATALOG_FILE_PATH, 'wb')
f.write(etree.tostring(site_tree, pretty_print=True, xml_declaration=True, encoding="UTF-8"))
f.close()
