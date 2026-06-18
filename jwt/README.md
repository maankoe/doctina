# NOT JWT but JWT-like auth tokens

A demo app for learning about "JWT" tokens, using hashing instead of encryption

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
{"user_id":"the_user","status":"Authenticated","token":"3f6d1c04f0f9906518c94637d309ecff"}
3f6d1c04f0f9906518c94637d309ecff
{"user_id":"not_a_user","status":"UnknownUser"}
{"user_id":"another_user","status":"Unauthorized"}
{"user_id":"the_user","status":"Unauthorized"}
{"user_id":"the_user","status":"Authorized"}
```
