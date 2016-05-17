# TululBot ![TululBot Build Status](https://travis-ci.org/tulul/tululbot.svg) [![Coverage Status](https://coveralls.io/repos/github/tulul/tululbot/badge.svg?branch=master)](https://coveralls.io/github/tulul/tululbot?branch=master) [![Stories in Ready](https://badge.waffle.io/tulul/tululbot.png?label=ready&title=Ready)](https://waffle.io/tulul/tululbot)

![TululBot Command Preview](https://cdn.rawgit.com/tulul/tululbot/master/assets/img/preview.gif)

## User Guide
### Command List
**/leli** - Returns search result with given keywords

**/quote** - Get random quote from [our database](https://github.com/tulul/tulul-quotes)

**/slang** - Lookup slang word definition; the result may surprise you!

**/hotline** - Dev group only

**/who** - Know your tululbot

## Development Guide

### How to set up your machine

1. Setup your Python virtual environment. There are two ways to do this. One is via [virtualenvwrapper][virtualenvwrapper] and the other one is via [pyenv][pyenv]. If you decided to use [virtualenvwrapper][virtualenvwrapper], here are the steps you may follow:

    1. Make sure you have Python on your system.

    1. Install [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/) to make it easier working with [virtualenv](https://virtualenv.pypa.io/en/latest/). We need virtualenv because Tululbot uses Python 3, whereas most systems still use Python 2. Virtualenv makes it easy to manage different Python versions along with their libraries. There are many ways to install virtualenvwrapper. One of the easiest ways is to use Pip.
       ```bash
       pip install virtualenvwrapper
       ```

       [Pip](https://pip.pypa.io/en/latest/) is the default package manager for Python. It should already be installed if you have Python >= 2.7.9 or Python >= 3.4 on your system.

    1. Configure your virtualenvwrapper as described in [their docs](https://virtualenvwrapper.readthedocs.org/en/latest/install.html#shell-startup-file).

    1. Make sure you have Python 3 installed on your system. This can be done in many ways. For instance, in OSX, you may install it with Homebrew
       ```bash
       brew install python3
       ```

       **UPDATE**:
       Homebrew's `python3` is already updated to Python 3.5. Since we're using Python 3.4, you might want to use [pyenv][pyenv] instead.

    1. [Create a Python 3 virtual environment](https://virtualenvwrapper.readthedocs.org/en/latest/command_ref.html#mkvirtualenv) and clone this repository.
       ```bash
       mkvirtualenv -p /path/to/python3/binary name_of_your_virtualenv
       git clone git@github.com:tulul/tululbot.git /path/to/your/tululbot/project/directory
       ```

    1. Activate the virtual environment you've just created.
       ```bash
       workon name_of_your_virtualenv
       ```

    If you'd like to use [pyenv][pyenv] instead, here are the steps you may follow:

    1. Install [pyenv][pyenv] and its [pyenv-virtualenv][pyenv-virtualenv] plugin. Configure them as written in their docs.

    1. Install Python 3.4 with `pyenv`, create virtual environment, and clone this repository.
       ```bash
       pyenv install 3.4.3
       pyenv virtualenv 3.4.3 name_of_your_virtualenv
       git clone git@github.com:tulul/tululbot.git /path/to/your/tululbot/project/directory
       ```

    1. Activate the virtual environment you've just created.
       ```bash
       pyenv activate name_of_your_virtualenv
       ```

1. Navigate to the directory where you've cloned this repo and install all its dependencies.
   ```bash
   cd /path/to/your/tululbot/project/directory
   pip install -r requirements.txt
   ```

   Dependencies are all listed in `requirements.txt`. To re-generate this file (after you've installed new packages), simply run `pip freeze > requirements.txt`. For Linux users, if you have a problem installing the dependencies (PyYaml in particular), install the package `python3-dev` or `python3-devel` first.

1. Create `.env` file under the project root directory. It contains the configuration variables for the application. Sample `.env` file can be found in `.env.example`.

1. Run the app
   ```bash
   python manage.py runserver
   # or
   ./manage.py runserver
   ```

1. The app is now running! Try to play around with it by simulating a webhook request. For instance, try this:
   ```bash
   curl --data '{"update_id": 12345,"message":{"text":"/who","chat":{"id":-12345},"message_id":1}}' --header "Content-Type: application/json" http://127.0.0.1:5000/<YOUR TELEGRAM BOT TOKEN IN .ENV>
   ```

   You should get a JSON response that looks like this:
   ```json
   {
     "chat_id": -12345,
     "disable_web_page_preview": "true",
     "method": "sendMessage",
     "reply_to_message_id": 1,
     "text": "TululBot v0.1.0\n\nEnhancing your tulul experience since 2015\n\nContribute on https://github.com/tulul/tululbot\n\nWe're hiring! Contact @iqbalmineraltown for details"
   }
   ```

   As you can see, the url endpoint is determined by the `TELEGRAM_BOT_TOKEN` config variable. This is actually [recommended by Telegram](https://core.telegram.org/bots/api#setwebhook).

[virtualenvwrapper]: https://pypi.python.org/pypi/virtualenvwrapper
[pyenv]: https://github.com/yyuu/pyenv
[pyenv-virtualenv]: https://github.com/yyuu/pyenv-virtualenv

### How to run the tests/linters

1. Make sure you already installed [pytest][pytest] and [flake8][flake8]. Both are listed in `requirements.txt` so if you followed the instructions to setup your machine above then they should already be installed.

1. Put `.env` file under your `tests` directory.

1. You can run the tests and linters with `python manage.py test` and `python manage.py lint` respectively. If you remember that `manage.py` is actually executable, you may run it with `./manage.py COMMAND`.

1. To run both linters and tests in one command, you can use `python manage.py check`. This is useful to check your code before making a pull request.

1. For more info on what you can do with `manage.py`, run `python manage.py --help`.

[pytest]: http://pytest.org/latest/
[flake8]: https://pypi.python.org/pypi/flake8

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

In case you want to commit a really minor fix, you may skip all above steps and directly push to master. For example, fixing typos, fixing whitespaces, super minor bug you spotted in your previous commits, etc. Remember, our development process model is **Leaderless Agile**. Don't over-abuse this rule. With great power, comes great responsibility.
