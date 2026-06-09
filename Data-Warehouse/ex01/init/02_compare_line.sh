total=0

for f in ./*.csv; do
    count=$(($(wc -l < "$f") - 1))
    echo "$(basename "$f") : $count lignes"
    total=$((total + count))
done

echo "TOTAL : $total lignes"