# NOT JWT but JWT-like auth tokens

A demo app for learning about "JWT" (-like) tokens - it's not JSON

Run using:

```
uv sync
. .venv/bin/activate
python server.py
```

Then, in another terminal:

```
sh client.sh
```

This should output something like:
```
{"status":"UnknownUser","token":null}
{"status":"Unauthenticated","token":null}
{"status":"Authenticated","token":"0d8a76b89e5557c3291097cd08f873d1#the_user#2026-06-19T23:12:57.527180#1"}
12546b1a7a25c74ef4d52634951ba3ee#the_user#2026-06-19T23:12:57.538879#1
{"status":"UnknownUser"}
{"status":"Unauthorized: invalid token"}
{"status":"Unauthorized: insufficient access"}
{"status":"Authorized"}
{"status":"Unauthorized: token expired"}
```
