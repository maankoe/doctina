
curl -X POST "localhost:8000/authenticate" \
    -d '{"user_id": "not_a_user", "password": "password"}' \
    -H "accept: application/json" \
    -H "Content-Type: application/json" 

echo
curl -X POST "localhost:8000/authenticate" \
    -d '{"user_id": "the_user", "password": "wrong_password"}' \
    -H "accept: application/json" \
    -H "Content-Type: application/json" 

echo
curl -X POST "localhost:8000/authenticate" \
    -d '{"user_id": "the_user", "password": "their_password"}' \
    -H "accept: application/json" \
    -H "Content-Type: application/json" 

echo
response=$(curl -X POST "localhost:8000/authenticate" \
    -d '{"user_id": "the_user", "password": "their_password"}' \
    -H "accept: application/json" \
    -H "Content-Type: application/json")
token=$(echo $response | jq -r .token)
echo $token
echo '{"user_id": "not_a_user", "token": "'${token}'"}'

curl -X POST "localhost:8000/authorize" \
    -d '{"user_id": "not_a_user", "token": "'${token}'"}' \
    -H "accept: application/json" \
    -H "Content-Type: application/json"
echo


curl -X POST "localhost:8000/authorize" \
    -d '{"user_id": "another_user", "token": "'${token}'"}' \
    -H "accept: application/json" \
    -H "Content-Type: application/json"
echo

#echo '{"user_id": "the_user", "token": "'${token}'"}'
curl -X POST "localhost:8000/authorize" \
    -d '{"user_id": "the_user", "token": "'${token}'"}' \
    -H "accept: application/json" \
    -H "Content-Type: application/json"
echo
curl -X POST "localhost:8000/authorize" \
    -d '{"user_id": "the_user", "token": "'${token}'", "resources": ["a", "b"]}' \
    -H "accept: application/json" \
    -H "Content-Type: application/json"
echo
sleep 3
curl -X POST "localhost:8000/authorize" \
    -d '{"user_id": "the_user", "token": "'${token}'", "resources": ["a", "b"]}' \
    -H "accept: application/json" \
    -H "Content-Type: application/json"

