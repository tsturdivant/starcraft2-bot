# Starcraft 2 Bot  

Starcraft 2 Bot is a Python program using the python-sc2 api to run a bot that will automatically play a game of Starcraft 2!


## Installation

Starcraft 2 Bot requires [python-sc2](https://github.com/Dentosal/python-sc2) to run.

Install the dependencies:

```sh
$ pip install --user --upgrade sc2
```

Click on the link above to view the GitHub repo for python-sc2.  

You will also need to install Starcraft 2, which you can get for free [here!](https://www.blizzard.com/en-us/download)

##### Note:
If you receive the error: 
```sh
ERROR:asyncio:Unclosed client session client_session: 
<aiohttp.client.ClientSession object at 0x10c8df588>
```
You may need a different version. Using the following command should fix the issue: 
```sh
$ pip install --upgrade --force-reinstall https://github.com/Dentosal/python-sc2/archive/develop.zip
```

## Running 
To run the bot simply run the program through terminal!

Some options you may want to change in the following block of code: 
```sh
run_game(maps.get("AbyssalReefLE"), [
    Bot(Race.Protoss, protossBot()),
    Computer(Race.Terran, Difficulty.{difficulty})
], realtime={booleanValue}) # realtime boolean for if you want sped up or real time
```
  - Difficulty.{difficulty}: can be Easy, Medium, or Hard
  - realtime={booleanValue}: True for running in real time, False for fast-forwarding
## Feedback
Please feel free to leave any feedback on the bot, let me know what kind of bot you 
create, and let me know if you think there are any changes that should be made. 



