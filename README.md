setup
---
optionally (recommended) create virtual environment `python3 -m venv venv`
and activate it `source venv/bin/activate`

install packages
`pip install discord.py`

create "config.txt" file
add the discord bot token in the first line 
add the port which proxy uses in the second line

run the bot 
`python3 main.py`

---
commands list:
```
- help
- ping       - ping the bot
- conn       - get amount of connected devices
- connlst    - get list of connected devices (their IPs)
- banlist    - get the ban list
- ban <IP>   - ban
- unban <IP> - unban
- serverinfo - get basic information about host server
- restart    - restart (reboot) entire server
- reboot     - alias of restart
```