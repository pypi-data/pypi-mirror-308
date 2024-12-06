#!/usr/bin/env python3

import json
import os
import stat
import subprocess
import sys

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def get_config_path(job_script_path):
    project_dir = os.path.dirname(os.path.abspath(job_script_path))
    return os.path.join(project_dir, ".slacknotif_config")


def set_config(config_path):
    token = input("Enter your Slack token: ").strip()
    channel_id = input("Enter you Slack Channel ID").strip()
    config = {"SLACK_TOKEN": token, "CHANNEL_ID": channel_id}

    with open(config_path, "w") as config_file:
        json.dump(config, config_file)

    os.chmod(config_path, stat.S_IRUSR | stat.S_IWUSR)

    print(f"SlackNotif config has been saved to {config_path}")


def load_config(config_path):
    if not os.path.exists(config_path):
        print(
            "SlackNotif config not set for this project. Use `slacknotif config settoken <job_script.py>` to set it."
        )
        sys.exit(1)

    with open(config_path, "r") as config_file:
        config = json.load(config_file)

    slack_token = config.get("SLACK_TOKEN")
    channel_id = config.get("channel_id")

    if not slack_token or not channel_id:
        print(
            "Error: SLACK_TOKEN or CHANNEL_ID is missing in the configuration Use `slacknotif config setconfig <job_script.py>` to reset it."
        )
        sys.exit(1)

    return slack_token, channel_id


def notify(job_script, job_name):
    config_path = get_config_path(job_script)
    slack_token, channel_id = load_config(config_path)

    client = WebClient(token=slack_token)
    bot_name = "SlackNotifPy"

    try:
        subprocess.run(["python", job_script], check=True)
        message = f"{job_name} completed successfully"
    except subprocess.CalledProcessError:
        message = f"{job_name} failed"

    try:
        client.chat_postMessage(channel=channel_id, text=message, username=bot_name)
        print("Message sent successfully!")
    except SlackApiError as e:
        print(f"Error sending message: {e}")


def main():
    if len(sys.argv) < 2:
        print("Usage: slacknotif <command> [<args>]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "config" and len(sys.argv) == 4 and sys.argv[2] == "setconfig":
        job_script = sys.argv[3]
        config_path = get_config_path(job_script)
        set_config(config_path)
    elif len(sys.argv) == 3:
        job_script = sys.argv[1]
        job_name = sys.argv[2]
        notify(job_script, job_name)
    else:
        print("Usage:")
        print(
            "  slacknotif <job_script.py> <job_name>           # Run job and send notification"
        )
        print(
            "  slacknotif config setconfig <job_script.py>      # Set SlackNotif config for the project"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
