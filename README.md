# JoJo Bot
It understands over 60 JoJo references by text and replies with an appropriate photo
This Bot Sends You The JoJo Reference In PNG or GIF format as Response to Your Text Version of This Reference. The digits from 0 to 9 are exceptions, if you type any of them it will get you my JoJo association to this number.


## Input: 
- jojo reference


## Output: 
- photo of it


## Setup

### Local Development (polling mode)

1. Clone the repository:
   <br>git clone https://github.com/justamanwho/JoJo-bot.git
   <br>cd JoJo-bot


2. Create and activate virtual environment:
   <br>python -m venv venv
   <br>source venv/bin/activate


3. Install dependencies:
   <br>pip install -r requirements.txt


4. Create a `.env` file with your bot token:
   <br>BOT_NAME=your_telegram_bot_name
   <br>BOT_TOKEN=your_telegram_bot_token


5. In `app.py`, comment out the webhook section and uncomment `bot.infinity_polling()`.


6. Run the bot:
   <br>python app.py

### Production Setup (webhook mode)

1. Clone the repository on your server:
   git clone https://github.com/justamanwho/JoJo-bot.git
   <br>cd JoJo-bot


2. Create and activate virtual environment:
   <br>python -m venv venv
   <br>source venv/bin/activate


3. Install dependencies:
   <br>pip install -r requirements.txt


4. Create an `.env` file:
   <br>BOT_NAME=your_telegram_bot_name
   <br>BOT_TOKEN=your_telegram_bot_token
   <br>BOT_WEBHOOK=https://yourdomain/jojo-webhook


5. Copy the systemd service file from the `setup/` directory:
   <br>sudo cp setup/jojo-bot.service /etc/systemd/system/


6. Your server must have a public IP or domain. See `setup/webhook-example.py` for an example webhook endpoint 
   (can be deployed on a portfolio, a website, or any backend).


7. Start and enable the service:
   <br>sudo systemctl daemon-reload
   <br>sudo systemctl start jojo-bot.service
   <br>sudo systemctl enable jojo-bot.service


8. Check status and logs:
   <br>sudo systemctl status jojo-bot.service
   <br>sudo journalctl -u jojo-bot.service -f


## Links and Sources:
- telegram bot - https://t.me/jojo_references_bot

<img width="382" height="1009" alt="JoJo-bot" src="https://github.com/user-attachments/assets/29f291b0-e193-4e70-9c33-afa01265d3ad" />


## To do list:
