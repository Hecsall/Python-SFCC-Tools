MASTER_IMAGES_PATH="$(dirname $0)/master-images.txt"
OUTPUT_PATH="$(dirname $0)/sandbox-images.txt"

# Check if file exists before running
if [ ! -f $MASTER_IMAGES_PATH ]; then
    echo "master-images.txt not found, did you run images.py?"
    exit 1
fi

rclone lsf sandbox: --recursive --files-only > $OUTPUT_PATH

awk 'NR==FNR{uu[$1]=1}NR!=FNR&&uu[$1]!=1{print}' sandbox-images.txt master-images.txt > images-to-copy.txt