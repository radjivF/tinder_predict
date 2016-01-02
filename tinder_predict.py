# -*- coding: utf-8 -*-

"""Predict who liked your Tinder profile.

Usage:
  tinder_predict.py --facebook_id=<facebook_id> --facebook_token=<token> [--like_all]
  tinder_predict.py (-h | --help)
  tinder_predict.py --version

Options:
  --facebook_id=<facebook_id> Your Facebook profile ID: http://findmyfbid.com/
  --facebook_token=<facebook_token> Facebook auth token for the Tinder app, use the `access_token` in the redirect URL of this link: https://www.facebook.com/dialog/oauth?client_id=464891386855067&redirect_uri=https://www.facebook.com/connect/login_success.html&scope=basic_info,email,public_profile,user_about_me,user_activities,user_birthday,user_education_history,user_friends,user_interests,user_likes,user_location,user_photos,user_relationship_details&response_type=token
  --like_all    Automatically match with people in the predict list
  -h --help     Show this screen.
  --version     Show version.

"""
import requests
from collections import defaultdict
from docopt import docopt

TINDER_API_BASE_URL = "https://api.gotinder.com/"
TINDER_REQUEST_HEADERS = {
    "Content-type": "application/json",
    "User-agent": "Tinder/4.6.1 (iPhone; iOS 7.1; Scale/2.00)"}

class TinderProfile(dict):
    """Tinder profile data, indexed by Tinder ID"""

    def id_(self):
        """Tinder ID."""
        return self["_id"]

    def __hash__(self):
        return hash(self.id_())

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.id_() == other.id_()

def get_tinder_token(fb_id, fb_token):
    """Use Facebook ID and token to get a Tinder authentication token, and
    update default headers."""

    request_data = {
        "facebook_id": fb_id,
        "facebook_token": fb_token
    }
    response = requests.post(TINDER_API_BASE_URL + "/auth", data=request_data)
    assert response.ok, response.text
    token = response.json()["token"]
    TINDER_REQUEST_HEADERS["X-Auth-Token"] = token

    return response.json()

def predict_likes(like_all=False):
    """Predict likes on the current Tinder profile."""

    seen_profiles = defaultdict(int)

    # The number of iterations could be increased if you have lots of likes
    for _ in xrange(2):
        response = requests.get(TINDER_API_BASE_URL + "/user/recs",
                               headers=TINDER_REQUEST_HEADERS)
        assert response.ok, response.text
        assert "results" in response.json(), response.json()

        profiles = [TinderProfile(result)
                    for result in response.json()["results"]]

        for profile in profiles:
            seen_profiles[profile] += 1

    for profile, count in seen_profiles.iteritems():
        if count > 1:
            id_ = profile.id_()
            username = profile["name"]
            is_spambot = profile.get("connection_count") <= 0
            if is_spambot:
                report_spam_user(id_)
                like_or_pass_user(id_, like=False)
                print "%s, %s (SPAM, reported)" % (username, id_)
            else:
                if like_all:
                    like_or_pass_user(id_, like=True)
                    print "%s, %s (LIKED!)" % (username, id_)
                else:
                    print "%s, %s" % (username, id_)

def report_spam_user(id_):
    """Report and pass the given user ID."""

    CAUSE_SPAM = 1
    r = requests.get(TINDER_API_BASE_URL + "/report/" + id_,
                     json={"cause": CAUSE_SPAM},
                     headers=TINDER_REQUEST_HEADERS)
    assert r.ok, r.text

def like_or_pass_user(id_, like):
    like_or_pass = "like" if like else "pass"

    r = requests.get(TINDER_API_BASE_URL + "/" + like_or_pass + "/" + id_,
                     json={"last_activity_date": ""},
                     headers=TINDER_REQUEST_HEADERS)
    assert r.ok, r.text

if __name__ == "__main__":
    arguments = docopt(__doc__, version='Tinder Predict 1.0')

    facebook_id = arguments["--facebook_id"]
    facebook_token = arguments["--facebook_token"]
    get_tinder_token(facebook_id, facebook_token)

    predict_likes(like_all=arguments["--like_all"])
