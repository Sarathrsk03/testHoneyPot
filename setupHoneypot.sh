# !/bin/bash 

sudo apt-get install -y python3
sudo apt-get install -y python3-pip 
sudo apt-get install -y git 

git pull https://github.com/Sarathrsk03/testHoneyPot test 

cd testHoneyPot 

read -p "Enter the company name: " $companyName 
read -p "Enter the industry: " $industry
read -p "Enter the role: " $role

echo $companyName 
echo $industry
echo $role 

#export geminiAPI=

python3 docxCreate.py 
python3 docxCreate.py

echo "All tasks completed"
