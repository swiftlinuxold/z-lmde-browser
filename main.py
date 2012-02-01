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
print 'Removing Firefox, adding Iceweasel'
os.system('apt-get purge -y firefox firefox-l10n-en-us')

print 'Adding optional blockage of Flash'
os.system('apt-get install -y xul-ext-flashblock')

import shutil

def elim_dir (dir_to_elim): 
    if (os.path.exists(dir_to_elim)):
        shutil.rmtree (dir_to_elim)

# The following directories should be DELETED:
# /home/(username)/.config/chromium 
# /home/(username)/.mozilla
# /home/(username)/.opera
print "Deleting Chromium, Mozilla, and Opera files in /home"
elim_dir ("/home/" + uname + "/.config/chromium")
elim_dir ("/home/" + uname + "/.mozilla")
elim_dir ("/etc/skel/.mozilla")
elim_dir ("/home/" + uname + "/.opera")
elim_dir ("/etc/skel/.opera")

src = dir_develop + '/browser/etc/hosts'
dest = '/etc/hosts'
shutil.copyfile (src, dest)

src = dir_develop + '/usr_local_bin/block-advert.sh'
dest = '/usr/local/bin/block-advert.sh'
shutil.copyfile (src, dest)
os.system ('chmod a+rx ' + dest)

print 'FINISHED CONFIGURING ICEWEASEL'
print '=============================='
