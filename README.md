#ProZaC - Proxy Zabbix Ceilometer


##Objective
This project started as a way to integrate monitoring information collected in a Cloud environment, namely by OpenStack's Ceilometer, exporting it to an already existing monitoring solution using Zabbix.

##Features

* Integration of OpenStack's available monitoring information (e.g. using Ceilometer) with already existing Monitoring systems (e.g. Zabbix);
* Automatically gather information about the existing Cloud Infrastructure being considered (tenants, instances);
* Seamlessly handle changes in the Cloud Infrastructure (creation and deletion of tenants and/or instances);
* Periodically retrieve resources/meters details from OpenStack;
* Allow to have one common monitoring system (e.g Zabbix) for several, distributed, OpenStack-based Cloud Data Centres.

##Requirements
ProZaC was written using _Python_ version 2.7.5 but can be easily ported to version 3. For support of AMQP protocol, it is used either Pika or Qpid-Proton, depending whether the message broker is RabbitMQ or QPID.

For installing those libraries, if you already have _Python_ and the _pip_ packet manager configured, you need only to use a terminal/console and simply run:

		sudo pip install pika 
		
		sudo pip install python-qpid-proton 

Otherwise, you might check whether pika or qpid are available in the software repositories of your distribution, i.e.

	        sudo yum install python-pika python-qpid-proton

		sudo apt-get install python-pika python-qpid-proton

If the previous command fails, download and manually install the Pika library on the host where you intend to run ProZaC:

This can be done installing dependencies as root: 

  apt-get install build-essential cmake uuid-dev python-dev libssl-dev swig \
     ruby libboost-dev libboost-program-options-dev libboost-system-dev libsasl2-dev \
     libnspr4-dev libnss3-dev libdb++-dev libaio-dev

and after downloading qpid packages http://qpid.apache.org/download.html Qpid Proton and Qpid C++ Broker. after quite easily 
configure and compile both packages:

  wget http://apache.fastbull.org/qpid/proton/0.8/qpid-proton-0.8.tar.gz
  tar -zxvf qpid-proton-0.8.tar.gz 
  cd qpid-proton-0.8/
  mkdir build
  cd build/
  cmake .. -DCMAKE_INSTALL_PREFIX=/installdir -DSYSINSTALL_PYTHON=ON -DBUILD_PHP=OFF -DBUILD_PERL=OFF \
    -DBUILD_RUBY=OFF -DBUILD_ JAVA=OFF
  make all

and after as root: 

  make install

more or less the same for the C++ broker:
 
 wget http://mirrors.muzzy.it/apache/qpid/0.30/qpid-cpp-0.30.tar.gz
 tar -zxvf qpid-cpp-0.30.tar.gz
 cd qpid-cpp-0.30
 mkdir build
 cd build/
 cmake .. -DCMAKE_INSTALL_PREFIX=/instaldir -DBUILD_BINDING_PERL=OFF -DSYSCONF_INSTALL_DIR=/etc
 make all

as root:

 make install


**Note:** Since the purpose of this project is to be integrated with OpenStack and Zabbix it is assumed that apart from a running installation of these two, some knowledge of OpenStack has already been acquired.

##Usage
Assuming that all the above requirements are met, ProZaC can be run  with 3 simple steps:

1. On your OpenStack installation point to your Keystone configuration file (keystone.conf) and uncomment the following line:

		notification_driver = keystone.openstack.common.notifier.rpc_notifier

2. Edit the `proxy.conf` configuration file to reflect your own system, including the IP addresses and ports of Zabbix and of the used OpenStack modules (RabbitMQ/QPID, Ceilometer Keystone and Nova). You can also tweak some ZCP internal configurations such as the polling interval, template name and proxy name (used in Zabbix).

3. Finally, copy the provided init script in the init.d directory, and run the Proxy Zabbix-Ceilometer !
   	    
		sudo mv prozac /etc/init.d/

		service prozac start

If all goes well the information retrieved from OpenStack's Ceilometer will be pushed in your Zabbix monitoring system.

##Source

If not doing so already, you can check out the latest version of Prozac through [github](https://github.com/egiorgio/ProZaC).

##Copyright

(C) Istituto Nazionale di Fisica Nucleare. For more info, emidio.giorgio@ct.infn.it

##Credits

ProZaC is a fork of *ZabbixCeilometer-Proxy* (aka ZCP), which is Copyright of OneSource Consultoria Informatica, Lda. [🔗](http://www.onesource.pt). For further information about ZCP, check its [github](https://github.com/clmarques/ZabbixCeilometer-Proxy).
Main features introduced with ProZaC:

* support to distinct message brokers servers between nova and keystone (distributed/federated cloud scenarios)
* support to QPID message brokers  
* support to file logging (through python lib)
* support to token renewal : it's no longer needed to restart the proxy each hour
* init script provision
 
See individual source files for more details about functionalities added after the fork.

##License
Distributed under the Apache 2 license. See ``LICENSE.txt`` for more information.

##About

This work has been supported by INFN, Catania division, in the context of PRISMA project. For further details about PRISMA, check out the [PRISMA website](http://www.ponsmartcities-prisma.it/). 
For more details on ProZaC, or Zabbix consultancy, please contact main author via email **_emidio.giorgio✉️ct.infn.it__**   
