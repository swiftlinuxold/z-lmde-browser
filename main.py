#! /usr/bin/env python

# Check for root user login
import os, sys
if not os.geteuid()==0:
    sys.exit("\nOnly root can run this script\n")

# Get your username (not root)
import pwd
uname=pwd.getpwuid(1000)[0]

# The remastering process uses chroot mode.
# Check to see if this script is operating in chroot mode.
# /home/mint directory only exists in chroot mode
is_chroot = os.path.exists('/home/mint')
dir_develop=''
if (is_chroot):
	dir_develop='/usr/local/bin/develop'
	dir_user = '/home/mint'
else:
	dir_develop='/home/' + uname + '/develop'
	dir_user = '/home/' + uname

# Everything up to this point is common to all Python scripts called by shared-*.sh
# =================================================================================

print '==========================='
print 'BEGIN CONFIGURING ICEWEASEL'

# Remove Firefox, which is automatically replaced with Iceweasel
print 'Removing Firefox'
os.system('apt-get remove -y firefox firefox-l10n-en-us')


print 'FINISHED CONFIGURING ICEWEASEL'
print '=============================='
