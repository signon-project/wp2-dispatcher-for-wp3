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

def use_NLU(data, conf):
    if (data['App']['sourceLanguage'] == 'NLD'):
        data['App']['sourceLanguage'] = 'DUT'
    if data['App']['sourceMode'] == 'TEXT' or data['App']['sourceMode'] == 'VIDEO':
        to_nlu_data = {'App': {'sourceText': data['App']['sourceText'],
                            'sourceLanguage': data['App']['sourceLanguage']
                            }}
    elif data['App']['sourceMode'] == 'AUDIO':
        to_nlu_data = {'App': {'sourceText': data['SourceLanguageProcessing']['ASRText'],
                            'sourceLanguage': data['App']['sourceLanguage']
                            }}

    if data['App']['sourceMode'] == 'TEXT' or data['App']['sourceMode'] == 'AUDIO':
        response = requests.post('http://servernlu:' + conf['componentsPort']['nlu'], json=to_nlu_data,
                        timeout=(conf['externalServices']['timeout']))

        r = response.json()

        data['SourceLanguageProcessing']['DEPREL'] = r['lin_tags']['DEPREL']
        data['SourceLanguageProcessing']['FEATS'] = r['lin_tags']['FEATS']
        data['SourceLanguageProcessing']['HEAD'] = r['lin_tags']['HEAD']
        data['SourceLanguageProcessing']['ID'] = r['lin_tags']['ID']
        data['SourceLanguageProcessing']['LEMMA'] = r['lin_tags']['LEMMA']
        data['SourceLanguageProcessing']['NERPOS'] = r['lin_tags']['NERPOS']
        data['SourceLanguageProcessing']['NERTYPE'] = r['lin_tags']['NERTYPE']
        data['SourceLanguageProcessing']['TOKEN'] = r['lin_tags']['TOKEN']
        data['SourceLanguageProcessing']['UPOSTAG'] = r['lin_tags']['UPOSTAG']
        data['SourceLanguageProcessing']['normalised'] = r['normalised']
        data['SourceLanguageProcessing']['wsd'] = r['wsd']