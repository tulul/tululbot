# Tululbot

## User Guide
### Command List
**/ngelely**\<space\>\<keywords\> - Returns google search with given keywords

**/wiki**\<space\>\<keywords\> - Try to return wiki page with given keywords

**/who** - Know your tululbot

## Development Guide

### How to setup your machine

1. Make sure you have Python on your system.

1. Install [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/) to make it easier working with [virtualenv](https://virtualenv.pypa.io/en/latest/).  We need virtualenv because Tululbot uses Python 3, whereas most systems still use Python 2. Virtualenv makes it easy to manage different Python versions along with their libraries. There are many ways to install virtualenvwrapper. One of the easiest way is to use Pip.
   ```bash
   pip install virtualenvwrapper
   ```

   [Pip](https://pip.pypa.io/en/latest/) is the default package manager for Python. It should already be installed if you have Python 2.7 or Python 3.x on your system.

1. Configure your virtualenvwrapper as described in [their docs](https://virtualenvwrapper.readthedocs.org/en/latest/install.html#shell-startup-file).

1. Make sure you have Python 3 installed on your system. This can be done in many ways. For instance, in OSX, you may install it with Homebrew
   ```bash
   brew install python3
   ```

1. [Create a Python 3 virtual environment](https://virtualenvwrapper.readthedocs.org/en/latest/command_ref.html#mkvirtualenv) and clone this repository.
   ```bash
   mkvirtualenv -p /path/to/python3/binary name_of_your_virtualenv
   git clone git@github.com:tulul/tululbot.git /path/to/your/tululbot/project/directory
   ```

1. Activate the virtual environment you've just created.
   ```bash
   workon name_of_your_virtualenv
   ```

1. Navigate to the directory where you've cloned this repo and install all its dependencies.
   ```bash
   cd /path/to/your/tululbot/project/directory
   pip install -r requirements.txt
   ```

   Dependencies are all listed in `requirements.txt`. To generate this file, simply run `pip freeze > requirements.txt`.

1. Before running the app, you have to set environment variables. Those variables will be used to configure the app. Again, there are many ways to do this one of them is to use virtualenv's `postactivate` and `predeactivate` hook.

   Assuming you have set your `$WORKON_HOME` correctly, under `$WORKON_HOME/name_of_your_virtualenv/bin` directory you have `postactivate` and `predeactivate` files. Those two files will be executed by virtualenv after activating and before deactivating `name_of_your_virtualenv` respectively. Thus, in `postactivate`, you may put
   ```bash
   export TELEGRAM_BOT_TOKEN=somerandomstring
   export DEBUG=true
   export LOG_LEVEL=DEBUG
   ```
   and in `predeactivate` you may put
   ```bash
   unset TELEGRAM_BOT_TOKEN
   unset DEBUG
   unset LOG_LEVEL
   ```
   Make sure those two files are executable. Adjust the value of those variables as you please. You have to deactivate and activate your virtual environment for the changes to take place.

1. Run the app
   ```bash
   python app.py
   ```

1. The app is now running! Try to play around with it by simulating a webhook request. For instance, try this:
   ```bash
   curl --data '{"update_id": 12345,"message":{"text":"/wiki potus","chat":{"id":-12345},"message_id":1}}' --header "Content-Type: application/json" http://127.0.0.1:5000/somerandomstring
   ```

   As you can see, the url endpoint is determined by the `TELEGRAM_BOT_TOKEN` config var. This is actually [recommended by Telegram](https://core.telegram.org/bots/api#setwebhook).
