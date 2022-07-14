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
> Note: All scripts have a dedicated README inside their own folders.

1. Use the `catalog-reducer/reducer.py` to remove all the offline products that are not visible on the website.
2. Use the `site-master-match/match.py` to compare a siteCatalog with the masterCatalog you reduced in the step before, so that it will remove all the products that are assigned in the siteCatalog but don't exist inside the masterCatalog.
3. Use the `inventory-reducer/reducer.py` to remove from an inventory file every product that doesn't exist inside the masterCatalog.
4. Use the `get-product-images/images.py` to create a list of all the product images needed and then use the `get-product-images/copy-images.sh` to copy them from a development environment to your sandbox using rclone.