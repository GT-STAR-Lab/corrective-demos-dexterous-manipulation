echo "Setting up training configs for User $1...";

cd ~/GT/CoRX/hand_dapg/dapg/study_data;

demos="30 20 10 20_10_1 10_20_1 20_10_2 10_20_2"

for demo in $demos; do
    sed "s/<user_id>/$1/g" dapg_template.txt > $1/configs/dapg_$1_$demo.txt; sed -i "s/<demos>/$demo/" $1/configs/dapg_$1_$demo.txt;
done
cd - > /dev/null;

echo "Created config files for User $1!"