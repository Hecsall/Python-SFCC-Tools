from pathlib import Path
from lxml import etree


# Current working directory (do not change)
CURRENT_DIRECTORY = Path(__file__).parent
# Repo root directory (do not change)
ROOT_DIRECTORY = Path(__file__).parent.parent
# Path to the master catalog file
MASTER_CATALOG_FILE_PATH = ROOT_DIRECTORY / "masterCatalog.min.xml"
# Output path for the images list text file
IMAGES_LIST_FILE = CURRENT_DIRECTORY / "master-images.txt"
# Catalog XML schema to be used with lxml (do not change)
SFCC_CATALOG_SCHEMA = "{http://www.demandware.com/xml/impex/catalog/2006-10-31}"


# Check if files exist before attempting to read them
if not MASTER_CATALOG_FILE_PATH.exists():
    raise Exception('{} file not found'.format(MASTER_CATALOG_FILE_PATH.name))


print("Starting to process catalog\n{}".format(MASTER_CATALOG_FILE_PATH))
print("Please wait...")

tree = etree.parse(MASTER_CATALOG_FILE_PATH)
root = tree.getroot()

images = tree.findall('//{schema}image'.format(schema=SFCC_CATALOG_SCHEMA))

images_paths = []

for image in images:
    path = 'default/images{}'.format(image.get('path'))
    if path not in images_paths:
        images_paths.append('default/images{}'.format(image.get('path')))

print("\nDone")

f = open(IMAGES_LIST_FILE, 'w')
f.write('\n'.join(sorted(images_paths)))
f.close()
