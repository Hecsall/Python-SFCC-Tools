while IFS="" read -r p || [ -n "$p" ]
do
    PARENT_DIR=$(dirname $p)
    # Example
    # rclone copy /default/images/images/123.png /default/images/images
    rclone copy development:$p sandbox:$PARENT_DIR
    echo "Done $p"
done < images-list.txt
