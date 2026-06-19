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
{"user_id":"user_id","status":"UnknownUser","token":null}
{"user_id":"the_user","status":"Unauthenticated","token":null}
{"user_id":"the_user","status":"Authenticated","token":"67aa9d9d1d0d97800ea83d0cdc5f53e8#the_user#2026-06-19T23:02:00.741627#1"}
99ab0d60601560e87f39a26ab72a3a19#the_user#2026-06-19T23:02:00.753563#1
{"user_id": "not_a_user", "token": "99ab0d60601560e87f39a26ab72a3a19#the_user#2026-06-19T23:02:00.753563#1"}
{"user_id":"not_a_user","status":"UnknownUser"}
{"user_id":"another_user","status":"Unauthorized: insufficient access"}
{"user_id":"the_user","status":"Unauthorized: insufficient access"}
{"user_id":"the_user","status":"Authorized"}
{"user_id":"the_user","status":"Unauthorized: token expired"}
```
