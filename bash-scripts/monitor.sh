#!/bin/bash

output_file="log.csv"

echo "Time,CPU,MEMORY" > $output_file

cpu() {
    uptime | awk -F'load average:' '{ print $2 }' | awk '{ printf "%.2f", $1 * 100 }'
}

memory() {
    free | awk '/Mem:/ { printf "%.2f", $3/$2 * 100 }'
}

elapsed_time=5

while [ $elapsed_time -le 300 ]; do

    avg_cpu_usage=$(cpu)
    mem_usage=$(memory)
    
    echo -e "$elapsed_time,$avg_cpu_usage,$mem_usage" >> $output_file
    
    sleep 5

    elapsed_time=$((elapsed_time + 5))
    
done
