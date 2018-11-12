# Hummingbot

A simple machine vision bot that tweets when it sees hummingbirds on a
Google AIY-Vision camera.

Copyright 2018 Kevin Hester, kevinh@geeksville.com, GPL V3 License

## Build/install instructions

Note: the current build instructions are slightly yucky and assume you know
a bit about using the Linux shell/python.  If you encounter problems or have
questions, open a github issue or send me a note. I'm happy to update these
instructions as needed to make it clearer/easier.

1. On the AIY-Vision: cd /home/pi/AIY-projects-python/src/examples/vision
2. Clone this repository into that directory
3. run "sudo pip3 install pyyaml tweepy".  This installs libraries this little
bot needs.
4. Go to the [twitter developer console](https://apps.twitter.com/) and
register for your developer consumer_key and consumer_secret.  
Put those values into the indicated portion of config.yml.
5. run "python3 hummingbot.py".  If this is the first time you run the bot
it will ask you to visit an URL in your browser to get a PIN.  Visit that URL
and type the PIN into this app.  The app will then save the necessary keys
needed to tweet as that user.
6. Once you have everything working nicely you can run this app from
/etc/rc.local to have it start at powerup.
