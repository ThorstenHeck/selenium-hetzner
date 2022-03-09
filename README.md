## Create a fresh Hetzner Project export API_TOKEN manage Member

## Requirements

1password

## Setup

Auth to 1password

    eval $(op signin)

Clone this repo

    git clone git@github.com:ThorstenHeck/selenium-hetzner.git

Match your secret management with proper mapping inside 1password and edit the create_etzner_project.sh to your needs.

Run the shell script to build and let selenium create a Project and export the API Token to your 1password vault

    bash create_hetzner_project.sh
