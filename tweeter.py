# This is the client side glue for doing our tweets


# importing the module
import tweepy
import yaml

# Load auth keys etc...
configfile = "config.yml"
config = yaml.safe_load(open(configfile))

# authentication of consumer key and secret
auth = tweepy.OAuthHandler(config["twitter"]["consumer_key"], config["twitter"]["consumer_secret"])

# See if we already have keys for this user, if not ask user to authorize us

if "user" in config:
    auth.access_token = config["user"]["access_token"]
    auth.access_token_secret = config["user"]["access_token_secret"]
else:
    try:
        redirect_url = auth.get_authorization_url()
        print("auth url", redirect_url)
    except tweepy.TweepError:
        print('Error! Failed to get request token.')

    verifier = raw_input('PIN:').strip()
    auth.get_access_token(verifier)

    # FIXME - save config to disk
    print('saving new access token')
    config["user"] = {}
    config["user"]["access_token"] = str(auth.access_token)
    config["user"]["access_token_secret"] = str(auth.access_token_secret)
    stream = file(configfile, 'w')
    yaml.safe_dump(config, stream)

# authenticate and retrieve user name
auth.set_access_token(auth.access_token, auth.access_token_secret)

# authentication of access token and secret
api = tweepy.API(auth)

user = api.me()
print("my Twitter username " + user.name)

def tweet(filename, text):
    # update the status
    api.update_with_media(filename, text)

# run test code if invoked standalone
if __name__ == "__main__":
    tweet('testimage.jpg', 'testing testing testing')
