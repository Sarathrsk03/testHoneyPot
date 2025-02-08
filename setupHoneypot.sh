# !/bin/bash 

sudo apt-get install -y python3
sudo apt-get install -y python3-pip 
sudo apt-get install -y git 

git pull https://github.com/Sarathrsk03/testHoneyPot test 

cd testHoneyPot 

read -p "Enter the company name: " companyNameInp 
read -p "Enter the industry: " industryInp
read -p "Enter the role: " roleInp
export companyName= $companyNameInp
export industry= $industryInp
export role= $roleInp

#export geminiAPI=

python3 generatePrompts.py 

echo "All tasks completed"
cd .. 
rm setup.sh
rm -rf testHoneypot
exit
