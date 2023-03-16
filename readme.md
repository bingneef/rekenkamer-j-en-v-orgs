# HOWTO

## Step to run
1. Create a .env file with the following content:
```sh
S
```
2. Run the following command:
```sh
docker run --env-file .env --mount type=bind,src=/${PWD},dst=/app/output bingneef/rekenkamer-j-en-v-orgs:latest
```