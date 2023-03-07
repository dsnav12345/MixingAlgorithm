for m in {2..6}
do
    for d in {3..5}
    do
        for n in {2..5}
        do
            inp='./inputs/'${m}'_'${d}'_'${n}'.txt'
            oup='./outputs/'${m}'_'${d}'_'${n}'.txt'

#            id=$((0))
            echo -e '' > $oup

            while IFS= read -r line; do
                python3 hRASS_timed.py $line
#                id=$(( id + 1 ))
#                echo $id >> $oup
            done < "$inp"

            echo ${m} ${d} ${n}
        done
    done
done