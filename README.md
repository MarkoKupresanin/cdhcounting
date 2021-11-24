# Chaotic Destiny Counting Bot
### Created by: KaptainKermit1#1191

___
#### Necessary requirements to run the bot can be found in the [requirements.txt](https://github.com/MarkoKupresanin/cdhcounting/blob/main/requirements.txt) file. 
#### Python version 3.8.6 is recommended

___

## Environment variables:

#### In a ``.env`` file there are two variables that are necessary to use the bot.
1. ``PTERODACTYL_API_KEY  `` --> An API key created by the Pterodactyl panel you are using.
2. ``BOT_TOKEN`` --> The Discord Bot token which can be generated [here](https://discord.com/developers/applications).

## How to run

1. #### In your terminal/command prompt:
> ### MacOS/Linux: 
> ``pip3 install -r requirements.txt``
> ### Windows:
> ``pip install -r requirements.txt``

2. #### Then start the bot with this command:
> ### MacOS/Linux:
> ``python3 main.py``
> ### Windows
> ``python main.py``
___

## How to use:
#### Using the default prefix of ``c!`` you can run the ``c!help`` command to see all the help commands.

### Setting up the counting game:
1. In your Discord server, run this command:
> ``c!maketable``
> *Ignore any TypeError that may show up in the terminal*
2. Next run this command to initialize the game:
> ``c!initializeGame [counting_channel_ID]``
3. *Optional*: Configuring additional settings
> Run ``c!updateSettings [newID] [failBool] [newAuthorLoss] [newNumberLoss] [newProfit]``
#### Parameter explanation:
* **newID** --> New counting channel ID, if you don't want to change this, put the same ID you are already using. 
* **failBool** --> Either true or false, true meaning the game will reset if someone messes up the count, false to continue the game after a fail.
* **newAuthorLoss** --> Integer value greater than 0, this is the amount of points which will be taken off if someone counts twice in a row.
* **newNumberLoss** --> Integer value greater than 0, this is the amount of points which will be taken off if someone counts the wrong number.
* **newProfit** --> Integer value greater than 0, this is the amount of points which will be added for a successful count.
##### **NOTE: If you wish to only change one setting, just fill in the other parameters with what you already have set up.**
##### *If you ever forget the current settings you have, just run ``c!showsettings``.*


