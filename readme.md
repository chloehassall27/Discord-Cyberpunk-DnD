# Cyberpunk DnD Discorb Bot

## Production server

- To SSH into the server, `ssh -i ".\bot-vm_key.pem" cyberpunk@20.246.94.220`
- The server files are available in `/home/cyberpunk/server`
- If needed, install the requirements with `pip install -r requirements.txt`
- Launch the server with `python3 app.py`

## Development

### Pre-reqs
[Install and use the Azure Cosmos DB Emulator for local development and testing](https://learn.microsoft.com/en-us/azure/cosmos-db/local-emulator?tabs=ssl-netstd21)

### Environment Setup

API string for MongoDB env variable, [instructions here](https://learn.microsoft.com/en-us/azure/cosmos-db/local-emulator?tabs=ssl-netstd21#api-for-mongodb)
- To launch the storage emulator, in an admin terminal in the emulator directory, run `.\Microsoft.Azure.Cosmos.Emulator.exe /EnableMongoDbEndpoint=3.6 /MongoPort=10255`

### Other Notes

Use `pipreqs --force` to update requirements.txt