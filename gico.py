#!/usr/bin/env python2

# gico.py - The IP address console
#
#  GICO is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  GICO is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2015 Hypsurus <hypsurus@mail.ru>
#

import sys
import urllib2
import os
import optparse
from lib.MyShell import myshell
from random import random
from hashlib import md5
from time import strftime

"""
 Config globals
"""

__version__ = "0.2"
__author__ = "Hypsurus"

_PATH = "./"

"""
    IP providers repository
"""
_REPOS = ['ftp.arin.net/pub/stats/arin/delegated-arin-extended-latest',
          'ftp.ripe.net/ripe/stats/delegated-ripencc-latest',
          'ftp.afrinic.net/pub/stats/afrinic/delegated-afrinic-latest',
          'ftp.apnic.net/pub/stats/apnic/delegated-apnic-latest',
          'ftp.lacnic.net/pub/stats/lacnic/delegated-lacnic-latest',
          'ftp.arin.net/info/asn.txt']

_LOCAL_REPOS = ['delegated-arin-extended-latest',
                'delegated-ripencc-latest',
                'delegated-afrinic-latest',
                'delegated-apnic-latest',
                'delegated-lacnic-latest']

_QUERY_VALUE = {'ip_provider'  : 0,
                'country_code' : 1,
                'ip_version'   : 2,
                'ip'           : 3,
                'asn'          : 4,
                'created'      : 5,
                'status'       : 6}

words = ['clear', 'exit', 'get', 'by', 'version',
         'country_code', 'ip', 'ip_provider', 'asn',
         'update', 'created', 'ip_version', 'status']

_QUERY_HOWTO = """
Examples:
    1. get ip by country_code US
    2. get ip by country_code US into ips_us.txt
    3. get ip_version by ip 0.0.0.0
    4. get created by ip 0.0.0.0
"""

class GICO_Syntax(Exception):
    def __init__(self):
        pass

class GICO(object):
    """ GICO class, all the function to get it work """
    def __init__(self):
        self.cursor = None
        self.query = None

    def get_hook(self, url, download=False):
        """ Download a file from HTTP/S,
            XXX: If download=false it will return the file size.
        """
        opener = urllib2.build_opener()
        self.cursor = opener.open("http://%s" % (url) )
        meta = self.cursor.info()
        bytes_size = int(meta.getheaders("Content-Length")[0])
        dl_bytes = 0
        file_name = url.split('/')[-1]

        if not download:
            return int(bytes_size)

        with open("%sdatabase/%s" % (_PATH, file_name), "w") as database:
            while True:
                data = self.cursor.read(1024)
                if not data:
                    break
                dl_bytes += len(data)
                database.write(data)
                sys.stdout.write("> Downloading %s (%d) of (%d) ...\r" % (file_name, dl_bytes, bytes_size) )
            sys.stdout.write("\n")
            database.close()

        with open("%sdatabase/update" %(_PATH), "a") as update:
            update.write("%s,%s,%s\n" % (file_name, url, bytes_size) )
            update.close()
    
    def check_for_update(self):
        """ Check is repository needs update """
        if not os.path.exists("%sdatabase/update" %(_PATH)):
            print_error("No \'update\' file found")
            return None
        with open("%sdatabase/update" %(_PATH), "r") as update:
            for line in update.readlines():
                # Quick hack to replace new line
                line = line.replace("\n", "")
                file_name, url, bytes_size = line.split(",")
                online_size = int(self.get_hook(url, download=False))
                if int(bytes_size) == online_size:
                    print_info("\033[01;37;42m[OK]\033[00m %s - is up-to-date." % (file_name) )
                elif online_size > int(bytes_size): 
                    print_info("\033[01;37;41m[Update]\033[00m %s - is out-of-date" % (file_name) )
                    self.get_hook(url, download=True)

    def download_repos(self, download=True):
        """ Will download the repositorys """
        if not os.path.exists("%sdatabase/" % (_PATH) ): 
            os.mkdir("%sdatabase/" % (_PATH))
        else:
            download = False
        if not os.path.exists("%soutput/" % (_PATH) ):
            os.mkdir("%soutput/" % (_PATH))
        
        if not download:
            return
        repos_len = len(_REPOS)
        counter = 0

        print_info("Updateing %d repositorys ..." % (repos_len) )
        print_info("\033[01;37;44mIt may take awhile, read the news or eat something...\033[00m")
        for repository in _REPOS:
            counter += 1
            sys.stdout.write("> Connecting to %s (%d) of (%d) ...\n" % ( repository.split("/")[0], counter, repos_len ) )
            self.get_hook(repository, download=True)

    def read_local_repo(self, ro=0, ro2=0, match=None, save=False, in_file=None, ret=False):
        """ Read local repository 
            1. c[0] == IP provider 
            2. c[1] == Country code
            3. c[2] == IP version
            4. c[3] == IP Address
            5. c[4] == ASN
            6. c[5] == Date
            7. c[6] == Status
        """
        if save:
            fp = open("%soutput/%s" % (_PATH, in_file), "w")

        for repo in _LOCAL_REPOS:
            r = open("%sdatabase/%s" % (_PATH, repo), "r" )

            for row in r.readlines():
                row = row.replace("\n", "")
                c = row.split("|")
                
                # Check if it's IP address
                # print("ro = %d, ro2 = %d, match = %s" % (ro,ro2,match) )
                try:
                    if "." in c[3] or ":" in c[3]:
                        if match:
                            if c[ro2] == match:
                                if save:
                                    fp.write("%s\n" % (c[ro]) )
                                if ret:
                                    return(c[ro])
                                else:
                                    print(c[ro])
                        elif not match:
                            print(c[ro])
                except IndexError:
                    pass
            r.close()
        if save:
            print_info("Saved into %soutput/%s ..." % (_PATH, in_file) )
            fp.close()

    def read_local_repo_asn(self, match=None, ro=1, ret=False):
        """ Get the ASN of the IP address 
            1. c[0] = ASN
            2. c[1] = AS name
            3. c[2] = POC Handlers
        """

        fp = open("%sdatabase/asn.txt" %(_PATH), "r")
        for line in fp.readlines():
            line = line.replace("\n", "")
            if line:
                if line[0].isalpha():
                    pass
                else:
                    if line.split()[0] == match:
                        if ret:
                            return "%s" % (line.split()[1][-1])
                        else:
                            print(line.split()[1])
        fp.close()

class Console(object):
    """ The console """
    def __init__(self, r):
        self.prompt = "> "
        self.GICO = r

    def do_get(self, args):
        """ Do the get command """
        ro = 0
        ro2 = 0
        match = None
        save = False
        in_file = None

        if args[0] == "get":
            print("Usage: get [query] ...")
            return

        try:    
            if len(args) >= 1:
                ro = _QUERY_VALUE[args[0]]
            if len(args) >= 4:
                _ = args.index("by")
                ro2 = _QUERY_VALUE[args[2]]
                match = args[3] 
            if len(args) > 4:
                _ = args.index("into")
                save = True
                in_file = args[5]

            if match:
                if len(match.split(".")) == 4:
                    match = match.split(".")
                    match = "%s.%s.%s.0" % (match[0], match[1], match[2])
            self.GICO.read_local_repo(ro, ro2, match, save, in_file)
        except KeyError, ValueError:
            print_error("query: invaild syntax.")
            return 

    def do_update(self, args):
        """ Run the update command """
        try:
            self.GICO.check_for_update()
        except urllib2.URLError:
            print_error("Connection failed, please check your net.")

    def do_get_asn(self, args):
        """ Get the ASN """
        if args[0] == "asn":
            print("Usage: asn [ASN] ...")
            return
        self.GICO.read_local_repo_asn(args[0])

    def do_show_version(self, args):
        """ Show versions """
        print("\033[01;37mGICO v%s\nMyShell v%s\033[00m" % (__version__, myshell.__version__)
                )
    def shell(self):
        """ Serve the shell"""
        myshell.shell_add_option("get", "Execute query.", self.do_get)
        myshell.shell_add_option("asn", "Get ASN name by ASN.", self.do_get_asn)
        myshell.shell_add_option("update", "Check for database updates.", self.do_update)
        myshell.shell_add_option("version", "show versions.", self.do_show_version)
        myshell.shell_shell(self.prompt, words)

    def shell_noint(self, query):
        """ Run shell without shell """
        query = query.split()
        query.pop(0)
        self.do_get(query)

    def ip_info(self, ip):
        """ Print IP address information """
        if len(ip.split(".")) == 4:
            ip = ip.split(".")
            ip = "%s.%s.0.0" % (ip[0], ip[1])
        ASN_NUM = self.GICO.read_local_repo(4, 3,ip, False, None, True)

        print("\033[37;31m%s/24\033[00m Info: " %(ip) )
        print("\tIP          : \033[01;37;41m%s\033[00m" % (ip) )
        print("\tProvider    : \033[01;37;44m%s\033[00m" % (self.GICO.read_local_repo(0, 3,ip, False, None, True)) )
        print("\tCountry     : \033[01;37;41m%s\033[00m" % (self.GICO.read_local_repo(1, 3,ip, False, None, True)) )
        print("\tIP version  : \033[01;37;44m%s\033[00m" % (self.GICO.read_local_repo(2, 3,ip, False, None, True)) )
        print("\tCreated     : \033[01;37;41m%s\033[00m" % (self.GICO.read_local_repo(5, 3,ip, False, None, True)) )
        print("\tStatus      : \033[01;37;44m%s\033[00m" % (self.GICO.read_local_repo(6, 3,ip, False, None, True)) )
        print("\tASN         : \033[01;37;41m%s\033[00m" % (ASN_NUM) )
        #print("\tASN name    : \033[01;37;44m%s\033[00m" % (self.GICO.read_local_repo_asn(ASN_NUM, True)) )

def print_error(msg):
    print("\033[01;37m[X] %s\033[00m" %(msg) )

def print_info(msg):
    print("\033[01;37m%s\033[00m" % (msg) )

def main():
    optparse.OptionParser.format_epilog = lambda self, formatter: self.epilog
    parser = optparse.OptionParser("Usage: %prog [OPTIONS] ...", epilog=_QUERY_HOWTO)
    parser.add_option("--query", dest="QUERY", help="Run GICO query.")
    parser.add_option("--info",  dest="IP",    help="Get IP information.")
    options,d = parser.parse_args()

    r = GICO()
    r.download_repos()
    c = Console(r)
    if options.QUERY:
        c.shell_noint(options.QUERY)
    elif options.IP:
        c.ip_info(options.IP)
    else:
        c.shell()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print_error("See you (;")
        sys.exit(0)
    except Exception as e:
        print_error(str(e))

# vim: ts=2 sw=2
