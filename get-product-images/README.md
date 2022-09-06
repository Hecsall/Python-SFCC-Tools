
# **List Product Images**
First of all we need a list of all the images we want to copy from the development instance to your sandbox instance.

To create that, use the `image.py` script, this will create a list of images that are linked inside the masterCatalog.
Place inside the repository root folder your masterCatalog file (named `masterCatalog.min.xml`) and run the python script.

Now we have our master catalog images list, but probably you already have images in your sandbox, and wasting time to copy images you already have is no good.

Here comes the `list-sandbox-images.sh` script.

`list-sandbox-images.sh` will create a `sandbox-images.txt` file with all your already existing images listed. It will then compare the `sandbox-images.txt` and the `master-images.txt` creating a new `images_to_copy.txt` file that will only contain the missing ones.

Once this final txt is created, you will use the `copy-images.sh` script from your terminal that will use your rclone config credentials (see "**rclone setup**" step in the README) to copy those images from a Development instance to your Sandbox.


## **rclone setup (required for the copy-images script)**

- Install rclone in you local machine
    ```sh
    # macOS example using homebrew
    brew install rclone
    ```
- Run the rclone Web GUI with this command
    ```sh
    rclone rcd --rc-web-gui --rc-user=admin --rc-pass=pass --rc-serve
    ```
- Inside the Web GUI, go to **Configs** and create 2 new configs for your instances, one for your Sandbox and one for your Development environment:
    - Name: In this repo, the sandbox is named "sandbox" and development is named "development". **VERY IMPORTANT every other step and script in this repo will assume that you used those names**.
    - On the select below, choose WebDAV.
    - URL: url of your environment masterCatalog WebDAV (found inside **Business Manager > Administration > Development Setup**) and should be in the format https://SOMETHING.demandware.net/on/demandware.servlet/webdav/Sites/Catalogs/masterCatalog
    - Name of the Webdav: write "**other**"
    - User name: it's the e-mail you use to enter the Business Manager
    - Password: here insert your **account password** that you use to access the Business Manager.
    - Bearer token: leave empty


## **Testing the connection**
To ensure the connection works as expected, inside the rclone Web GUI go to **Explorer** and try to open the instances you created.
If you can see the folders inside (if any) you can proceed with the next section. Otherwise check your configs again.
> Note: Testing the acces from rclone I noticed that opening WebDAV from the browser first helps rclone to connect


## **How to use `copy-images.sh`**

If you have done the steps above correctly, executing `rclone config show` in your terminal should print the 2 configs created.

Now ensure the `copy-images.sh` file refers to the 2 instances with the names you used (again, in this repo those are `development` and `sandbox`), and if everything it's ok, make the script executable and run it with the 2 commands below:

```sh
chmod +x copy-images.sh
./copy-images.sh
```

This will take **a while**, depending on how many images you have, maybe try it out with just one image to see if it works, then proceed with all of them.