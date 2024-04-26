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

def mapLanguage_SLR(input):
    switcher = {
        "VGT": "VGT",
        "SSP": "LSE",
        "BFI": "BSL",
        "ISG": "ISL",
        "DSE": "NGT",
        "BSL": "BSL"
    }

    return switcher.get(input)

def use_SLR(file_name, data, conf):
    video_filename_local = os.path.basename(file_name)
    with open(file_name, 'rb') as file:
        print("sourceLanguage = "+str(data['App']['sourceLanguage'])+"\t mapped to: "+ str(mapLanguage_SLR(data['App']['sourceLanguage'])))
        slr_metadata = {'sourceLanguage': mapLanguage_SLR(data['App']['sourceLanguage'])}
        files = {
            'video': (video_filename_local, file, f'video/{data["App"]["sourceFileFormat"]}'),
            'metadata': ('metadata.json', json.dumps(slr_metadata), 'application/json')
        }
        result = requests.post("http://server_slr:" + conf['componentsPort']['slr'] + "/extract_features", files=files,
                            timeout=(conf['externalServices']['timeout']))
        json_out = result.json()

        data['SourceLanguageProcessing']['SLR'] = {'embedding': json_out['embedding']}