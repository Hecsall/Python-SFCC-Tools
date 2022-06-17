while IFS="" read -r p || [ -n "$p" ]
do
    rclone copy development:$p sandbox:$p
    echo "Done $p"
done < images-list.txt
