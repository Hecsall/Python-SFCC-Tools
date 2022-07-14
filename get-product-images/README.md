
# **Get Product Images**
The `image.py` script will create a list of images that are linked inside the masterCatalog.
Place inside the repository root folder your masterCatalog file (named `masterCatalog.min.xml`) and run the python script.

Once the txt is created, using the `copy-images.sh` script from your terminal it will use your rclone config credentials to copy those images from a Development instance to your Sandbox.


## **rclone setup (required for the copy-images script)**

- Install rclone in you local machine
    ```sh
    # macOS example using homebrew
    brew install rclone
    ```
- Access inside the Business Manager of your **Sandbox** and **Development** instances, and for each one click the top right "**User profile**" icon, click the "**Manage Access Keys**" link and then "**Generate Access Key**" button.\
    In the popup window that will open, select the "**WebDAV File Access and UX Studio**" scope. Take note of the access keys that are generated.
- On your computer, run the rclone Web GUI with this command
    ```sh
    rclone rcd --rc-web-gui --rc-user=admin --rc-pass=pass --rc-serve
    ```
- Inside the Web GUI, go to **Configs** and create 2 new configs for your instances, one for your Sandbox and one for your Development environment:
    - Name: chose a name for this config, in this repo example the sandbox is named "sandbox" and development is named "development".\
    **This name will be used inside the copy-images.sh script, so keep it simple.**
    - On the select below, choose WebDAV.
    - URL: url of your environment masterCatalog WebDAV (found inside **Business Manager > Administration > Development Setup**) and should be in the format https://SOMETHING.demandware.net/on/demandware.servlet/webdav/Sites/Catalogs/masterCatalog
    - Name of the Webdav: write "**other**"
    - User name: it's the e-mail you use to enter the Business Manager
    - Password: here insert the **access key** generated inside the Business Manager before (NOT your account password).
    - Bearer token: leave empty


## **Testing the connection**
To ensure the connection works as expected, inside the rclone Web GUI go to **Explorer** and try to open the instances you created.
If you can see the folders inside (if any) you can proceed with the next section. Otherwise check your configs again.


## **Usage copy-images.sh**

If you have done the steps above correctly, executing `rclone config show` in your terminal should print the 2 configs created.

Now ensure the `copy-images.sh` file refers to the 2 instances with the names you used (again, in this repo those are `development` and `sandbox`), and if everything it's ok, make the script executable and run it with the 2 commands below:

```sh
chmod +x copy-images.sh
./copy-images.sh
```

This will take **a while**, depending on how many images you have.