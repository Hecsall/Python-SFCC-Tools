IMAGES_LIST_FILE="$(dirname $0)/master-images.txt"

# Check if file exists before running
if [ ! -f $IMAGES_LIST_FILE ]; then
    echo "master-images.txt not found, did you run imager.py?"
    exit 1
fi


while IFS="" read -r p || [ -n "$p" ]
do
    PARENT_DIR=$(dirname $p)
    # Example
    # rclone copy /default/images/images/123.png /default/images/images
    rclone copy development:$p sandbox:$PARENT_DIR
    echo "Done $p"
done < master-images.txt
