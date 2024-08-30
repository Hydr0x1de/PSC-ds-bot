Setup
---
`./setup.sh`

Fill in `config.toml`: token and port (port which proxy-server uses).

Additionally, if you wanna use banlist/ban/unban commands, you should install and configure `firewalld`

`sudo apt install firewalld`

Run the bot 
`python3 main.py`


Commands list
---
```
- help
- ping       - ping the bot
- conn       - get amount of connected devices
- connlst    - get list of connected devices (their IPs)
- banlist    - get the ban list
- ban <IP>   - ban
- unban <IP> - unban
- serverinfo - get basic information about host server
- reboot     - reboot entire server
```

Using reboot command supposes you run the bot not on the local computer, and also have set up autostart of the bot.