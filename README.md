# lambda-web-adapter-flask-search_bar
Web application for searching musical artist information from XML file

This Python Flask web application allows users to search for information about musical artists and their albums from a provided XML file. Users can search for artists by name and view detailed information about the artist, including their name, city of origin, biography, and website (if available). The application also displays details of albums associated with the artist, including the album title, release year, and list of songs.

Key features:

    Load data from an XML file containing information about artists and their albums
    Search for artists by name
    Display detailed information about the artist
    Display details of albums associated with the artist

Technologies used:
    
    Python
    Flask
    Docker
    SAM(Aws Serverless Application Model)
    CloudFormation
    Jinja
    ElementTree (XML library)
    Html
    CSS


The application can be deployed in an AWS account using the [Serverless Application Model](https://github.com/awslabs/serverless-application-model). The `template.yaml` file in the root folder contains the application definition.

The top level folder is a typical AWS SAM project. The `app` directory is a flask application with a [Dockerfile](app/Dockerfile).

```dockerfile
FROM public.ecr.aws/docker/library/python:3.8.12-slim-buster
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.8.1 /lambda-adapter /opt/extensions/lambda-adapter
WORKDIR /var/task
COPY app.py requirements.txt ./
RUN python3.8 -m pip install -r requirements.txt
CMD ["gunicorn", "-b=:8080", "-w=1", "app:app"]
```

Line 2 copies lambda adapter binary into /opt/extensions. This is the only change to run the Flask application on Lambda.

```dockerfile
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.8.1 /lambda-adapter /opt/extensions/lambda-adapter
```

## Pre-requisites

The following tools should be installed and configured.
* [AWS CLI](https://aws.amazon.com/cli/)
* [SAM CLI](https://github.com/awslabs/aws-sam-cli)
* [Python](https://www.python.org/)
* [Docker](https://www.docker.com/products/docker-desktop)


## Deploy to Lambda
Navigate to the sample's folder and use the SAM CLI to build a container image
```shell
$ aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws
$ sam build
```

This command compiles the application and prepares a deployment package in the `.aws-sam` sub-directory.

To deploy the application in your AWS account, you can use the SAM CLI's guided deployment process and follow the instructions on the screen

```shell
$ sam deploy --guided
```
Please take note of the container image name.
Once the deployment is completed, the SAM CLI will print out the stack's outputs, including the new application URL. You can use `curl` or a web browser to make a call to the URL

```shell
...
---------------------------------------------------------------------------------------------------------
OutputKey-Description                        OutputValue
---------------------------------------------------------------------------------------------------------
FlaskApi - URL for application            https://xxxxxxxxxx.execute-api.us-west-2.amazonaws.com/
---------------------------------------------------------------------------------------------------------
...

$ curl https://xxxxxxxxxx.execute-api.us-west-2.amazonaws.com/
```

## Run the docker locally

We can run the same docker image locally, so that we know it can be deployed to ECS Fargate and EKS EC2 without code changes.

```shell
$ docker run -d -p 8080:8080 {ECR Image}

```

Use curl to verify the docker container works.

```shell
$ curl localhost:8080/ 
```
