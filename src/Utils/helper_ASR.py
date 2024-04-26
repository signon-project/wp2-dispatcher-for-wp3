# Copyright 2021-2023 FINCONS GROUP AG within the Horizon 2020
# European project SignON under grant agreement no. 101017255.

# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 

#     http://www.apache.org/licenses/LICENSE-2.0 

# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.

import requests
import json
import os

def retrieveCodeLanguagev2(sourceLanguage):
    switcher = {
        "DUT": 3,
        "NLD": 3,
        "ENG": 1,
        "SPA": 2,
        "GLE": 4
    }
    return switcher.get(sourceLanguage)

def retrieveCodeLanguagev1(sourceLanguage):
    switcher = {
        "DUT": 1,
        "ENG": 5,
        "NLD": 6,
        "SPA": 9
    }

    return switcher.get(sourceLanguage)

def use_ASR(file_name, data, conf):

    if conf['asr']['version'] == 'v2':
        languageCode = retrieveCodeLanguagev2(data['App']['sourceLanguage'])
        if languageCode in [1,2,3]:
            username_signon_wav2vec2 = "signon@project.eu"
            password_signon_wav2vec2 = "SignonProject2023"

            url_signon_wav2vec2 = 'https://signon-wav2vec2.cls.ru.nl/login'
            payload_signon_wav2vec2 = {
                'grant_type': '',
                'username': username_signon_wav2vec2,
                'password': password_signon_wav2vec2,
                'scope': '',
                'client_id': '',
                'client_secret': ''
            }
            headers_signon_wav2vec2 = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'accept': 'application/json'
            }
            response_signon_wav2vec2 = requests.post(url_signon_wav2vec2, data=payload_signon_wav2vec2, headers=headers_signon_wav2vec2)
            access_token_signon_wav2vec2 = response_signon_wav2vec2.json()['access_token']

            text = transcribe(file_name, languageCode, access_token_signon_wav2vec2)
        else:
            username_restasr = "SignOnASR"
            password_restasr = "SignOnASR2022"

            url_restasr_login = 'https://restasr.cls.ru.nl/auth/login'
            payload_restasr_login = {
                "username": username_restasr,
                "password": password_restasr
            }
            headers_restasr_login = {
                'Content-Type': 'application/json'
            }
            response_restasr = requests.post(url_restasr_login, json=payload_restasr_login, headers=headers_restasr_login, timeout=(conf['externalServices']['timeout']))
            access_token_restasr = response_restasr.json()['data']['access_token']

            text = transcribe(file_name, languageCode, access_token_restasr)

        if text is not None:
            data['SourceLanguageProcessing']['ASRText'] = text
        else:
            data['SourceLanguageProcessing']['ASRText'] = " "


    elif conf['asr']['version'] == 'v1':
        r = requests.post('https://restasr.cls.ru.nl/auth/login', json={
            "username": "SignOnASR",
            "password": "SignOnASR2022"
        }, headers={'Content-Type': 'application/json'},
                        timeout=(conf['externalServices']['timeout']))

        token = r.json()['data']['access_token']
        url = 'https://restasr.cls.ru.nl/users/SignOnASR/audio'
        audio_filename = os.path.basename(file_name)
        multipart_form_data = {
            'file': (audio_filename, open(file_name, 'rb'), 'audio/wav')
        }
        headers = {
            'Authorization': 'Bearer ' + token,
        }
        r2 = requests.post(url, headers=headers, files=multipart_form_data,
                        timeout=(conf['externalServices']['timeout']))
        id_audio = r2.json()['data']['filename']
        languageCode = retrieveCodeLanguagev1(data['App']['sourceLanguage'])
        params = {"code": languageCode,
                "text": "custom text",
                "keep": True
                }
        r3 = requests.post('https://restasr.cls.ru.nl/users/SignOnASR/audio/' + id_audio,
                        json=params, headers={'Authorization': "Bearer " + token},
                        timeout=(conf['externalServices']['timeout']))
        text = r3.json()['data']['nbest']
        ctm = r3.json()['data']['ctm']
        if text is not None:
            data['SourceLanguageProcessing']['ASRText'] = text.lower()
        else:
            data['SourceLanguageProcessing']['ASRText'] = " "
        data['SourceLanguageProcessing']['ASRCTM'] = ctm



def transcribe(filename, lang_code, token):
    if lang_code in [2,3]:
        url = f'https://signon-wav2vec2.cls.ru.nl/user/1/{lang_code}'
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        files = {
            'file': (filename, open(filename, 'rb'), 'audio/wav')
        }
        response = requests.post(url, headers=headers, files=files)
        output = response.json()
        transcript = output[0].split(': ')[-1]
        return transcript

    elif lang_code == 1:
        url = f'https://signon-wav2vec2.cls.ru.nl/user/2/4/{lang_code}'
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        files = {
            'file': (filename, open(filename, 'rb'), 'audio/wav')
        }
        response = requests.post(url, headers=headers, files=files)
        output = response.json()
        transcript = output[0].split(': ')[-1]
        return transcript

    elif lang_code == 4:
        url = 'https://restasr.cls.ru.nl/users/SignOnASR/audio'
        audio_filename = os.path.basename(filename)
        multipart_form_data = {
            'file':(audio_filename, open(filename, 'rb'), 'audio/wav')
        }
        headers = {
            'Authorization': 'Bearer ' + token,
        }
        r2 = requests.post(url, headers=headers, files=multipart_form_data)
        id_audio = r2.json()['data']['filename']
        params = {
            "code": 11,
            "text": "custom text",
            "keep": True
        }
        r3 = requests.post('https://restasr.cls.ru.nl/users/SignOnASR/audio/'+id_audio,
                           json=params, headers={'Authorization': "Bearer "+token})
        transcript = r3.json()['data']['nbest']
        return transcript


