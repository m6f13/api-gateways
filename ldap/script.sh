#!/bin/bash

ORG_DC="proconion"
ORG_DOMAIN="com"
USER_UID="$1"
USER_CN="$2"
USER_SN="$3"
USER_PASS="$4"

# Create the organization LDIF
cat <<EOL > organization.ldif
dn: dc=$ORG_DC,dc=$ORG_DOMAIN
objectClass: top
objectClass: dcObject
objectClass: organization
o: $ORG_DC
dc: $ORG_DC

EOL

# Create the user LDIF
cat <<EOL > user.ldif
dn: uid=$USER_UID,ou=users,dc=$ORG_DC,dc=$ORG_DOMAIN
objectClass: top
objectClass: person
objectClass: organizationalPerson
objectClass: inetOrgPerson
uid: $USER_UID
cn: $USER_CN
sn: $USER_SN
userPassword: $USER_PASS

EOL
