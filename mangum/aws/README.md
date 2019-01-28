# mangum

Mangum is a library that provides adapters and tools for ASGI applications used on FaaS platforms.

## Requirements

- AWS-CLI
- Python 3.6+

## Usage

Mangum adapters are intended to work with any ASGI application and any ASGI framework.

**Note**: One caveat to the ASGI adapter working universally is any platform-specific conflicts that need to be considered in a particular application, e.g. read-only filesystems.

* Edit `asgi.py` and uncomment and application try.

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
