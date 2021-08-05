# Std Libaries
import configparser
import json
from collections import defaultdict

# Third-party Libraries
import tweepy
import tqdm


# Authentication using keys from .ini files
keys = configparser.ConfigParser()
keys.read("keys.ini")

auth = tweepy.OAuthHandler(**keys["consumer"])
auth.set_access_token(**keys["tokens"])

api = tweepy.API(auth)


# Store all list of followers and following
records = defaultdict(list)


# Attribute savers
def save_note(fn="test.txt"):
    """Save attributes from any object in .txt file"""

    def saver(func):                                    # func must return sequence obj
        result = "\n".join(func())
        with open(fn, "w") as note:
            note.write(result)
        return func

    return saver


# Friend Functions
# @save_note(fn="friend_attr.txt")
def getone_friends():
    for friend in tweepy.Cursor(api.friends).items(1):
        print(friend)


def record_relations(kind):                              # kind must be either 'friends' or 'followers'
    cursor = tweepy.Cursor(getattr(api, kind))
    for user in tqdm.tqdm(cursor.items()):

        records[kind].append({
            "id": user.id,
            "name": user.name,
            "screen_name": user.screen_name,
            "location": user.location,
            "following": user.following,
            "profile_image_url_https": user.profile_image_url_https,
        })


def start_recording(fn):

    record_relations("friends")
    record_relations("followers")

    json_str = json.dumps(records, sort_keys=False, indent=4)
    with open(fn, "w") as file:
        file.write(json_str)



if __name__ == "__main__":
    start_recording("friends.json")