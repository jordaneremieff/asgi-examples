# Mangum

[Mangum](https://github.com/erm/mangum) is a library that provides an ASGI adapter for use with AWS Lambda & API Gateway.

The `Mangum` adapter class is intended to "just work" with any ASGI application or framework, but non-ASGI-specific behaviour that conflicts with the environment may need to be addressed specifically depending on the particular application.

In this example, we will use the [SAM CLI](https://aws.amazon.com/serverless/sam/) for testing and deployment, but you may use alternative packaging and deployment methods.

Read more about the SAM CLI [here](https://github.com/awslabs/aws-sam-cli/blob/develop/docs/usage.md).

## Requirements

* AWS CLI already configured with at least PowerUser permission
* [Python 3 installed](https://www.python.org/downloads/)
* [Docker installed](https://www.docker.com/community-edition)
* [Python Virtual Environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/)

## Setup

There are several examples in the `asgi.py` file, the default is a raw ASGI application with no dependencies. You will need to uncomment an app example in `asgi.py` and edit `requirements.txt` to include the dependencies for a particular framework app.

## Build

The following command will build the project:

```bash
sam build
```

Some dependencies (Starlette, for example) contain native modules that need to be compiled specifically for the operating system running on AWS Lambda, the `--use-container` argument will build inside a Lambda-like Docker container:

```bash
sam build --use-container
```
 
By default, this command writes built artifacts to `.aws-sam/build` folder.

### Local development

**Invoking function locally through local API Gateway**

```bash
sam local start-api
```

If the previous command ran successfully you should now be able to hit the following local endpoints to invoke your function:

`http://127.0.0.1:3000/asgi/quart/hello`
`http://127.0.0.1:3000/asgi/bocadillo/hello`
`http://127.0.0.1:3000/asgi/starlette/hello`
`http://127.0.0.1:3000/asgi/fastapi/hello`


## Packaging & deployment

* Create an S3 bucket for your application

```shell
$ aws s3 mb s3://BUCKET_NAME --region <region-name>
```

* Package

```bash
$ sam package \
    --output-template-file packaged.yaml \
    --s3-bucket REPLACE_THIS_WITH_YOUR_S3_BUCKET_NAME
```

* Create a stack & deploy

```bash
$ sam deploy \
    --template-file packaged.yaml \
    --stack-name REPLACE_THIS_WITH_A_STACK_NAME \
    --capabilities CAPABILITY_IAM
```

* Retrieve the endpoints

```shell
$ aws cloudformation describe-stacks \
--stack-name <stack-name> \
--query Stacks[].Outputs
```

Then you should see an endpoint similar to this:

```shell
https://xxxxxx.execute-api.ap-southeast-1.amazonaws.com/Prod/
```

