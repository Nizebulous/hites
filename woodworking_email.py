import sys
import requests


SUBJECT = "Wood Working This Week"


def send_woodworking_email():
    """
    Find the next woodworking session and if it is this week, then send a
    notification email
    """
    params = {
        'to': sys.argv[1:],
        'subject': SUBJECT
    }
    response = requests.get("http://hites.org/woodworking/email_events", params=params)
    if response.status_code != requests.codes.ok:
        raise Exception('Bad Response from server')


if __name__ == "__main__":
    send_woodworking_email()
