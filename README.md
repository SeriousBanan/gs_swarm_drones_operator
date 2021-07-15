# gs_swarm_drones_operator

A repository with the source code for launching an operator program for a swarm of Pioneer-Max drones.

## Requirements

-   Python 3.8 (Download: <https://www.python.org/downloads/>)

## Installation of operator

1. Clone gs_swarm_drones_operator repository.

    ```bash
    git clone https://github.com/SeriousBanan/gs_swarm_drones_operator.git
    ```

2. Install required python modules.

    ```bash
    python3 -m pip install -r <path to gs_swarm_drones_operator>/requirements.txt
    ```

## Preparing to launch

1. Go to folder with gs_swarm_drones_operator repository.

    ```bash
    cd <path to gs_swarm_drones>
    ```

2. Connect to network with drones.

3. Fill json configuration file.

    You need to remove `...` and fill fields in configuration.json file:

    - **drones count**: int value of amount of drones.
    - **drones initial positions**: dict where keys - drone's ids, values - ids of vertexes where drone start it program (from field.json file).

    ```json
    {
        "0": 0,
        "1": 6
    }
    ```

    - **addresses**: dict where keys - drone ids or operator, values - dict with ips and ports.

        For example:

        ```json
        "0": {
            "ip": "192.168.1.19",
            "port": 10000
        }
        ```

        This information used to communication between drones and operator.

    Example of full filled configuration file:

    ```json
    {
        "drones count": 2,
        "drones initial positions": {
            "0": 6,
            "1": 0
        },
        "addresses": {
            "operator": {
                "ip": "192.168.1.1",
                "port": 10000
            },
            "0": {
                "ip": "192.168.1.2",
                "port": 10000
            },
            "1": {
                "ip": "192.168.1.3",
                "port": 10000
            }
        },
        "image file path": "received_image.png"
    }
    ```

## Launching operator application

1. Go to folder with operator application file:

    ```bash
    cd <path to gs_swarm_drones_operator>
    ```

2. Launch python script:

    ```bash
    python3 application.py
    ```
