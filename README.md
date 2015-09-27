# Tululbot

## How to contribute

1. Make sure you have Python on your system.

1. Install [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/) to make it easier working with [virtualenv](https://virtualenv.pypa.io/en/latest/).
   We need virtualenv because Tululbot uses Python 3, whereas most systems still use Python 2. Virtualenv makes it easy to manage different Python versions along
   with their libraries.

1. Make sure you have Python 3 installed on your system. This can be done in many ways. For instance, in OSX, you may install it with Homebrew
   ```bash
   brew install python3
   ```

1. [Create a Python 3 virtual environment](https://virtualenvwrapper.readthedocs.org/en/latest/command_ref.html#mkvirtualenv)
   and clone this repository.

1. Activate the virtual environment you've just created.

1. Navigate to the directory where you've cloned this repo and install all its dependencies by `pip install -r requirements.txt`.

   Dependencies are all listed on `requirements.txt`. To generate this file, simply run `pip freeze > requirements.txt`.

   [Pip](https://pip.pypa.io/en/latest/) is the default package manager for Python. It should be installed by default on Python 2.7 and Python 3.x

1. Set configuration vars as environment variables. For now, just do this:
   ```
   export TELEGRAM_BOT_TOKEN=somerandomstring
   export DEBUG=true
   export LOG_LEVEL=DEBUG
   ```

1. Run the app by `python app.py`

1. The app is now running! Try to play around with it by simulating a webhook request. For instance, try this:
   ```bash
   curl --data '{"update_id": 12345,"message":{"text":"/wiki potus","chat":{"id":-12345},"message_id":1}}' --header "Content-Type: application/json" http://127.0.0.1:5000/somerandomstring
   ```

   As you can see, the url endpoint is determined by the `TELEGRAM_BOT_TOKEN` config var. This is recommended by Telegram.
