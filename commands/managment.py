from re import search

from discord.ext import commands

from .tools import execute, serialize_ctx, validate_ip

@commands.command()
async def banlist(ctx) -> None:
    """send list of banned IPs"""
    tmp = execute('firewall-cmd --zone=public --list-rich-rules').strip()
    if not tmp:
        await ctx.send('Banlist is blank!')
    else:
        pattern = r'source address="(\d+\.\d+\.\d+\.\d+)"'
        result = ''
        for line in tmp.split('\n'):
            match = search(pattern, line)
            print(match)
            result += match.group(1) + '\n'
        await ctx.send('Banlist:\n' + result)


@commands.command()
@validate_ip
async def ban(ctx, ip: str) -> None:
    """ban IP connection; provide correct IP to ban"""
    addStatus = execute(f'firewall-cmd --zone=public --add-rich-rule=\'rule family="ipv4" source address="{ip}" drop\' --permanent')
    addStatus = 'ERR' if not addStatus else addStatus.upper()
    reloadStatus = execute('firewall-cmd --reload')
    reloadStatus = 'ERR' if not reloadStatus else reloadStatus.upper()
    execute(f'ss -K dst {ip}')
    await ctx.send(f'add firewall rule: {addStatus}\nreload firewall: {reloadStatus}\ndevice kicked out: SUCCESS')


@commands.command()
@validate_ip
async def unban(ctx, ip: str) -> None:
    """unban IP connection; provide correct IP to unban"""
    removeStatus = execute(f'firewall-cmd --zone=public --remove-rich-rule=\'rule family="ipv4" source address="{ip}" drop\' --permanent')
    removeStatus =  'ERR' if not removeStatus else removeStatus.upper()
    reloadStatus = execute('firewall-cmd --reload')
    reloadStatus = 'ERR' if not reloadStatus else reloadStatus.upper()
    await ctx.send(f'remove firewall rule: {removeStatus}\nreload firewall: {reloadStatus}')


@commands.command()
async def reboot(ctx) -> None:
    """reboot server"""
    await ctx.send('Going to reboot the server')
    serialize_ctx(ctx)
    execute('reboot')