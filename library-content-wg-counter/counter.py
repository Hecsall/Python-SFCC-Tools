from pathlib import Path
from lxml import etree
import sys
import re
import json

# The library.xml exported from Salesforce contains some instances of &#11; and &#13;
# Remove them from the file with a search and replace before running this script or it will break

# Script root directory (do not change)
SCRIPT_DIRECTORY = Path(__file__).parent
# Path to the library file
LIBRARY_FILE_PATH = SCRIPT_DIRECTORY / "library.xml"
# Library XML schema to be used with lxml (do not change)
SFCC_LIBRARY_SCHEMA = "{http://www.demandware.com/xml/impex/library/2006-10-31}"
# Output
OUTPUT_JSON = SCRIPT_DIRECTORY / "output.json"
# Find only online contents or not
find_only_online_contents = False


opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]

if "-o" in opts:
    find_only_online_contents = True

# Check if files exist before attempting to read them
if not LIBRARY_FILE_PATH.exists():
    raise Exception('{} file not found'.format(LIBRARY_FILE_PATH.name))


print("Starting to parse library\n{}".format(LIBRARY_FILE_PATH))
print("Please wait...")

library_tree = etree.parse(LIBRARY_FILE_PATH)

library_contents = library_tree.findall('//{schema}content'.format(schema=SFCC_LIBRARY_SCHEMA))
print("Found {} contents".format(len(library_contents)))

contents_to_loop = []

if find_only_online_contents:
    for content in library_contents:
        # Find contents that have at least one <online-flag>true</online-flag>
        onlineflags = content.findall('{schema}online-flag'.format(schema=SFCC_LIBRARY_SCHEMA))
        any_online = any(flag.text == 'true' for flag in onlineflags)
        if any_online:
            contents_to_loop.append(content)
else:
    contents_to_loop = library_contents

contents_with_widgets = {}

for content in contents_to_loop:
    content_id = content.attrib['content-id']
    content_attributes = content.find('{schema}custom-attributes'.format(schema=SFCC_LIBRARY_SCHEMA))

    if content_attributes is not None:
        body_content_attributes = content_attributes.findall('{schema}custom-attribute'.format(schema=SFCC_LIBRARY_SCHEMA))
        if body_content_attributes:
            for body in body_content_attributes:
                bodytext = body.text
                # Search for closing widget tags [/something] with letters numbers - _ and .
                matches = re.findall(r'\[\/([a-zA-Z0-9_.-]*)\]', bodytext)

                if matches:
                    for match in matches:
                        if match in contents_with_widgets:
                            if content_id not in contents_with_widgets[match]:
                                contents_with_widgets[match].append(content_id)
                        else:
                            contents_with_widgets[match] = [content_id]

with open(OUTPUT_JSON, "w") as outfile:
    json.dump(contents_with_widgets, outfile, sort_keys=True)
