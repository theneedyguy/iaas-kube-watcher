#!/bin/bash
docker build . -t ckevi/kubepy:latest
docker tag ckevi/kubepy:latest ckevi/kubepy:1.2-20
docker push ckevi/kubepy:latest
docker push ckevi/kubepy:1.2-20
