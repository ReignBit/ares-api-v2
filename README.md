# Ares Api v2
Database access api for services ran on ARES. Completely rebuilt from the ground up using Flask_restful and SQLAlchemy, with focus on full coverage unit-testing and modularity.

**Not compatible with v1 endpoints**

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
|id      | int(18) | Unique identifier for instance of User           |
|birthday| int     | Birth date for the user in the format YYYY-MM-DD |
|years   | int     | Not Used                                         |


### <a name="guild">Guild</a>
```json
    {
        "id": 123456789010111213,
        "settings": {
            "settings": {
                "prefix": "$"
            }
        },
    }
```
| Tag    | Type    | Description                                      |
|---     | ---     | ---                                              |
|id      | int(18) | Unique identifier for instance of Guild          |
|settings| dict    | Data used by Kat's modular extensions. General guild data |


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
|gid     | int(18) | Unique identifier for instance of the parent Guild |
|id      | int(18) | Unique identifier for instance of parent User      |
|level   | int     | Level of the user                                  |
|xp      | int     | Total experience of the user                       |
|settings| dict    | User specific data (Per extension)                 |



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
| ✔️  |  PATCH | /api/v2/users               | Edit a new user                        | [User](#user)
| ✔️   |  PATCH | /api/v2/guilds              | Edit a new guild                       | [Guild](#guild)
| ✔️   |  PATCH | /api/v2/guilds/[id]         | Edit a new member in guild             | [Member](#member) 
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
        "id": string,
        "pid": int,
        "status": boolean,
        
        "directory": string,
        "cmd": string,
        "args": string,
        
        "can_vote": boolean,
        "keep_alive": boolean
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

### <a name="service">PublicService</a>

```json
    {
        "id": string,
        "status": boolean,
        "keep_alive": boolean,
        "can_vote": boolean
    }
```
| Tag      | Type     | Description                                         |
|---       | ---      | ---                                                 |
|id        | string   | Unique identifier for the Service                   |
|status    | bool     | Whether the service is currently running            |
|can_vote  | boolean  | Used by kat. Should users be able to vote for start |
|keep_alive| boolean  | Should this service be kept alive at all times      |

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
