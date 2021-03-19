
# Ares Api v2
![master](https://github.com/ReignBit/ares-api-v2/workflows/unit-tests/badge.svg?branch=master)

Database access api for services ran on ARES. Completely rebuilt from the ground up using Flask_restful and SQLAlchemy, with focus on full coverage unit-testing and modularity.

**Not compatible with v1 endpoints**

# How to use
## Configuration
- Download Python 3.x and pip
- Create a new file under `app` called `config.py`.
- Subclass any of the existing Config classes in `app.config_defaults`.
    - Make sure to change `SQLALCHEMY_DATABASE_URI` and `SQLALCHEMY_BINDS` to fit your environment.
    - Also change `AUTH_USERS` to something unique.
- Return back to the root directory and run the following commands:

### Windows
- `virtualenv .venv`
- `.\.venv\Scripts\activate.bat`
- `pip install -r requirements.txt`
- `python -m app`

### Linux
- `virtualenv .venv`
- `source ./venv/bin/activate`
- `pip install -r requirements.txt`
- `python -m app`



<br><br>
# Kat
[My Discord bot Kat](https://github.com/ReignBit/discord-kat) uses these endpoints to manage user information. They should not be used externally, but are still here for documentation purposes. Access to this information may be considered in the future.

### <a name="user">User</a>
```json
    {
        "id": 123456789010111213,
        "birthday": "2002-04-22",
        "years": 4
    }
```

| Tag    | Type    | Description                                      |
|---     | ---     | ---                                              |
|id*      | int(18) | Unique identifier for instance of User           |
|birthday| int     | Birth date for the user in the format YYYY-MM-DD |
|years   | int     | Not Used                                         |

<br><br>
### <a name="guild">Guild</a>
```json
    {
        "id": 123456789010111213,
        "settings": {
            "settings": {
                "prefix": "$"
            }
        }
    }
```

| Tag    | Type    | Description                                      |
|---     | ---     | ---                                              |
|id*      | int(18) | Unique identifier for instance of Guild          |
|settings| dict    | Data used by Kat's modular extensions. General guild data |

<br><br>
### <a name="member">Member</a>
Can only be referenced with a reference to a Guild object.
```json
    {
        "id": 123456789010111213,
        "gid": 234567890101112345,
        "level": 10,
        "xp": 524,
        "settings": {}
    }
```

| Tag    | Type    | Description                                        |
|---     | ---     | ---                                                |
|gid*     | int(18) | Unique identifier for instance of the parent Guild |
|id*      | int(18) | Unique identifier for instance of parent User      |
|level   | int     | Level of the user                                  |
|xp      | int     | Total experience of the user                       |
|settings| dict    | User specific data (Per extension)                 |

<br><br>
## Endpoints

|   Privileged   | Method | URL                    | Description                            | Return Type |
|:------:| ------ | --------                    | -----------                            |----
| ✔️  |  GET   | /api/v2/users               | Retrieve all user ids                  |  array[int]
| ✔️  |  GET   | /api/v2/guilds               | Retrieve all guild ids                |  array[int]
| ✔️   |  GET   | /api/v2/guilds/[gid]/members     | Retrieve all members of a guild   | array\[[Member](#member)\]
| ✔️  |  GET   | /api/v2/users/[id]          | Retrieve user information              |  [User](#user)
| ✔️   |  GET   | /api/v2/guilds/[id]         | Retrieve guild information             | [Guild](#guild)
| ✔️   |  GET   | /api/v2/guilds/[gid]/[uid]  | Retrieve member information from guild | [Member](#member)      
| ✔️  |  POST   | /api/v2/users              | Create a new user                      |  [User](#user)
| ✔️   |  POST   | /api/v2/guilds             | Create a new guild                     | [Guild](#guild)
| ✔️   |  POST   | /api/v2/guilds/members     | Create a new member in guild           | [Member](#member) 
| ✔️  |  PATCH | /api/v2/users               | Edit an existing user                        | [User](#user)
| ✔️   |  PATCH | /api/v2/guilds              | Edit an existing guild                       | [Guild](#guild)
| ✔️   |  PATCH | /api/v2/guilds/[id]         | Edit an existing member             | [Member](#member) 
| ✔️  |  DELETE| /api/v2/users/[id]          | Delete a user                          | None
| ✔️   |  DELETE| /api/v2/guilds/[id]         | Delete a guild                         | None
| ✔️   |  DELETE| /api/v2/guilds/[gid]/[uid]  | Delete a member from guild             | None

<br><br>
# Orwell/Supervisor [WIP]
Orwell (working title) is the service manager for ARES. Able to monitor, start, and stop services. These endpoints help orwell do it's thing.
Again, these are all privileged endpoints, but here for documentation. I doubt these will ever be open-ended due to their purpose.


### <a name="service">Service</a>
```json
    {
        "id": "game-server-2",
        "pid": "4958",
        "status": 1,
        
        "directory": "/opt/game/",
        "cmd": "gamex64",
        "args": "-server -rcon password123 -map ctf_fort",
        
        "can_vote": 0,
        "keep_alive": 0
    }
```
| Tag      | Type     | Description                                         |
|---       | ---      | ---                                                 |
|id        | string   | Unique identifier for the Service                   |
|pid       | int      | Process id of the running service (-1 if offline)   |
|status    | bool     | Whether the service is currently running            |
|directory | string   | Path to the executable/working directory            |
|cmd       | string   | Executable name                                     |
|args      | string   | Commandline arguments                               |
|can_vote  | boolean  | Used by kat. Should users be able to vote for start |
|keep_alive| boolean  | Should this service be kept alive at all times      |

<br><br>
### <a name="service">PublicService</a>

```json
    {
        "id": "game-server-2",
        "status": 1,
        "keep_alive": 0,
        "can_vote": 0
    }
```
| Tag      | Type     | Description                                         |
|---       | ---      | ---                                                 |
|id        | string   | Unique identifier for the Service                   |
|status    | bool     | Whether the service is currently running            |
|can_vote  | boolean  | Used by kat. Should users be able to vote for start |
|keep_alive| boolean  | Should this service be kept alive at all times      |

<br><br>
## Endpoints
| Privileged | Method  | URL                           | Description                                  | Return Type     |
| :---:      |---      | ---                           | ---                                          | ---             |
|❌         | GET      |/api/v2/public/services       | Retrieve a public-friendly list of services  | array\[[PublicService](#public-service)\]|
|✔️         | GET      |/api/v2/services              | Retrieve a list of services                  | array\[[Service](#service)\]  |
|✔️         | POST     |/api/v2/services              | Create a service                             | [Service](#service)        |
|✔️         | PATCH    |/api/v2/services/[id]         | Retrieve a service                           | [Service](#service)         |
|✔️         | DELETE   |/api/v2/services/[id]         | Delete a service                             | None            |
|✔️         | POST   |/api/v2/services/[id]/start     | Start a service process                      | [Service](#service)         |
|✔️         | POST   |/api/v2/services/[id]/stop      |  Stop a service process                      | [Service](#service)         |
