# Mangum

Mangum is a library that provides an ASGI adapter for use with AWS Lambda & API Gateway.

## Testing the examples

Below is just one potential way to deploy the application, it uses a [SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-template-basics.html) template and is very basic.

## Requirements

- AWS-CLI
- Python 3.6+

## Initial setup

The `Mangum` adapter is intended to "just work" with any ASGI application and any ASGI framework, but non-ASGI-specific behaviour that conflicts with the AWS Lambda environment may cause issues.

* Edit `asgi.py` and uncomment and application try.

* Edit `requirements.txt` to include any dependencies, ie: if you are using a framework.

## Packaging & deployment

* Build the Python dependencies

```shell
$ pip3 install -r requirements.txt -t ./build
```

* Include the `asgi.py` in the `build` folder

```shell
$ cp asgi.py build/
```

* Create an S3 bucket for your application

```shell
$ aws s3 mb s3://<bucket-name> --region <region-name>
```

* Package the application

```shell
$ aws cloudformation package \
--template-file template.yaml \
--output-template-file packaged.yaml \
--s3-bucket <bucket-name>
```

* Deploy the package

```shell
$ aws cloudformation deploy \
--template-file packaged.yaml \
--stack-name <stack-name> \
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

If everything went as expected, you should see the application response.
