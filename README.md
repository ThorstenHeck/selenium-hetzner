## Create a fresh Hetzner Project export API_TOKEN manage Member

## Requirements

optional:

1password

Mach 1password with the create_hetzner_project_1password.sh to work properly - so edit the vault and item UID that it works on your behalf. 
And auth to 1password:

    eval $(op signin)


## Setup


Clone this repo

    git clone git@github.com:ThorstenHeck/selenium-hetzner.git

Run the shell script to build and let selenium create a Project and prints out the created API Token:

    bash create_hetzner_project.sh
