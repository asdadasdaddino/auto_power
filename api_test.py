import requests

response_login = requests.get("http://point-900.com:8085/auto/api/user_auth?u=mi11&p=mi1155@@&v=1.4.1")
print(response_login.json())
user_key = response_login.json()['more_info']['key']
print(user_key)

response_bal = requests.get("http://point-900.com:8085/auto/api/user_bal?u=mi11&k=" + user_key)
print(response_bal.json())

response_bet = requests.get("http://point-900.com:8085/api/bet?userid=mi11&key=" + user_key +"&gm=PWB&tdate=20211021&rno=1126634&origin=auto&pp5=1000")
print(response_bet.json())