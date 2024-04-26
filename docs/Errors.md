## Errors Documentation

The SignON WP3 Dispatcher returns errors in JSON format, according to the RFC 7807 specification ([link](https://tools.ietf.org/html/rfc7807)).  
Below is a short recap of the fields:
* **type**: URI that identifies the problem type (e.g. "urn:error-type:name-of-the-error")
* **title**: Human readable short description of the error
* **status**: Repetition of the response status code (e.g. 400)
* **detail**: Human readable full description of the error
* **instance**: URI reference that identifies the specific occurrence of the problem (e.g. "urn:uuid:d294b32b-9dda-4292-b51f-35f65b4bf64d")

The RFC 7807 specification allows extensions (i.e. custom, machine readable fields).  
Below are the one used:
* **stackTrace**: Stack trace of the error (can be enabled/disabled with `include-stack-trace` flag in `application.yml` )
* **timestamp**: Timestamp of the error (with format "dd-MM-yyyy hh:mm:ss")
* **parameters**: Relevant parameters (see table below for more info)

### Error Codes
According to the RFC 7807 specification, the "type" field shall be unique and shall not change.  
Due to this, the "type" field can be used as an error code to uniquely identify the error.  
The following table lists the error codes reported by the IPR Service, with the related parameters and HTTP Status Code.

|   Error Code                                              |     Parameters Names (JSON type)         |   HTTP Status Code   |                Source                |
|:---------------------------------------------------------:|:----------------------------------------:|:--------------------:|:------------------------------------:|
|    urn:error-type:Minio-Timeout                           |                  /                       |          500         |           SignON WP3 Dispatcher      |
|    urn:error-type:Minio-Error                             |                  /                       |          500         |           SignON WP3 Dispatcher      |
|    urn:error-type:ASR-Timeout                             |                  /                       |          500         |           SignON WP3 Dispatcher      |
|    urn:error-type:ASR-Error                               |                  /                       |          500         |           SignON WP3 Dispatcher      |
|    urn:error-type:NLU-Timeout                             |                  /                       |          500         |           SignON WP3 Dispatcher      |
|    urn:error-type:NLU-Error                               |                  /                       |          500         |           SignON WP3 Dispatcher      |

### Error Response Example

Below is reported an example error response.

```json
{
    "type":"urn:error-type:minio-error",
    "title":"There has been an Error with minio",
    "status":500,
    "detail":"Something with minio has not worked correctly",
    "instance":"urn:uuid:40b5638e-347f-49cd-a228-4a95de41790b",
    "stackTrace":"Traceback (most recent call last):\n  File \"dispatcher.py\", line 148, in on_request\n    s3.Bucket(data['OrchestratorRequest']['bucketName']).download_file(data['App']['sourceKey'], file_name)\n  File \"/usr/local/lib/python3.8/site-packages/boto3/s3/inject.py\", line 277, in bucket_download_file\n    return self.meta.client.download_file(\n  File \"/usr/local/lib/python3.8/site-packages/boto3/s3/inject.py\", line 190, in download_file\n    return transfer.download_file(\n  File \"/usr/local/lib/python3.8/site-packages/boto3/s3/transfer.py\", line 320, in download_file\n    future.result()\n  File \"/usr/local/lib/python3.8/site-packages/s3transfer/futures.py\", line 103, in result\n    return self._coordinator.result()\n  File \"/usr/local/lib/python3.8/site-packages/s3transfer/futures.py\", line 266, in result\n    raise self._exception\n  File \"/usr/local/lib/python3.8/site-packages/s3transfer/tasks.py\", line 269, in _main\n    self._submit(transfer_future=transfer_future, **kwargs)\n  File \"/usr/local/lib/python3.8/site-packages/s3transfer/download.py\", line 354, in _submit\n    response = client.head_object(\n  File \"/usr/local/lib/python3.8/site-packages/botocore/client.py\", line 415, in _api_call\n    return self._make_api_call(operation_name, kwargs)\n  File \"/usr/local/lib/python3.8/site-packages/botocore/client.py\", line 745, in _make_api_call\n    raise error_class(parsed_response, operation_name)\nbotocore.exceptions.ClientError: An error occurred (404) when calling the HeadObject operation: Not Found\n","timestamp":"2022-10-05T18:03:50.477+00:00",
    "parameters":"null"
}
```

