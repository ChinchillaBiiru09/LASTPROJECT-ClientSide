from flask import jsonify, make_response, session, request, current_app as app
from jwt import ExpiredSignatureError, InvalidTokenError
from .. import app

import jwt, requests, logging, json

logging.basicConfig(level=logging.DEBUG)


def decode_jwt(token):
    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return decoded_token, ""
    except ExpiredSignatureError:
        logging.debug("Token has expired")
        return None, "Sesi login anda telah habis. Silahkan login kembali."
    except InvalidTokenError:
        logging.debug("Invalid token")
        return None, "Token anda invalid. Silahkan coba lagi."
    except Exception as e:
        logging.debug(f"Unexpected error: {e}")
        return None, str(e)

# UTILITIES DASHBOARD ============================================================ Begin
def get_count_category(): # Clear
    try:
        # Membuat URL
        url = app.config['BE_URL'] + '/category/count'

        # Set headers url
        headers = {
            'Authorization' : f'Bearer {session["user"]["access_token"]}',
            'Content-Type' : 'application/json'
        }
        
        # request response ke BE api
        response = requests.request(
            method='GET',
            url=url,
            headers=headers
        )

        data = response.json().get('data')
        count = 0
        if data != None:
            count = data['category_count']

        return count
    except Exception as e:
        return str(e)

def get_count_template(): # Clear
    try:
        # Membuat URL
        url = app.config['BE_URL'] + '/template/count'

        # Set headers url
        headers = {
            'Authorization' : f'Bearer {session["user"]["access_token"]}',
            'Content-Type' : 'application/json'
        }
        
        # request response ke BE api
        response = requests.request(
            method='GET',
            url=url,
            headers=headers
        )

        data = response.json().get('data')
        count = 0
        if data != None:
            count = data['template_count']

        return count
    except Exception as e:
        return e

def get_count_user(): # Clear
    try:
        # Membuat URL
        url = app.config['BE_URL'] + '/user/count'

        # Set headers url
        headers = {
            'Authorization' : f'Bearer {session["user"]["access_token"]}',
            'Content-Type' : 'application/json'
        }
        
        # request response ke BE api
        response = requests.request(
            method='GET',
            url=url,
            headers=headers
        )

        data = response.json().get('data')
        count = 0
        if data != None:
            count = data['user_count']

        return count
    except Exception as e:
        return e

def get_count_invitation(): # Clear
    try:
        # Membuat URL
        url = app.config['BE_URL'] + '/invitation/count'

        # Set headers url
        headers = {
            'Authorization' : f'Bearer {session["user"]["access_token"]}',
            'Content-Type' : 'application/json'
        }
        
        # request response ke BE api
        response = requests.request(
            method='GET',
            url=url,
            headers=headers
        )

        data = response.json().get('data')
        count = 0
        if data != None:
            count = data['invitation_count']

        return count
    except Exception as e:
        return e

def get_template_popular(): # Clear
    try:
        # Membuat URL
        url = app.config['BE_URL'] + '/template/'

        # Set headers url
        headers = {
            'Authorization' : f'Bearer {session["user"]["access_token"]}',
            'Content-Type' : 'application/json'
        }
        
        # request response ke BE api
        response = requests.request(
            method='GET',
            url=url,
            headers=headers
        )

        data = response.json().get('data')

        return None
    except Exception as e:
        return str(e)

def get_category_popular():
    try:
        pass
    except Exception as e:
        return str(e)

def get_recent_invitation():
    try:
        pass
    except Exception as e:
        return str(e)

def get_count_guest(): # Clear
    try:
        # Membuat URL
        url = app.config['BE_URL'] + '/guest/count'

        # Set headers url
        headers = {
            'Authorization' : f'Bearer {session["user"]["access_token"]}',
            'Content-Type' : 'application/json'
        }
        
        # request response ke BE api
        response = requests.request(
            method='GET',
            url=url,
            headers=headers
        )

        data = response.json().get('data')
        count = 0
        if data != None:
            # print(data)
            count = data['guest_count']

        return count
    except Exception as e:
        return e

def get_count_greeting(): # Clear
    try:
        # Membuat URL
        url = app.config['BE_URL'] + '/greeting/count'

        # Set headers url
        headers = {
            'Authorization' : f'Bearer {session["user"]["access_token"]}',
            'Content-Type' : 'application/json'
        }
        
        # request response ke BE api
        response = requests.request(
            method='GET',
            url=url,
            headers=headers
        )

        data = response.json().get('data')
        count = 0
        if data != None:
            count = data['greeting_count']

        return count
    except Exception as e:
        return e

def get_request_template():
    try:
        # Membuat URL
        url = app.config['BE_URL'] + '/template/request/'

        # Set headers url
        headers = {
            'Authorization' : f'Bearer {session["user"]["access_token"]}',
            'Content-Type' : 'application/json'
        }
        
        # request response ke BE api
        response = requests.request(
            method='GET',
            url=url,
            headers=headers
        )

        data = response.json().get('data')
        # print("data -> ", data)

        return data
    except Exception as e:
        return e

# UTILITIES DASHBOARD ============================================================ End


# UTILITIES PROFILE ============================================================ Begin
def get_profile(is_param=False): # Clear
    try:
        # Params
        dataInput = None
        if is_param:
            id = request.args.get('id')
            dataInput = {
                "user_id": id
            }
        
        # Create URL
        url = app.config['BE_URL'] + '/profile/'

        # Set headers url
        headers = {
            'Authorization' : f'Bearer {session["user"]["access_token"]}',
            'Content-Type' : 'application/json'
        }
        
        # Send request to BE api
        response = requests.request (
            method='GET',
            url=url,
            headers=headers,
            params=dataInput
        )

        # Response data
        data = response.json().get('data')
        return data
    
    except Exception as e:
        return str(e)

def get_log(is_param=False): # Clear
    try:
        # Params
        dataInput = None
        if is_param:
            id = request.args.get('id')
            dataInput = {
                "user_id": id
            }
        
        # Create URL
        url = app.config['BE_URL'] + '/log/activity'

        # Set headers url
        headers = {
            'Authorization' : f'Bearer {session["user"]["access_token"]}',
            'Content-Type' : 'application/json'
        }
        
        # Send request to BE api
        response = requests.request (
            method='GET',
            url=url,
            headers=headers,
            params=dataInput
        )

        # Response data
        data = response.json().get('data')
        return data
    
    except Exception as e:
        return str(e)

# UTILITIES PROFILE ============================================================ End


# UTILITIES TEMPLATE PAGE ============================================================ Begin
def get_category(): # Clear
    try:
        # Membuat URL
        url = app.config['BE_URL'] + '/category/'

        # Set headers url
        headers = {
            'Authorization' : f'Bearer {session["user"]["access_token"]}',
            'Content-Type' : 'application/json'
        }
        
        # request response ke BE api
        response = requests.request(
            method='GET',
            url=url,
            headers=headers
        )

        data = response.json().get('data')

        return data
    except Exception as e:
        return str(e)

def get_detail_category(): # Clear
    try:
        # Set Params
        id = request.args.get('id')
        dataInput = {
            "category_id": id
        }

        # Create URL
        url = app.config['BE_URL'] + '/category/detail'

        # Set headers url
        headers = {
            'Authorization' : f'Bearer {session["user"]["access_token"]}',
            'Content-Type' : 'application/json'
        }
        
        # request response ke BE api
        response = requests.request(
            method='GET',
            url=url,
            headers=headers,
            params=dataInput
        )

        data = response.json().get('data')

        return data
    except Exception as e:
        return str(e)

def get_template(is_param=False): # Clear
    try:
        # Membuat URL
        url = app.config['BE_URL'] + '/template/'

        # Set headers url
        headers = {
            'Authorization' : f'Bearer {session["user"]["access_token"]}',
            'Content-Type' : 'application/json'
        }
        
        # request response ke BE api
        response = requests.request(
            method='GET',
            url=url,
            headers=headers
        )

        data = response.json().get('data')

        return data
    except Exception as e:
        return str(e)

def get_detail_template():
    try:
        # Params
        id = request.args.get('temId')
        dataInput = {
            "template_id": id
        }
        # print(dataInput)

        # Create URL
        url = app.config['BE_URL'] + '/template/detail'

        # Set headers url
        headers = {
            'Authorization' : f'Bearer {session["user"]["access_token"]}',
            'Content-Type' : 'application/json'
        }
        
        # request response ke BE api
        response = requests.request(
            method='GET',
            url=url,
            headers=headers,
            params=dataInput
        )

        data = response.json().get('data')
        # print(data)

        return data
    except Exception as e:
        return str(e)

def get_detail_request_template():
    try:
        # Params
        id = request.args.get('reqId')
        dataInput = {
            "request_id": id
        }
        # print(dataInput)
        
        # Membuat URL
        url = app.config['BE_URL'] + '/template/request/detail'

        # Set headers url
        headers = {
            'Authorization' : f'Bearer {session["user"]["access_token"]}',
            'Content-Type' : 'application/json'
        }
        
        # request response ke BE api
        response = requests.request(
            method='GET',
            url=url,
            headers=headers,
            params=dataInput
        )

        data = response.json().get('data')
        
        return data
    except Exception as e:
        return e

# UTILITIES TEMPLATE PAGE ============================================================ End


# UTILITIES GUEST PAGE ============================================================ Begin
def get_guest(is_param=False): # Clear
    try:
        # Params
        dataInput = None
        if is_param:
            id = request.args.get('id')
            dataInput = {
                "user_id": id
            }

        # Create URL
        url = app.config['BE_URL'] + '/guest/'

        # Set headers url
        headers = {
            'Authorization' : f'Bearer {session["user"]["access_token"]}',
            'Content-Type' : 'application/json'
        }
        
        # request response ke BE api
        response = requests.request(
            method='GET',
            url=url,
            headers=headers,
            params=dataInput
        )

        data = response.json().get('data')

        return data
    except Exception as e:
        return str(e)

def get_detail_guest():
    try:
        # Params
        code = request.args.get('code')
        dataInput = {
            "invitation_code": code
        }

        # Create URL
        url = app.config['BE_URL'] + '/guest/detail'

        # Set headers url
        headers = {
            'Authorization' : f'Bearer {session["user"]["access_token"]}',
            'Content-Type' : 'application/json'
        }
        
        # request response ke BE api
        response = requests.request(
            method='GET',
            url=url,
            headers=headers,
            params=dataInput
        )

        data = response.json().get('data')

        return data
    except Exception as e:
        return str(e)

def get_guest_by_id():
    try:
        # Params
        id = request.args.get('gueId')
        dataInput = {
            "guest_id": id
        }

        # Create URL
        url = app.config['BE_URL'] + '/guest/detail/id'

        # Set headers url
        headers = {
            'Authorization' : f'Bearer {session["user"]["access_token"]}',
            'Content-Type' : 'application/json'
        }
        
        # request response ke BE api
        response = requests.request(
            method='GET',
            url=url,
            headers=headers,
            params=dataInput
        )

        data = response.json().get('data')

        return data
    except Exception as e:
        return str(e)

# UTILITIES GUEST PAGE ============================================================ End


# UTILITIES DETAIL USER PAGE ============================================================ Begin
def get_invitation(is_param=False): # Clear
    try:
        # Params
        dataInput = None
        if is_param:
            id = request.args.get('id')
            dataInput = {
                "user_id": id
            }
        
        # Create URL
        url = app.config['BE_URL'] + '/invitation/'

        # Set headers url
        headers = {
            'Authorization' : f'Bearer {session["user"]["access_token"]}',
            'Content-Type' : 'application/json'
        }
        
        # Send request to BE api
        response = requests.request (
            method='GET',
            url=url,
            headers=headers,
            params=dataInput
        )

        # Response data
        data = response.json().get('data')
        return data
    
    except Exception as e:
        return str(e)

def get_detail_category(): # Clear
    try:
        # Params
        id = request.args.get('id')
        dataInput = {
            "category_id": id
        }

        # Create URL
        url = app.config['BE_URL'] + '/category/detail'

        # Set headers url
        headers = {
            'Authorization' : f'Bearer {session["user"]["access_token"]}',
            'Content-Type' : 'application/json'
        }
        
        # request response ke BE api
        response = requests.request(
            method='GET',
            url=url,
            headers=headers,
            params=dataInput
        )

        data = response.json().get('data')

        return data
    
    except Exception as e:
        return str(e)

def get_greeting(is_param=False): # Clear
    try:
        # Params
        dataInput = None
        if is_param:
            id = request.args.get('id')
            dataInput = {
                "user_id": id
            }

        # Create URL
        url = app.config['BE_URL'] + '/greeting/'

        # Set headers url
        headers = {
            'Authorization' : f'Bearer {session["user"]["access_token"]}',
            'Content-Type' : 'application/json'
        }
        
        # request response ke BE api
        response = requests.request(
            method='GET',
            url=url,
            headers=headers,
            params=dataInput
        )

        data = response.json().get('data')

        return data
    except Exception as e:
        return str(e)

# UTILITIES DETAIL USER PAGE ============================================================ End


# UTILITIES INVITATION PAGE ============================================================ Begin
def get_detail_invitation(): # Clear
    try:
        # Params
        id = request.args.get('id')
        dataInput = {
            "invitation_id": id
        }
        
        # Create URL
        url = app.config['BE_URL'] + '/invitation/detail'

        # Set headers url
        headers = {
            'Authorization' : f'Bearer {session["user"]["access_token"]}',
            'Content-Type' : 'application/json'
        }
        
        # Send request to BE api
        response = requests.request (
            method='GET',
            url=url,
            headers=headers,
            params=dataInput
        )

        # Response data
        data = response.json().get('data')
        return data
    
    except Exception as e:
        return str(e)

def get_detail_code_invitation(code): # Clear
    try:
        # Params
        # code = request.args.get('code')
        dataInput = {
            "invitation_code": code
        }
        print(code)
        print(dataInput)
        
        # Create URL
        url = app.config['BE_URL'] + '/invitation/detail/code'

        # Set headers url
        headers = {
            'Authorization' : f'Bearer {session["user"]["access_token"]}',
            'Content-Type' : 'application/json'
        }
        
        # Send request to BE api
        response = requests.request (
            method='GET',
            url=url,
            headers=headers,
            params=dataInput
        )

        # Response data
        data = response.json().get('data')
        return data
    
    except Exception as e:
        return str(e)

def get_detail_greeting():
    try:
        # Params
        code = request.args.get('code')
        dataInput = {
            "invitation_code": code
        }
        
        # Create URL
        url = app.config['BE_URL'] + '/greeting/detail'

        # Set headers url
        headers = {
            'Authorization' : f'Bearer {session["user"]["access_token"]}',
            'Content-Type' : 'application/json'
        }
        
        # Send request to BE api
        response = requests.request (
            method='GET',
            url=url,
            headers=headers,
            params=dataInput
        )

        # Response data
        data = response.json().get('data')
        return data
    
    except Exception as e:
        return make_response(jsonify(str(e)))
# UTILITIES INVITATION PAGE ============================================================ End


# UTILITIES SHARE INVITATION ============================================================ Begin
def set_message(code, title): # Clear
    try:
        # print(link)
        link = app.config['FE_URL']+"/"+code+"/"+title
        message = f"""Assalamualaikum Warahmatullahi Wabarakatuh

Tanpa mengurangi rasa hormat, perkenankan kami mengundang Bapak/Ibu/Saudara/i untuk menghadiri acara kami.

Berikut link undangan kami, untuk info lengkap dari acara bisa kunjungi :\n

{link}

\nMerupakan suatu kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan untuk hadir dan memberikan doa restu.

Dan agar selalu menjaga kesehatan bersama serta datang pada waktu yang telah ditentukan.*

Terima kasih banyak atas perhatiannya.

Wassalamualaikum Warahmatullahi Wabarakatuh
                """
        return message
    
    except Exception as e:
        return str(e)

# UTILITIES SHARE INVITATION ============================================================ End
