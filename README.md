This repo contains an authentication module for Keystone.
This module sets the REMOTE_USER variable if the user can be authenticated against an external backend (sheldon)
When the REMOTE_USER variable is set Keystone will assume the user is authenticated and will give the user access
based on the user in keystone with the same name (with sheldon we prepend the username with spil- to easily differentiate between normal and sheldon users).
