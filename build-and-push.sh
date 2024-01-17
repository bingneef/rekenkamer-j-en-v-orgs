VERSION=${1:-'latest'}

docker build . --platform linux/amd64 -f Dockerfile -t bingneef/rekenkamer-elastic-export:${VERSION}
docker push bingneef/rekenkamer-elastic-export:${VERSION}

