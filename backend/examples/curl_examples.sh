# Signup
curl -s -X POST http://localhost:8000/signup \
  -H 'Content-Type: application/json' \
  -d '{"email":"test@example.com","password":"secret123","name":"Test","dietary_preferences":{"vegetarian":false}}' | jq

# Login
TOKEN=$(curl -s -X POST http://localhost:8000/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"test@example.com","password":"secret123"}' | jq -r .access_token)

# Create journal entry
curl -s -X POST http://localhost:8000/journal \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"entry_text":"Am mancat pizza si salata. Ma simt stresat si anxios."}' | jq

# Stats summary
curl -s "http://localhost:8000/stats/summary" \
  -H "Authorization: Bearer $TOKEN" | jq
