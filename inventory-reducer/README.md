
# **Inventory Reducer**

Place inside the repository root folder the reduced master catalog created with the catalog reducer, and the inventory xml file that you want to compare, named `masterCatalog.min.xml` and `inventory.xml` respectively.

The script will remove all inventory assignments pointing to products that don't exist inside the masterCatalog and set every product's allocation, ats and perpetual to make them available.

```sh
python reducer.py
```