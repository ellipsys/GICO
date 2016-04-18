GICO
=====

The IP console.

![globe](https://raw.githubusercontent.com/wiki/Hypsurus/GICO/images/globe.png)


GICO is a console to work with an IP address from the terminal, we can execute querys,
dump output to a file, and check geoip.

GICO uses 5 repositorys:

* delegated-arin-extended-latest
* delegated-ripencc-latest
* delegated-afrinic-latest
* delegated-apnic-latest
* delegated-lacnic-latest

Requirements
============

* Python <= 2.7

Platforms
=========

* Linux (Tested)
* Mac (Not tested)
* Windows (Not tested)

Usage
======

When you first run GICO ot will try to download the repositorys, 
it will look like:

![firsttime](https://raw.githubusercontent.com/wiki/Hypsurus/GICO/images/first_time_update.png)

After the upgrade you will be in the GICO shell, and you can start working:

![shell_commands](https://raw.githubusercontent.com/wiki/Hypsurus/GICO/images/usage_shell_commands.png)


Output of IP --info:

![ip_info](https://raw.githubusercontent.com/wiki/Hypsurus/GICO/images/ip_info_output.png)

API
====

**Command syntax:** 

> [COMMAND] by [OPTION]

`get ip by country_code US`

Command  | Action
---------|-----------------------
 get     | Get output of query
 by      |  Long query

**Query syntax**

Option       | Value
-------------|---------------------------
ip					 | IP address or request IP
country_code | Country code
status       | IP address status
created      | IP address date
asn          | IP ASN
ip_version   | IP version ipv4/ipv6
ip_provider  | IP provider ARIN/RIPE/LACNIC etc..

**Examples:**

> Get all IP address of country_code US

`get ip by country_code US`


> Save all IP address of country US

`get ip by country_code US into test.txt`

**The file will be saved in the output/ directory**

> Get ASN of IP address

`get asn by ip 0.0.0.0`

> Get country of IP address

`get country_code  by ip 0.0.0.0`

Command line
=============

> Get IP information

`./gico.py --info 0.0.0.0`

**If it return None, try to change the last 2 digits in the IP to 0 (0.0.1.2 to 0.0.0.0)**

> Run query:

`./gico.py --query "get country_code by ip 0.0.0.0" `

Contributing
=============

Contributions are very welcome!

1. fork the repository
2. clone the repo (git clone git@github.com:USERNAME/GIPC.git)
3. make your changes
6. Add yourself in contributors.txt
4. push the repository
5. make a pull request

Thank you - and happy contributing!

Copying
========

###### Copyright 2015 (C) Hypsurus <hypsurus@mail.ru>
###### License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.
