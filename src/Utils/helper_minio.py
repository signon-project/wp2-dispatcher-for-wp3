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

import boto3
import botocore

from os import makedirs
from os import path

def download_minio_file(data, conf):
    minioUsername = conf['minio']['username']
    minioPassword = conf['minio']['password']
    s3 = boto3.resource('s3',
                        endpoint_url=conf['minio']['endpoint'],
                        aws_access_key_id=minioUsername,
                        aws_secret_access_key=minioPassword
                        )
    downloadDirectoryPath = conf['minio']['downloadDirectoryPath'] + '/' + data['App']['appInstanceID']
    if not path.exists(downloadDirectoryPath):
        makedirs(downloadDirectoryPath)
    file_name = conf['minio']['downloadDirectoryPath'] + "/" + data['App']['sourceKey']
    s3.Bucket(data['OrchestratorRequest']['bucketName']).download_file(data['App']['sourceKey'], file_name)
    print("\n|#| - Succesfully downloaded '" + str(data['App']['sourceKey']) + "' from minio in '" + file_name + "' - |#|\n")
    return file_name