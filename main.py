import discord
from tts import virtual_response

adjusted_noise = False

intents = discord.Intents.default()
intents.typing = True
intents.dm_typing = True
intents.members = True
intents.voice_states = True

client = discord.Client(intents=intents)

current_voice_connection = [None]


@client.event
async def on_connect():
    print('We have connected to Discord')


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):  # event that happens per any message.
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
    # virtual_response("hello")
    if "hello" in message.content.lower():
        await message.author.send("Hey")
    if "voice" in message.content.lower():
        print(f"{message.guild.voice_channels}")
        voice_channel = discord.utils.get(message.guild.voice_channels, name="General")
        await voice_channel.connect()


@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="general")
    await channel.send("Check ur DMs")
    await member.send("Welcome to the server, if you need help, just send a message here and we'll "
                      "try our best to solve your issue")
    overwrites = {
        member.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        member.guild.me: discord.PermissionOverwrite(read_messages=True),
        member: discord.PermissionOverwrite(read_messages=True)
    }
    voice_channel = await member.guild.create_voice_channel(member.name, overwrites=overwrites)

    print(f"{member} joined the {member.guild} server")


@client.event
async def on_member_remove(member):
    voice_channel = discord.utils.get(member.guild.voice_channels, name=member.name)
    await voice_channel.delete(reason="Member Left Server")

@client.event
async def on_voice_state_update(member, before, after):
    if current_voice_connection[0] is None:
        print(current_voice_connection[0])
    else:
        print(current_voice_connection[0])
        current_voice_connection[0].disconnect()
    print(client.voice_clients)
    current_voice_connection[0] = await after.channel.connect()


client.run('NzY5NTA0ODE1OTYwMTYyMzM0.X5P_NA.YI_Zs3FiLMn-aIeLDv9Lz-Hs5B4')
