#!/bin/bash
PROJECT_ROOT=/lang_dec

echo "Provisioning VM for lang-dec..."

yum update -y
yum install epel-release -y
yum install kernel-devel kernel-headers dkms -y

echo "Creating the lang-dec environment with conda"
conda env create -f $PROJECT_ROOT/environment-linux.yml

echo "Deploying lang-dec as a service"
cp $PROJECT_ROOT/vagrant/run-jupyter.sh /usr/local/bin/lang-dec
chmod +x /usr/local/bin/lang-dec

cp $PROJECT_ROOT/vagrant/lang-dec.service /usr/lib/systemd/system/

echo "Starting the lang-dec service"
systemctl enable lang-dec
systemctl start lang-dec

sleep 5
echo "######## Jupyter instance details ##########"
cat /root/.local/share/jupyter/runtime/nbserver-*
