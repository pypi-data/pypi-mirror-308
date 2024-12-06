import os

from dotenv import load_dotenv
from mtmaisdk import ClientConfig, Hatchet

load_dotenv()


# 不验证 tls 因后端目前 证数 是自签名的。
os.environ["HATCHET_CLIENT_TLS_STRATEGY"] = "none"
os.environ["HATCHET_CLIENT_TOKEN"] = (
    "eyJhbGciOiJFUzI1NiIsImtpZCI6Impfd1YwZyJ9.eyJhdWQiOiJodHRwOi8vbG9jYWxob3N0Ojg4ODgiLCJleHAiOjQ4ODQ5MDc0ODIsImdycGNfYnJvYWRjYXN0X2FkZHJlc3MiOiJsb2NhbGhvc3Q6NzA3NyIsImlhdCI6MTczMTMwNzQ4MiwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo4ODg4Iiwic2VydmVyX3VybCI6Imh0dHA6Ly9sb2NhbGhvc3Q6ODg4OCIsInN1YiI6IjMxMjcxMWY0LWRlZmQtNGEwMy05NWE2LTg4MjY1NmNlODA4MiIsInRva2VuX2lkIjoiZGZlNTM3ZTEtODg4NC00ZjVmLWIxZGUtNGEyMzRiZDc1NDc2In0.gcnSyv_qEeyasUctFA6etssH23YmePEtQUukmxvZuQRRQPLq9FqXAMl7Nk7QnWNIUxYMT6SZiHzRGXI1gkfU-Q"
)


server_url = "http://localhost:8383"
wfapp = Hatchet(
    debug=True,
    config=ClientConfig(
        server_url=server_url,
    ),
)
