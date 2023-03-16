VERSION=${1:-'latest'}

docker build . --platform linux/amd64 -f Dockerfile -t bingneef/rekenkamer-j-en-v-orgs:${VERSION}
docker push bingneef/rekenkamer-j-en-v-orgs:${VERSION}

#docker build . --platform linux/arm64 -f Dockerfile -t bingneef/rekenkamer-j-en-v-orgs:${VERSION}
#docker push bingneef/rekenkamer-j-en-v-orgs:${VERSION}
