# Tinder predict

Predict who liked your Tinder profile.
Thanks to @rtt for his unofficial Tinder API documentation: https://gist.github.com/rtt/10403467

## Setup

```
pip install -r requirements.txt
```

## Usage

```
tinder_predict.py --facebook_id=<facebook_id> --facebook_token=<token> [--like_all]

Options:
  --facebook_id=<facebook_id> Your Facebook profile ID: http://findmyfbid.com/
  --facebook_token=<facebook_token> Facebook auth token for the Tinder app, use the access_token in the redirect URL of this link: https://www.facebook.com/dialog/oauth?client_id=464891386855067&redirect_uri=https://www.facebook.com/connect/login_success.html&scope=basic_info,email,public_profile,user_about_me,user_activities,user_birthday,user_education_history,user_friends,user_interests,user_likes,user_location,user_photos,user_relationship_details&response_type=token
  --like_all    Automatically match with people in the predict list
```
