
# **Library Content WG Counter**

This script is used to check the presence of **Widgets in shortcode format** (`[widgetname][/widgetname]`) inside content assets, listing them all in JSON format.

Place inside this script folder the shared library XML file named `library.xml`.

```sh
python library-content-wg-counter/counter.py
```

By default the script search will include online and offline content. To search only online content pass the `-o` argument

```sh
python library-content-wg-counter/counter.py -o
```
