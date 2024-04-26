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

import getopt
import json
import os
import sys
from os import makedirs
from os import path
from time import time, sleep

import boto3
import botocore
import pika
import requests
import yaml

from Utils.helper_ASR import use_ASR
from Utils.helper_SLR import use_SLR
from Utils.helper_NLU import use_NLU
from Utils.helper_minio import download_minio_file
from ExceptionHandler.exceptionHandler import handleException

def now():
    return round(time() * 1000)

def check_same_text_language(data):
    text_languages = ['ENG', 'GLE', 'SPA', 'DUT']
    for lang in text_languages:
        if data['App']['sourceLanguage'] == lang and data['App']['translationLanguage'] == lang:
            return True
    return False

argv = sys.argv[1:]
configFile = 'config.yml'
opts, args = getopt.getopt(argv, "hc:", ["config="])
for opt, arg in opts:
    if opt == '-h':
        print('dispatcher.py -c <config-file-path>')
        sys.exit()
    elif opt in ("-c", "--config"):
        configFile = arg
print('Config file:', configFile)

with open(configFile, 'rb') as f:
    conf = yaml.safe_load(f.read())
print('RabbitMQ host:', conf['rabbitmq']['host'])
print('RabbitMQ RPC queue:', conf['rabbitmq']['rpc-queue'])
print('RabbitMQ WP4 queue:', conf['rabbitmq']['wp4-queue'])

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=conf['rabbitmq']['host']))
channel = connection.channel()

def on_request(ch, method, props, body):
    my_json = body.decode('utf8')
    data = json.loads(my_json)
    data['SourceLanguageProcessing'] = {}
    data['RabbitMQ'] = {}
    if not conf['debug']['multi-processing']:
        if data['App']['sourceMode'] == "AUDIO" or data['App']['sourceMode'] == "VIDEO":
            try:
                file_name = download_minio_file(data, conf)

            except (botocore.exceptions.ConnectTimeoutError, botocore.exceptions.EndpointConnectionError) as e:
                e_type = "Minio-Timeout"
                e_title = "Minio Component Timeout Connection"
                e_status = 500
                e_detail = "The Connection with the Minio Component caused a Timeout"
                handleException(e, ch, props.reply_to, props.correlation_id, e_type, e_title, e_status, e_detail)
            except Exception as e:
                e_type = "Minio-Error"
                e_title = "There has been an Error with Minio"
                e_status = 500
                e_detail = "Something with Minio has not worked correctly"
                handleException(e, ch, props.reply_to, props.correlation_id, e_type, e_title, e_status, e_detail)
                return

            if data['App']['sourceMode'] == 'VIDEO':
                try:
                    use_SLR(file_name, data, conf)
                except (requests.exceptions.ReadTimeout, requests.exceptions.Timeout, requests.exceptions.ConnectTimeout) as e:
                    e_type = "SLR-Timeout"
                    e_title = "SLR Component Timeout Connection"
                    e_status = 500
                    e_detail = "The Connection with the SLR Component caused a Timeout"
                    handleException(e, ch, props.reply_to, props.correlation_id, e_type, e_title, e_status, e_detail)
                except Exception as e:
                    e_type = "SLR-Error"
                    e_title = "Error related to the SLR Component"
                    e_status = 500
                    e_detail = "Something went wrong with the behaviour of the SLR Component"
                    handleException(e, ch, props.reply_to, props.correlation_id, e_type, e_title, e_status, e_detail)
                    return
            else:
                try:
                    use_ASR(file_name, data, conf)

                except (requests.exceptions.ReadTimeout, requests.exceptions.Timeout, requests.exceptions.ConnectTimeout) as e:
                    e_type = "ASR-Timeout"
                    e_title = "ASR Component Timeout Connection"
                    e_status = 500
                    e_detail = "The Connection with the ASR Component caused a Timeout"
                    handleException(e, ch, props.reply_to, props.correlation_id, e_type, e_title, e_status, e_detail)
                except Exception as e:
                    e_type = "ASR-Error"
                    e_title = "Error related to the ASR Component"
                    e_status = 500
                    e_detail = "Something went wrong with the behaviour of the ASR Component"
                    handleException(e, ch, props.reply_to, props.correlation_id, e_type, e_title, e_status, e_detail)
                    return
        try:
            if not check_same_text_language(data): use_NLU(data, conf)

        except (requests.exceptions.ReadTimeout, requests.exceptions.Timeout, requests.exceptions.ConnectTimeout) as e:
            e_type = "NLU-Timeout"
            e_title = "NLU Component Timeout Connection"
            e_status = 500
            e_detail = "The Connection with the NLU Component caused a Timeout"
            handleException(e, ch, props.reply_to, props.correlation_id, e_type, e_title, e_status, e_detail)
        except Exception as e:
            e_type = "NLU-Error"
            e_title = "There has been an Error with the NLU Component"
            e_status = 500
            e_detail = "Something with the NLU has not worked correctly"
            handleException(e, ch, props.reply_to, props.correlation_id, e_type, e_title, e_status, e_detail)
            return

    else:
        print("Dispatcher Instance " + str(os.getpid()) + " [x] Received request for " + data['App']['sourceText'])
        workSec = len(data['App']['sourceText'])
        sleep(workSec)
        print("Dispatcher Instance " + str(os.getpid()) + " [.] Returned " + str(workSec))
        translationText = " Waiting Time: " + str(workSec)
        print(translationText)

    data['SourceLanguageProcessing']['T2WP3'] = now()
    data['RabbitMQ']['correlationID'] = props.correlation_id
    data['RabbitMQ']['replyTo'] = props.reply_to


    response_string = json.dumps(data)
    ch.basic_publish(exchange='',
                     routing_key=conf['rabbitmq']['wp4-queue'],
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=response_string)
    print(" [x] Message Sent to WP4")


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=conf['rabbitmq']['rpc-queue'], on_message_callback=on_request, auto_ack=True)
print(" [x] Awaiting RPC requests")
channel.start_consuming()
