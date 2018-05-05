# thehive-slack-webhook
A simple [Lambda](https://console.aws.amazon.com/lambda/home?region=us-east-1#/) function for delivering [TheHive](https://github.com/TheHive-Project/TheHive) webhooks to Slack

# Instructions
1. Make a lambda function with API and add the following Environmental variables:
- `hiveURL` = `https://yourhiveserver.com`
- `hookURL` = `https://hooks.slack.com/services/<yourslackwebhook>`
- `orgIcon` = `https://url-to-company-icon.com/icon.png`
- `orgName` = `Your Company, Inc.`
- `slackChannel` = `alert-channel`

2. Configure TheHive to send webhooks to your Lambda API endpoint

3. Return to kicking ass in the SOC!


# Contributors
- [@eric_capuano](https://twitter.com/eric_capuano)
- [@cyberGoatPsyOps](https://twitter.com/cyberGoatPsyOps)
- Huge thanks to the team at [The Hive Project](https://github.com/TheHive-Project/TheHive) for an awesome project.
