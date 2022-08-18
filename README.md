# ptisp-auto-ip-updater
Python script to automatically update the IP address on a domain record.

## How to use?
To use the script only run
``` python3 updateIP.py -d <DOMAIN> -u <USERNAME> -p <PASSWORD>```

where:
    - Domain is the domain you want to update the IP address
    - Username is the username you use to login into PTISP
    - Password is the hash you have to generate in your profile settings [here](https://my.ptisp.pt/#profile/hash)

The script generates a file with the following name structure ```<DOMAIN>_lastIP.txt```. 
