IMAGES_LIST_FILE="$(dirname $0)/images-to-copy.txt"

# Check if file exists before running
if [ ! -f $IMAGES_LIST_FILE ]; then
    echo "images-to-copy.txt not found, did you run list-sandbox-images.sh?"
    exit 1
fi

echo "Starting copy from development to sandbox, this will take a while..."
rclone copy development: sandbox: --include-from=images-to-copy.txt -P -vv