# SignON WP3 Dispatcher
The SignON WP3 Dispatcher repository is part of [SignON](https://signon-project.eu/) an EU H2020 research and innovation funded project.  

The SignON Dispatchers (WP3/WP4/WP5) were implemented to allow the SignON Pipeline Components to analyse a message without implementing the communication channels between them nor with the Object Storage.  
The message from the SignON Orchestrator is passed to the first SignON Dispatcher (WP3) that:
1. retrieves the audio/video data from the Object Storage (if any)
2. communicates to the relevant SignON Pipeline Components
3. passes the message to the next SignON Dispatcher with a “piggyback” approach

The last SignON Dispatcher (WP5) returns the message to the SignON Orchestrator.

For further details please refer to public deliverable [D2.5 - Final release of the Open SignON Framework](https://signon-project.eu/publications/public-deliverables/).

## Getting Started

### Prerequisites
- Python: v3.8
- Message Broker: [RabbitMQ](https://www.rabbitmq.com/)
- Object Storage: [MinIO](https://min.io/)

For further details about the configuration of the components please refer to [SignON Framework Docker Compose](https://github.com/signon-project/wp2-framework-docker-compose).

### Installation 
1. Clone this repository
2. Create a virtual environment
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
4. Install the requirements
    ```bash
    pip install -r requirements.txt
    ```

### Usage
1. Set the parameters in `src/config.yml`
2. Start the SignON WP3 Dispatcher
    ```bash
    python dispatcher.py -c <config-file-path>
    ```
    > N.B. If ```<config-file-path>``` is not specified the project will use the config file in the same folder you are currently in.

    Alternatively, to launch the project Dockerised:
    ```bash
    docker build --tag=signon-wp3-dispatcher:X.X.X .
    docker run -d --rm --name signon-wp3-dispatcher -v path/to/config.yml:/config.yml signon-wp3-dispatcher:X.X.X
    ```

## Additional information

### Compatibility Matrix

| signon-wp3-dispatcher | signon-wp4-dispatcher | signon-wp5-dispatcher | signon-orchestrator |
|:---------------------:|:---------------------:|:---------------------:|:-------------------:|
|         4.0.0         |         5.0.0         |         4.0.0         |        17.0.0       |
|         3.0.7         |         4.0.5         |         3.0.3         |        12.0.0       |
|         3.0.6         |         4.0.4         |         3.0.3         |        12.0.0       |
|         3.0.5         |         4.0.3         |         3.0.3         |        12.0.0       |
|         3.0.1         |         4.0.0         |         3.0.0         |        12.0.0       |
|         3.0.0         |         4.0.0         |         3.0.0         |        12.0.0       |
|         2.4.0         |         3.2.0         |         2.1.0         |        8.0.0        |
|         2.3.2         |         3.1.2         |         2.0.2         |        7.0.0        |
|         2.3.2         |         3.1.2         |         2.0.2         |        6.1.0        |
|         2.2.2         |         3.0.2         |         2.0.2         |        6.0.0        |
|         2.2.1         |         3.0.1         |         2.0.1         |        6.0.0        |
|         2.2.0         |         3.0.0         |         2.0.0         |        6.0.0        |
|         2.1.0         |         2.1.0         |         2.0.0         |        6.0.0        |
|         2.0.0         |         2.0.0         |         2.0.0         |        6.0.0        |
|         1.0.0         |         1.0.0         |         1.0.0         |        5.0.0        |
|         0.1.0         |         0.1.0         |         0.1.0         |        5.0.0        |


### Documentation 
- [SignON Orchestrator AsyncAPI](https://github.com/signon-project/wp2-signon-orchestrator-asyncapi/blob/master/docs/markdown/asyncapi.md)

#### Other Details:
The IDE used for the project is:
- Visual Studio Code

## Authors
This project was developed by [FINCONS GROUP AG](https://www.finconsgroup.com/) within the Horizon 2020 European project SignON under grant agreement no. [101017255](https://doi.org/10.3030/101017255).  
For any further information, please send an email to [signon-dev@finconsgroup.com](mailto:signon-dev@finconsgroup.com).

## Licence
This project is released under the [Apache 2.0 license](https://www.apache.org/licenses/LICENSE-2.0.html).
