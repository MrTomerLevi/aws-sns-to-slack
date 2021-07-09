# Monitoring App (SNS to Slack)

This app contains a monitoring SNS topic that can get notifications from other AWS resources.<br/>
A Lambda function will send every notification arriving to SNS to Slack using a Slack WebHook.

This app is built using AWS SAM and required SAM CLI https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html 

![Alt text](images/example-slack.png?raw=true "Example Slack message")

## Lambda Function
The Lambda function is written in Python and is using AWS Lambda Powertools https://awslabs.github.io/aws-lambda-powertools-python/latest/
Lambda Powertools is set to:
* send Lambda function logs to CloudWatch
* send tracing info to X-Ray 
* get SNS message as class rather than as default Lambda event `dict`

## Creating a Slack webhook
 1. Navigate to https://<your-team-domain>.slack.com/services/new
 2. Search for and select "Incoming WebHooks".
 3. Choose the default channel where messages will be sent and click "Add Incoming WebHooks Integration".
 4. Copy the webhook URL from the setup instructions and use it in the next section.

## SAM Commands Examples
### Build
```
sam build --use-container --cached --parameter-overrides Env=develop SlackChannel=#develop-notifications SlackHookURL=<YOUR_WEBHOOK_URL>
```

### Local test (this will send a real message to Slack):
```
sam local invoke -e events/sns-cloudwatch.json LambdaSlack --parameter-overrides 'Env=develop SlackChannel=#develop-notifications SlackHookURL=<YOUR_WEBHOOK_URL>' --debug
```

### Deployment:

```
sam deploy --stack-name monitoring-and-alerting-<ENVIRONMENT> --s3-bucket <YOUR_S3_BUCKET> --s3-prefix monitoring_and_alerting  --capabilities CAPABILITY_IAM  --parameter-overrides Env=develop SlackChannel=#develop-notifications SlackHookURL=<YOUR_WEBHOOK_URL>-
```

# Getting SNS Topic ARN
Other AWS resources can get the SNS topic ARN using one of the following ways:
* SSM Parameters store. The SSM Parameter name is `alerting-sns-topic-arn-<environment>`<br/>
* CloudFormation stack outputs. After deployment navigate to CloudFormation -> monitoring-and-alerting -> Outputs
* SAM outputs will contain the ARN, for example:
```shell
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Outputs                                                                                                                                                                                                                
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Key                 SNSTopicAlertingArn                                                                                                                                                                                
Description         Alerting SNS Topic ARN                                                                                                                                                                             
Value               arn:aws:sns:us-east-1:12345678:monitoring-and-alerting-SNSTopicAlerting-ABCD1234                                                                                                          
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
```
