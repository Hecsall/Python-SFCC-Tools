while IFS="" read -r p || [ -n "$p" ]
do
    PARENT_DIR=$(dirname $p)
    rclone copy development:$p sandbox:$PARENT_DIR
    echo "Done $p"
done < images-list.txt
