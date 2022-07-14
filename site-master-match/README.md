
# **Site-Master match**

This script is used to check if there are **products/recommendations** in the siteCatalog that are not present inside the masterCatalog, removing them afterwards.

Place inside the repository root folder the masterCatalog (preferably the reduced one created with the reducer script) and the siteCatalog you want to compare, named `masterCatalog.min.xml` and `siteCatalog.xml` respectively.

```sh
python site-master-match/match.py
```