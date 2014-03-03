# CourseRevie.ws

__a Django project__

[![Build Status](https://travis-ci.org/coursereviews/coursereviews.png?branch=master)](https://travis-ci.org/coursereviews/coursereviews)

_Last updated: 8/8/13_

### Settings notes

4 settings files

- common.py (this is used in the other three using a wildcard import)
- development.py
- staging.py
- production.py

The DJANGO_SETTINGS_MODULE determines which of these files is used. Common.py is a dependency of the other three, and would never be set as the main settings file. 

For `wsgi.py` `DJANGO_SETTINGS_MODULE` defaults to `rocket.settings.production`. (doesn't matter much, since this is the production server hook)
For `manage.py` `DJANGO_SETTINGS_MODULE` defaults to `rocket.settings.development`.
As you can see below, I configured heroku to set `DJANGO_SETTINGS_MODULE` to `rocket.settings.production`.

To use the staging settings, manually set `DJANGO_SETTINGS_MODULE` to `rocket.settings.staging`.

Common.py should only hold indisputable settings that are not overriden in any of the other files. At this point it seems that I'd rather abandon DRY here in favor of DKY (don't kill yourself), because having sensible defaults in common.py leads to madness. It was crazy for a while where `debug = False` would be in common.py and then overriden in development.py. And that kind of thing would happen like 10 times, with both production.py and development.py overriding settings. It seems the easier solution is to have those settings set in their respective files, and leave common.py to the less controversial settings.

The only settings that should be set according to environment variables are ones that store __sensitive__ credentials (e.g. S3, mailgun, twitter keys). Sensitive here means that they relate to our production setup. For example, the keys to our developer twitter app are not sensitive. Those to our production app are. So I don't mind hardcoding the twitter developer app keys into the settings files, but I'll set the production keys as environment variables.

I'm willing to risk hardcoding arbitrary insensitive data (such as our AWS bucket name into the settings file) for the sake of simplicity.

### Heroku Deploy Notes

Branching from master into a temporary branch `staging` is a good idea. Remember to comment out less.js from `base.html` and switch over to the CDN bootstrap and jquery.

Static files deployment to S3 is done locally. The S3 connection is configured with environment variables. All of the following are required I think.

    export AWS_KEY=?????
    export AWS_SECRET=?????
    export AWS_STORAGE_BUCKET_NAME=static.rocketlistings.com
    export HEROKU_APP=rocket-listings

Don't forget to run `source ~/.bash_profile` or whatever.

To deploy

    fab deploy

Heroku config vars

    AWS_KEY:                      ??
    AWS_SECRET:                   ??
    SECRET_KEY:                   ??
    TWITTER_KEY:                  ??
    TWITTER_SECRET:               ??    
    AWS_STORAGE_BUCKET_NAME:      static.rocketlistings.com
    PYTHONPATH:                   fakepath # not sure if we still need this
    BUILDPACK_URL:                git://github.com/heroku/heroku-buildpack-python.git
    CLOUDAMQP_URL:                <set by heroku>
    DATABASE_URL:                 <set by heroku>
    DISABLE_INJECTION:            true # I don't remember setting this
    DJANGO_SETTINGS_MODULE:       rocket.settings.production
    HEROKU_POSTGRESQL_YELLOW_URL: <set by heroku>
    NEW_RELIC_LICENSE_KEY:        <set by heroku>
    NEW_RELIC_LOG:                <set by heroku>
    PGBACKUPS_URL:                <set by heroku>
    SENTRY_DSN:                   <set by heroku>


### Celery

Celery is a distributed task queue. We can use it for many things including scheduling routine work and running tasks in the background. [Docs here](http://docs.celeryproject.org/en/latest/getting-started/introduction.html).

Right now we are using RabbitMQ as a broker. To install:

    $ brew install rabbitmq

In a separate command line tab:
    
    $ rabbitmq-server

And in yet another tab:

    $ ./manage.py celeryd

Note: `./manage.py celeryd --loglevel=DEBUG` is often helpful if you're having problems.

### Project setup

Homebrew is a package manager for OS X. Read about it [here](http://mxcl.github.io/homebrew/). Install it, then run

    brew install python git sqlite rabbitmq node
    echo "export PATH=/usr/local/share/npm/bin:$PATH" >> ~/.bash_profile
    npm install -g less
    source ~/.bash_profile

If running `which python` gives you `/usr/local/bin/python`, you're good. Otherwise you have a problem with your path variable and homebrew installation (`brew doctor` helps).

Clone the project

    git clone git@github.com:Rocket-Listings/Rocket.git

Now install all of the python package dependencies by going:

    pip install -r reqs/development.txt

Now setup the sqlite3 database with our Fabric command.

    fab resetdb

After setting up the db, this command loads an admin test user into the database

__username__ chucknorris

__password__ test

### Development Notes

Start the server by running

    python manage.py runserver

In your browser, load `http://localhost:8000/` to see the site.

If you want to show others the site you can run:

    python manage.py runserver 0.0.0.0:8000

And then you can direct them to your ip (found using `ifconfig`) in their browser with `:8000` added to the end. This only works when you're on the same network as the person you want to show it to.

If you're tired of typing `python manange.py`,

you can make `manage.py` executable by running:

    chmod +x manage.py

And now you can instead type:

    ./manage.py runserver

Sort of faster

Show the server off to others on the LAN by making your server public

    ./manage.py runserver 0.0.0.0:8000

Then point them to your ip address (with the `:8000`).

### Facebook and Twitter Integration Notes

Facebook and Twitter are now connected, but due to url requirements, we have to access them from a "real" url rather than `localhost` or `127.0.0.1`.  Right now, they're set up to run at `http://local.rocketlistings.com:8000`.  To make this possible:

    sudo nano /etc/hosts

Add this line to the list:

    127.0.0.1       local.rocketlistings.com

Now access the site at `local.rocketlistings.com:8000`

The FB app key and secret are in users.js with the FB init code.  The Twitter app keys and secrets are in settings/common.py.  We are using [Twython](https://github.com/ryanmcgrath/twython) for Twitter integration.  [Docs here](https://twython.readthedocs.org/en/latest/).

All Twitter requests start like this:

    OAUTH_TOKEN = UserProfile.objects.get(user=request.user).OAUTH_TOKEN
    OAUTH_TOKEN_SECRET = UserProfile.objects.get(user=request.user).OAUTH_TOKEN_SECRET
    twitter = Twython(settings.TWITTER_KEY, settings.TWITTER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

### Fabric Command Reference 

(run from project root)

To completely reset your development database and load demo fixtures

    fab resetdb 

### Sublime Text Notes

Open up Sublime text and in the top menu go `Project -> Add Folder to Project`, and select `Rocket-Listings-Django`. After this we save the project by going `Project -> Save project as..` and saving the project file inside `Rocket-Listings-Django`, naming it whatever you want. From now on, to open the project, you can open Sublime Text, and hit `cmd+ctrl+P` to open a dialog to select a project. Clicking on the project you want to open will open it. Having Sublime Text Projects allow you to have all kinds of cool stuff the file browser sidebar among other things.

Pimp out your `.sublime-project` file like this

    {
        "folders":
        [
            {
                "path": "<KEEP THIS FIELD THE SAME>",
                "file_exclude_patterns":[
                    "*.sublime-project",
                    "*.sublime-workspace",
                    "*.css",
                    ".gitignore"
                ],
                "folder_exclude_patterns": [
                    "img",
                    "static_collected"
                ]
            }
        ]
    }

You should have much less visual clutter when looking through your project folders now.

### CSS Notes

Use classes in markup for styling, use ids for javascript hooks. Classnames should be lowercase with dashes between words. We use [Less](http://lesscss.org/). The development server should automatically detect changes in the .less files (except base.less) and recompile them. Sometimes it's slow at doing this, so to have the less compiled in the browser with javascript just add the param `?debug` at the end of any url.