# Camden Registration Api Client


## About

Wrapper on requests api to simulate user actions
on the Camden Activity Registration portal


## Running environment

Python > 3.9



## Usage


To install:

```
pip3 install camden_registration_api

```

And create your own runner file ```my_camden.py``` like below:

```
from camden_registration_api import CamdenClient

api_client = CamdenClient(
        login=<your login>,
        password=<your password>,
        activity_id=120589,
    )

# to run test registration
api_client.test()


# to run actual registration
api_client.register()
```

Then execute as normal python code:

```python3 my_camden.py```


## Other

To call Camden: 1-408-559-8553



## Special ask

Do not share with Alex K, let him train his fingers
