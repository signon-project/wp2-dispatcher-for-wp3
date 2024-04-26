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

import sys
import json
import pika
from time import time

import uuid
import traceback

def handleException(e, ch, replyTo, correlationID, e_type, e_title, e_status, e_detail, parameters="null"):
    print("Hi, there was an Error here")
    print("-" * 80)

    print(str(traceback.format_exc()))
    print("-" * 80)
    print(e.__class__)
    print("-" * 80)

    data = {}
    data['type'] = "urn:error-type:" + e_type
    data['title'] = e_title
    data['status'] = e_status
    data['detail'] = e_detail
    data['instance'] = "urn:uuid:" + str(uuid.uuid4())
    data['stackTrace'] = str(traceback.format_exc())
    data['timestamp'] = str(round(time() * 1000))
    data['parameters'] = parameters

    response_string = json.dumps(data)

    ch.basic_publish(exchange='',
                     routing_key=replyTo,
                     properties=pika.BasicProperties(correlation_id = correlationID),
                     body=response_string)

    print(" [xxx] Error Message Sent to Orchestrator")
    print("-" * 80)