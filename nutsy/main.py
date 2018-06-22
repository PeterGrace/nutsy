import click
import requests
import datetime

now = datetime.datetime.now()

BOT_ICON = "https://i.imgur.com/gqDVfU5.jpg"
BOT_NAME = "Nutsy"


def get_triggered_monitors(api_key, application_key):
    '''contact datadog and get the current monitor status'''
    auth_payload = {"api_key": api_key, "application_key": application_key}
    url = "https://api.datadoghq.com/api/v1/monitor"
    rs = requests.get(url, params=auth_payload)
    rs.raise_for_status()
    return rs.json()


def process_monitors(monitors):
    '''count incidents of monitor statuses'''
    results = {}
    for monitor in monitors:
        if (len(monitor['options']['silenced']) > 0):
            monitor['overall_state']='Silenced'
        try:
            results[monitor['overall_state']] += 1
        except KeyError:
            results[monitor['overall_state']] = 1
    return results


def generate_slack_payload(results):
    '''create message payload that slack requires'''
    message = {}
    attachment = {}
    fields = []
    for result in results.keys():
        field = {}
        field["title"] = "Status: %s" % result
        field["value"] = results[result]
        field["short"] = True
        fields.append(field)
    attachment['fields'] = fields
    attachment["title"] = "Current Monitor Status as of %s" % now.strftime("%Y-%m-%d %H:%M %Z")
    attachment["title_link"] = "https://app.datadoghq.com/monitors/manage"
    message["icon_url"] = BOT_ICON
    message["username"] = BOT_NAME
    message["attachments"] = [attachment]
    return message


@click.command()
@click.argument("dd-api-key", envvar="NUTSY_DD_API_KEY")
@click.argument("dd-app-key", envvar="NUTSY_DD_APP_KEY")
@click.argument("slack-url", envvar="NUTSY_SLACK_URL")
def main(dd_api_key, dd_app_key, slack_url):
    '''main function'''

    monitors = get_triggered_monitors(dd_api_key, dd_app_key)
    results = process_monitors(monitors)
    message = generate_slack_payload(results)
    requests.post(slack_url, json=message)


if __name__ == '__main__':
    main()
