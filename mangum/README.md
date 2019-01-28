# Mangum

[Mangum](https://github.com/erm/mangum) is a library that provides adapters and tools for ASGI applications used on FaaS platforms.

## Requirements

- AWS-CLI
- Python 3.6+

## Setup

Mangum adapters are intended to work with any ASGI application and any ASGI framework.

**Note**: One caveat to the ASGI adapters being universal would be any platform-specific conflicts that need to be considered for a particular application, e.g. read-only filesystems.

* Edit `asgi.py` and uncomment and application to try.

* Edit `requirements.txt` to include any dependencies, ie: if you are using a framework.

## Packaging & deployment

Some basic CLI tooling is provided in Mangum to wrap this deployment process, but it's experimental so the instructions to follow will be the specific AWS CLI methods to use:

* Build the Python dependencies

```shell
$ pip3 install -r requirements.txt -t ./build
```

* Create an S3 bucket for your application

```shell
$ aws s3 mb s3://<bucket-name> --region <region-name>
```

* Create a `build/` directory and copy the application

```shell
$ mkdir build/
$ cp asgi.py build/
```

* Package the application dependencies

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
--stack-name <stack-name>
--query Stacks[].Outputs
```
