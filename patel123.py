import time
import json
import requests
import random
import telebot
from telebot import types
import os

# Load the API key from a file or set a default
def load_api_key():
    if os.path.exists("api_key.txt"):
        with open("api_key.txt", "r") as file:
            return file.read().strip()
    return "SG_6d3487d4b33987f2"  # Default key (if necessary)

# Save the API key to a file
def save_api_key(new_key):
    with open("api_key.txt", "w") as file:
        file.write(new_key)

# Bot Token and API Key Configuration
bot_token = "7927841285:AAEum9YFyWfT4-xpwSjX4O3bwzES6z0-yHk"  # Replace with your actual main bot token
segmind_api_key = load_api_key()  # Load the initial API key

# Initialize the bot
bot = telebot.TeleBot(bot_token)

# List of admin IDs
ADMIN_IDS = [1989234528, 1989234528]  # Example admin user IDs

# Required groups
required_groups = [
    {"name": "@patel_ji47", "link": "https://t.me/patel_ji47"},
    {"name": "@flashmainchannel", "link": "https://t.me/flashmainchannel"}
]

# Global dictionaries to store user data
user_language = {}
user_shares = {}
user_message_ids = {}
user_in_help_mode = {}
approved_users = set()  # Store approved users
free_to_use = True  # Allow all users to use the bot freely

# Passwords and file links for each feature
password_links = {
    "obb": "❌❌❌",
    "ddos": "❌❌❌",
    "mod_apk": "❌❌❌",
    "free_src": "❌❌❌",
    "file_program": "❌❌❌"
}

file_links = {
    "obb": "https://drive.google.com/file/d/15ooyoNWk6_Wy2Ac2FCuF3lpmyJy8mbHN/view?usp=drivesdk",
    "ddos": "❌❌❌❌❌❌",
    "mod_apk": "❌❌❌❌❌❌",
    "free_src": "❌❌❌❌❌❌",
    "file_program": "❌❌❌❌❌❌"
}

# Function to track messages sent by the bot
def track_message(user_id, message):
    if user_id not in user_message_ids:
        user_message_ids[user_id] = []
    user_message_ids[user_id].append(message.message_id)

# Function to delete tracked messages
def delete_tracked_messages(user_id, chat_id):
    if user_id in user_message_ids:
        for message_id in user_message_ids[user_id]:
            try:
                bot.delete_message(chat_id, message_id)
            except Exception as e:
                print(f"Error deleting message {message_id}: {e}")
        user_message_ids[user_id] = []  # Clear the stored message IDs after deletion

# Function to check if the user is in required groups
def is_user_in_required_groups(user_id):
    for group in required_groups:
        try:
            member_status = bot.get_chat_member(group['name'], user_id).status
            if member_status in ['left', 'kicked']:
                return False
        except Exception as e:
            print(f"Error checking group {group['name']}: {e}")
            return False
    return True

# Function to send user details to all admins
def send_user_info_to_admins(user):
    user_id = user.id
    username = user.username if user.username else "No username"
    first_name = user.first_name
    last_name = user.last_name if user.last_name else "No last name"
    is_bot = "Yes" if user.is_bot else "No"
    message = f"New User Info:\nUser ID: {user_id}\nUsername: {username}\nFirst Name: {first_name}\nLast Name: {last_name}\nIs Bot: {is_bot}\n\n"

    for group in required_groups:
        try:
            member_status = bot.get_chat_member(group['name'], user_id)
            is_admin = "Yes" if member_status.status == "administrator" else "No"
            message += f"Group: {group['name']}, Admin: {is_admin}, Status: {member_status.status}\n"
        except Exception as e:
            message += f"Error checking group {group['name']}: {e}\n"

    for admin_id in ADMIN_IDS:
        bot.send_message(admin_id, message)

# Start command handler
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    send_user_info_to_admins(message.from_user)

    welcome_text = f"स्वागत है {user_name}! कृपया नीचे दिए गए आवश्यक समूहों में शामिल हों:\n👇👇👇👇\n" if user_language.get(user_id) == 'hi' else f"Welcome {user_name}! Please join the required groups below:\n👇👇👇👇\n"
    join_buttons = telebot.types.InlineKeyboardMarkup(row_width=1)
    for group in required_groups:
        join_buttons.add(telebot.types.InlineKeyboardButton(f"Join {group['name']}", url=group['link']))
    
    sent_message = bot.send_photo(message.chat.id, open('welcome_image.jpg', 'rb'), caption=welcome_text, reply_markup=join_buttons)
    track_message(user_id, sent_message)

    # Check button after groups
    check_button = telebot.types.InlineKeyboardMarkup()
    check_button.add(telebot.types.InlineKeyboardButton('✅ चेक' if user_language.get(user_id) == 'hi' else '✅ Check', callback_data='check_groups'))
    sent_message = bot.send_message(message.chat.id, "समूह में शामिल होने के बाद 'चेक' पर क्लिक करें।" if user_language.get(user_id) == 'hi' else "Click 'Check' after joining the group.", reply_markup=check_button)
    track_message(user_id, sent_message)

# Group verification handler
@bot.callback_query_handler(func=lambda call: call.data == 'check_groups')
def check_groups(call):
    user_id = call.from_user.id
    if is_user_in_required_groups(user_id):
        bot.send_message(call.message.chat.id, "आपने आवश्यक समूहों को जॉइन कर लिया है। अब कृपया अपनी भाषा चुनें।" if user_language.get(user_id) == 'hi' else "Great! You have joined the required groups. Now please select your language.")
        language_selection(call.message)
    else:
        bot.send_message(call.message.chat.id, "आपने सभी आवश्यक समूहों को जॉइन नहीं किया है। कृपया पहले समूहों में शामिल हों।" if user_language.get(user_id) == 'hi' else "You have not joined all the required groups. Please join the groups first.")

# Language selection function
def language_selection(message):
    language_buttons = telebot.types.InlineKeyboardMarkup()
    language_buttons.add(telebot.types.InlineKeyboardButton('🇬🇧 English', callback_data='lang_en'))
    language_buttons.add(telebot.types.InlineKeyboardButton('🇮🇳 हिंदी', callback_data='lang_hi'))
    bot.send_message(message.chat.id, "कृपया अपनी भाषा चुनें:" if user_language.get(message.chat.id) == 'hi' else "Please select your language:", reply_markup=language_buttons)

# Language selection handler
@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def set_language(call):
    user_id = call.from_user.id
    selected_lang = call.data.split('_')[-1]
    user_language[user_id] = selected_lang
    bot.send_message(call.message.chat.id, "आपने हिंदी चुनी है। 🇮🇳" if selected_lang == 'hi' else "You have selected English. 🇬🇧")
    show_feature_options(call.message)

# Show feature options after language selection
def show_feature_options(message):
    feature_options = telebot.types.InlineKeyboardMarkup()
    feature_options.add(
        telebot.types.InlineKeyboardButton('BGMI', callback_data='feature_bgmi'),
        telebot.types.InlineKeyboardButton('AI generate generate', callback_data='feature_ai')
    )
    bot.send_message(message.chat.id, "Select an option:" if user_language.get(message.chat.id) == 'en' else "एक विकल्प चुनें:", reply_markup=feature_options)

# BGMI options after selection
@bot.callback_query_handler(func=lambda call: call.data == 'feature_bgmi')
def show_bgmi_features(call):
    user_id = call.message.chat.id
    feature_buttons = telebot.types.InlineKeyboardMarkup(row_width=2)
    feature_buttons.add(
        telebot.types.InlineKeyboardButton('⚡ DDos File🚀', callback_data='ddos_file'),
        telebot.types.InlineKeyboardButton('📦 OBB File', callback_data='obb'),
        telebot.types.InlineKeyboardButton('🛠️ Mod .APK Loader', callback_data='mod_apk1'),
        telebot.types.InlineKeyboardButton('💻 Free SRC', callback_data='free_src1'),
        telebot.types.InlineKeyboardButton('📁 File Program', callback_data='file_program1'),
        telebot.types.InlineKeyboardButton('❓ Help', callback_data='help1'),
        telebot.types.InlineKeyboardButton('🌟 VIP Feature', callback_data='vip_feature')
    )
    bot.send_message(call.message.chat.id, "Select a BGMI option:" if user_language.get(user_id) == 'en' else "BGMI विकल्प चुनें:", reply_markup=feature_buttons)

# AI options after selection
@bot.callback_query_handler(func=lambda call: call.data == 'feature_ai')
def show_ai_features(call):
    ai_buttons = telebot.types.InlineKeyboardMarkup()
    ai_buttons.add(telebot.types.InlineKeyboardButton("🖼️ Generate Image", callback_data="generate_image"))
    bot.send_message(call.message.chat.id, "Choose an AI option:" if user_language.get(call.message.chat.id) == 'en' else "AI विकल्प चुनें:", reply_markup=ai_buttons)

@bot.callback_query_handler(func=lambda call: call.data == 'generate_image')
def generate_image_handler(call):
    user_id = call.from_user.id
    username = call.from_user.first_name
    start_message = (
        f"👋 Hello {username}!\n\n"
        "This bot can generate realistic images from a text query or a photo using AI. Use the command /gen followed by your prompt. For example, /gen YourPromptHere 🙂\n\n"
        "If you're unsure what to generate, visit our channel for examples and enjoy ❤️\n\n"
        "Links to the channel are available via the buttons below 👇"
    )
    
    bot.send_message(call.message.chat.id, start_message)

    # After sending the start message, prompt the user to send a description
    bot.send_message(call.message.chat.id, "Please send me a description to generate an image.")

# Handlers for each button with unique messages
@bot.callback_query_handler(func=lambda call: call.data in ['ddos_file', 'obb', 'mod_apk', 'free_src', 'file_program'])
def file_process_handler(call):
    button_name = call.data.replace("_file", "")
    user_id = call.message.chat.id
    lang = user_language.get(user_id, 'en')
    
    # First, prompt the user to share the bot
    share_buttons = telebot.types.InlineKeyboardMarkup()
    share_buttons.add(
        telebot.types.InlineKeyboardButton('Share Bot', switch_inline_query="Share this bot with friends"),
        telebot.types.InlineKeyboardButton('Check Share', callback_data=f'check_share_{button_name}')
    )
    bot.send_message(user_id, f"Please share '@Bgmi_hack_official_bot' with 5 people to get the {button_name}." if lang == 'en' else f"{button_name} प्राप्त करने के लिए कृपया '@Bgmi_hack_official_bot' को 5 लोगों के साथ शेयर करें।", reply_markup=share_buttons)
    user_shares[user_id] = button_name  # Store button info for user

# Check if the user has shared the bot and provide file link
@bot.callback_query_handler(func=lambda call: call.data.startswith('check_share_'))
def check_user_share(call):
    user_id = call.message.chat.id
    button_name = call.data.split('_')[-1]
    
    if user_shares.get(user_id) == button_name:
        # Provide file link for the specific button
        file_link = file_links.get(button_name, "No file link set")
        bot.send_message(call.message.chat.id, f"Here is the link for {button_name}: {file_link}")
        
        # Provide option to check the password
        password_check_buttons = telebot.types.InlineKeyboardMarkup()
        password_check_buttons.add(telebot.types.InlineKeyboardButton('Check Password', callback_data=f'check_password_{button_name}'))
        bot.send_message(call.message.chat.id, "Click 'Check Password' to get the password.", reply_markup=password_check_buttons)
    else:
        bot.send_message(call.message.chat.id, "Please start by clicking on the buttons.")

# Check if user shared enough and send the password
@bot.callback_query_handler(func=lambda call: call.data.startswith('check_password_'))
def check_password(call):
    user_id = call.message.chat.id
    feature = call.data.split('_')[-1]

    password_link = password_links.get(feature, "No password set")
    bot.send_message(call.message.chat.id, f"Here is the password for {feature}: {password_link}")

    # Option to restart or share again
    share_and_restart_buttons = telebot.types.InlineKeyboardMarkup()
    share_and_restart_buttons.add(
        telebot.types.InlineKeyboardButton('Share Bot', switch_inline_query="Share this bot with friends"),
        telebot.types.InlineKeyboardButton('Restart Bot', callback_data='restart_bot')
    )
    bot.send_message(call.message.chat.id, "Click the button below to restart the bot or share it with others.", reply_markup=share_and_restart_buttons)

# Handle bot restart and delete previous messages
@bot.callback_query_handler(func=lambda call: call.data == 'restart_bot')
def restart_bot(call):
    user_id = call.from_user.id
    delete_tracked_messages(user_id, call.message.chat.id)
    send_welcome(call.message)

# Help and VIP feature handlers
@bot.callback_query_handler(func=lambda call: call.data == 'help')
def help_button_process(call):
    help_message = (
        "🆘 Help Menu:\n"
        "Here are the commands you can use:\n"
        "/start - Start the bot and see the welcome message.\n"
        "/gen <your_prompt> - Generate an image based on your text prompt.\n"
        "/key <new_api_key> - Change the Segmind API key (admin only).\n"
        "/current_key - Check the current Segmind API key (admin only).\n"
        "/approve <user_id> - Approve a user to access the bot (admin only).\n"
        "/remove <user_id> - Remove a user from accessing the bot (admin only).\n"
        "/free - Allow all users to use the bot freely (admin only).\n"
        "/stop - Stop all users from using the bot (admin only).\n"
        "/help - Show this help message."
    )
    bot.send_message(call.message.chat.id, help_message)

@bot.message_handler(commands=['key'])
def set_api_key(message):
    if message.from_user.id in ADMIN_IDS:
        if len(message.text.split()) > 1:
            new_api_key = message.text.split()[1]
            global segmind_api_key
            segmind_api_key = new_api_key  # Update the global variable
            save_api_key(new_api_key)  # Save the new key to a file
            bot.reply_to(message, "✅ API key updated successfully.")
        else:
            bot.reply_to(message, "⚠️ Please provide the new API key. Example: /key your_new_api_key")
    else:
        bot.reply_to(message, "🚫 You are not authorized to change the API key.")

@bot.message_handler(commands=['current_key'])
def current_key(message):
    bot.reply_to(message, f"🔑 Current Segmind API Key: `{segmind_api_key}`", parse_mode='Markdown')

# Function for generating images based on user input
@bot.message_handler(commands=['gen'])
def generate_image(message):
    user_id = message.from_user.id
    
    if user_id not in approved_users and not free_to_use:
        bot.send_message(message.chat.id, "🚫 You need admin approval to use this command.")
        return

    if len(message.text.split()) > 1:
        bot.send_chat_action(message.chat.id, 'upload_photo')
        random_seed = random.randint(1, 10000000000000000)
        user_prompt = ' '.join(message.text.split()[1:])
        payload = {
            "prompt": user_prompt,
            "negative_prompt": "(worst quality, low quality, normal quality, lowres, low details, oversaturated, undersaturated, overexposed, underexposed, grayscale, bw, bad photo, bad photography, bad art)++++, (watermark, signature, text font, username, error, logo, words, letters, digits, autograph, trademark, name)+, (blur, blurry, grainy), morbid, ugly, asymmetrical, mutated malformed, mutilated, poorly lit, bad shadow, draft, cropped, out of frame, cut off, censored, jpeg artifacts, out of focus, glitch, duplicate, (airbrushed, cartoon, anime, semi-realistic, cgi, render, blender, digital art, manga, amateur)++, (3D ,3D Game, 3D Game Scene, 3D Character), (bad hands, bad anatomy, bad body, bad face, bad teeth, bad arms, bad legs, deformities)++",
            "scheduler": "dpmpp_2m",
            "num_inference_steps": 25,
            "guidance_scale": 5,
            "samples": 1,
            "seed": random_seed,
            "img_width": 512,
            "img_height": 768,
            "base64": False
        }
        api_url = "https://api.segmind.com/v1/sd1.5-juggernaut"
        headers = {
            "x-api-key": segmind_api_key,
            "Content-Type": "application/json"
        }
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))
        
        if response.status_code == 200:
            image_data = response.content
            bot.send_photo(message.chat.id, image_data, reply_to_message_id=message.message_id)
        else:
            bot.reply_to(message, "An error occurred while generating the image.")
    else:
        bot.reply_to(message, "Please provide a prompt after the /gen command. For example, /gen YourPromptHere")

# Polling to keep the bot running
while True:
    try:
        bot.polling(timeout=60, long_polling_timeout=60)
    except requests.exceptions.ReadTimeout:
        time.sleep(15)
    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(15)
