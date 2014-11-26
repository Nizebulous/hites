import requests


FROM = 'nizebulous@gmail.com'
TO = ['nizebulous@gmail.com']
SUBJECT = "Wood Working This Week"


def send_woodworking_email():
    """
    Find the next woodworking session and if it is this week, then send a
    notification email
    """
    params = {
        'from': FROM,
        'to': TO,
        'subject': SUBJECT
    }
    response = requests.get("http://192.168.59.103:5000/woodworking/email_events", params=params)
    if response.status_code != requests.codes.ok:
        raise Exception('Bad Response from server')


if __name__ == "__main__":
    send_woodworking_email()
