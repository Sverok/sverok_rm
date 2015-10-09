 #!/bin/bash
 #You need lingua and gettext installed to run this
 
 echo "Updating sverok_rm.pot"
 pot-create -d sverok_rm -o sverok_rm/locale/sverok_rm.pot sverok_rm/.
 echo "Merging Swedish localisation"
 msgmerge --update  sverok_rm/locale/sv/LC_MESSAGES/sverok_rm.po  sverok_rm/locale/sverok_rm.pot
 echo "Updated locale files"
 
