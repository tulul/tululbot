# TululBot

## User Guide
### Command List
**/ngelely**\<space\>\<keywords\> - Returns google search with given keywords

**/wiki**\<space\>\<keywords\> - Try to return wiki page with given keywords

**/who** - Know your tululbot

## Development Guide

### How to set up your machine

1. Make sure you have Python on your system.

1. Install [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/) to make it easier working with [virtualenv](https://virtualenv.pypa.io/en/latest/).  We need virtualenv because Tululbot uses Python 3, whereas most systems still use Python 2. Virtualenv makes it easy to manage different Python versions along with their libraries. There are many ways to install virtualenvwrapper. One of the easiest wayss is to use Pip.
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

1. Before running the app, you have to set environment variables. Those variables will be used to configure the app. Again, there are many ways to do this and one of them is to use virtualenv's `postactivate` and `predeactivate` hook.

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

### How to Contribute

If you want to write new features to TululBot or fix bugs, that's great! Here is a step-by-step guide to contribute to TululBot's development.

#### General Flow

1. You need an issue on GitHub about your contribution. This can be a bug report (in which case your contribution is the bug fix) or feature suggestion (in which case your contribution is the implementation). If your contribution is a about new issue you want to raise, create a new issue on GitHub.

1. Create a new branch on which you write your code. Use any branch name as you which. For example, `cool-feature`:
   ```bash
   git checkout -b cool-feature
   ```
1. Implement your contribution in the branch.

1. Periodically, and after you finished writing the code, pull the latest changes from master:
   ```bash
   git pull --rebase origin master
   ```

   Fix any conflicts that may arise.

1. After you really finished writing the code, commit your changes. You may create one or more commits.

1. Push the feature branch to `origin`:
   ```bash
   git push origin cool-feature
   ```
1. Create a new pull request on GitHub for `cool-feature` branch to be merged to `master`. Refer the issue number in the pull request description.

1. Wait for other tulul members to review your contribution.

1. If they approve your contribution, congrats! You may commit your contribution to master. First, don't forget to rebase your branch against master:

   ```bash
   git pull --rebase origin master
   ```

   Again, fix any conflicts that may arise.

1. Then, clean up your commits. Do a interactive rebase (please google this term).
   ```bash
   git rebase -i origin/master
   ```

   You can pick, fix up, squash, or reorder the commits, or anything in any way you like. For each commit you want to include:

   - If necessary, rewrite the commit message to a more meaningful one.
   - If your contribution consists of a single commit, append `Resolve #X` to your commit message, where `X` is the issue number. If your contribution consists of multiple commits, append it to the last commit. For the other commits, append `Part of #X`.

1. Force-push your feature branch to origin:

   ```bash
   git push -f origin cool-feature
   ```

1. Checkout master:

   ```bash
   git checkout master
   ```

1. Merge your changes to master:

   ```bash
   git merge cool-feature
   ```

1. Push master:

   ```bash
   git push origin master
   ```

   Note that your pull request will be automatically closed.

1. You may safely delete your feature branch:

   ```bash
   git branch -D cool-feature
   ```

   Also delete your feature branch on origin from GitHub.

   ```bash
   git push origin :cool-feature
   ```

1. Done!

#### Special Cases

In case you want to commit a really minor fix, you may skip all above steps and directly push to master. For example, fixing typos, fixing whitespaces, super minor bug you spotted in your previous commits, etc. Remeber, our development process model is **Leaderless Agile**. Don't over-abuse this rule. With great power, comes great responsibility.
