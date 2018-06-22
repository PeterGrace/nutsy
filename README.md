# nutsy
I wrote this once before for an employer, I decided to rewrite it again and open-source it.

Nutsy is a quick little slack bot that notifies a given webhook url that there are monitoring
entries that might require attention.

How to run:  `docker run -e NUTSY_DD_API_KEY=<datadog_api_key> -e NUTSY_DD_APP_KEY=<datadog_app_key> -e NUTSY_SLACK_URL=<slack_webhook_url> -ti --rm petergrace/nutsy`
