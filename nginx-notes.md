Starting with an Amazon Linux box I had lying around; not even sure if nginx is installed.

    Amazon Linux AMI release 2018.03

# Install

Probably easy -- `yum install nginx` or similar.

# Configure

Probably depends greatly on your distro.  Find a file named something like `nginx.conf` ...

Looks like I already hacked up a conf file:

    [ec2-user@ip-10-0-0-204 pyramid-tinyurl-doodle]$ rpm -ql nginx | fgrep conf | xargs ls -ld
    drwxr-xr-x 2 root     root     4096 Feb 26 00:14 /etc/nginx/conf.d
    -rw-r--r-- 1 root     root      283 Sep 11  2017 /etc/nginx/conf.d/virtual.conf
    -rw-r--r-- 1 root     root     1077 Sep 11  2017 /etc/nginx/fastcgi.conf
    -rw-r--r-- 1 root     root     1077 Sep 11  2017 /etc/nginx/fastcgi.conf.default
    -rw-rw-r-- 2 ec2-user ec2-user  386 Feb 26 00:18 /etc/nginx/nginx.conf
    -rw-r--r-- 1 root     root     2656 Sep 11  2017 /etc/nginx/nginx.conf.default
    -rw-r--r-- 1 root     root      141 Sep 11  2017 /etc/sysconfig/nginx
    [ec2-user@ip-10-0-0-204 pyramid-tinyurl-doodle]$

I confirmed that /etc/nginx/nginx.conf is identical to what's in this repo (at this commit!)

# Run

    [ec2-user@ip-10-0-0-204 pyramid-tinyurl-doodle]$ sudo /etc/rc.d/init.d/nginx start
    Starting nginx:                                            [  OK  ]

Well, shit; that was easier than I expected.
