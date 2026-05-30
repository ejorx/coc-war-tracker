import os

# Si COC_API_KEY está definida, se usa directamente (ejecución local).
# Si no, se generará dinámicamente en ApiService usando email/password.
api_key = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImQ4ZTk2ZGE1LTEwNTAtNDliZS1hZmYyLTE5YTY2NTRlZDJjZSIsImlhdCI6MTc4MDA4NDE4Mywic3ViIjoiZGV2ZWxvcGVyLzI2YjEzNjA1LWUxZGItMmE0Yy03NTA4LTVlOTc1MzE5ZmZiYiIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjc5LjExNy4yMjIuNTciXSwidHlwZSI6ImNsaWVudCJ9XX0.cYYQgD9lj1uqoMSoM9ZUq8xw_tgjPQDjbIE0rFlX9Sdf6Npf1J10SJrV-dDe5ZSNmaM1T3sm0oT65olSYRGtIA" #os.environ.get("COC_API_KEY", "")

coc_email = os.environ.get("COC_EMAIL", "")
coc_password = os.environ.get("COC_PASSWORD", "")

url = "https://api.clashofclans.com/v1/"

clan_tag = "%23"+"2RJPYCGLV"