# SSH into the spawned docker and execute commands to setup ray worker node
sshpass -p password ssh -o StrictHostKeyChecking=no -t master@$1 -p $2 "bash -lic 'echo -e password | 
sudo -S su; 
sudo apt update -y;
sudo apt install python3-pip glibc-source -y;
pip install setuptools==59.5.0;
pip install --upgrade pip;
pip install grpcio==1.32.0
pip install ray[data,train,tune,serve];
/home/master/.local/bin/ray start --address $3'"


