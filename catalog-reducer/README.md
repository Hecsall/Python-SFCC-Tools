
# **Catalog Reducer**

Place inside the repository root folder the master catalog that you want to process renamed as `masterCatalog.xml`.

Run the script and wait some time, this will parse the xml file and will create a `masterCatalog.min.xml` removing all the products 
that are **NOT online** (`<online-flag>false</online-flag>` in the xml) on **every** localization (if _at least_ one locale has the product online it will be considered online).

```sh
python reducer.py
```