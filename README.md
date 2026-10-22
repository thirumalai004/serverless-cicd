# serverless-cicd

Jenkins pipeline that tests, packages and deploys an AWS Lambda function
behind an API Gateway HTTP API, with automatic rollback.

## Structure

    serverless-cicd/
    ├── app/lambda_function.py     Lambda handler
    ├── tests/test_handler.py      Unit tests (pytest)
    ├── requirements.txt           Lambda runtime dependencies
    ├── Jenkinsfile                Pipeline definition
    ├── .gitignore
    └── README.md

## Pipeline stages

Test -> Package -> Deploy (publish version, move `prod` alias) -> Smoke test.
If any stage fails after deploy, the `prod` alias is moved back to the previous version.

## Setup values (edit in Jenkinsfile if yours differ)

- Region: ap-southeast-2
- Function: my-api-function (alias: prod)
- API URL: https://e55r5pw1y6.execute-api.ap-southeast-2.amazonaws.com/
