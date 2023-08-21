# Cyberpunk DnD Discorb Bot

## Production server

- To SSH into the server, `ssh -i ".\bot-vm_key.pem" cyberpunk@20.246.94.220`
- The server files are available in `/home/cyberpunk/server`
- The server utilizes systemd and should be started on startup after networking has started
- To restart the server, use `sudo systemctl restart dnd-bot.service`
- To view the server console, use `journalctl -f -u dnd-bot.service`

## Development

### Pre-reqs
[Install and use the Azure Cosmos DB Emulator for local development and testing](https://learn.microsoft.com/en-us/azure/cosmos-db/local-emulator?tabs=ssl-netstd21)

### Environment Setup

API string for MongoDB env variable, [instructions here](https://learn.microsoft.com/en-us/azure/cosmos-db/local-emulator?tabs=ssl-netstd21#api-for-mongodb)
- To launch the storage emulator, in an admin terminal in the emulator directory, run `.\Microsoft.Azure.Cosmos.Emulator.exe /EnableMongoDbEndpoint=3.6 /MongoPort=10255`

### Other Notes

Use `pipreqs --force` to update requirements.txt