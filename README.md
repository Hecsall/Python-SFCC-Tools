# **Python SFCC Tools**

Personal set of Python scripts useful while working with SalesForce Commerce Cloud.


## **Setup**
- Install Python 3
- Create a virtualenv to isolate the dependencies
    ```sh
    python3 -m venv venv
    ```
- Activate the virtualenv
    ```sh
    source venv/bin/activate
    ```
- Install dependencies
    ```sh
    pip install -r requirements.txt
    ```


## **Cleanup SFCC Catalog files for Sandboxes**
Inside my Sandbox I prefer to have a single siteCatalog for all the locales, this is my personal approach.

1. Use the `catalog-reducer/reducer.py` to remove all the offline products that are not visible on the website.
2. Use the `site-master-match/match.py` to compare a siteCatalog with the masterCatalog you reduced in the step before, so that it will remove all the product that are assigned in the siteCatalog but don't exist inside the masterCatalog.