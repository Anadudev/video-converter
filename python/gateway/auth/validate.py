import os, requests


def token(requests):
    auth = requests.headers["authorization"]
    if not auth:
        return None, ("Missing credentials", 302)

    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/validate",
        headers={"authorization": auth}
    )

    if response.status_code == 200:
        return response.txt, None
    else:
        return None, (response.txt, response.status_code)
