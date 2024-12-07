#!/usr/bin/env python3

import argparse
import json
import locale
import os
import stat
import subprocess
import sys
from typing import Optional

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def get_config_path(job_script_path: str) -> str:
    """Get the path to the config file.

    Args:
        job_script_path (str): Path to the job script.

    Returns:
        str: Path to the config file.
    """
    project_dir = os.path.dirname(os.path.abspath(job_script_path))
    print(f"Looking for config in {project_dir}...")
    return os.path.join(project_dir, ".slacknotif_config")

def set_message_flow() -> tuple[str, str]:
    """Set custom messages for success and failure notifications.

    Returns:
        tuple[str, str]: Success message and failure message.
    """
    print("\nYou can use {job_name} in your messages as a placeholder")
    print("Example: '{job_name} did the thing!'")
    success_msg = input(
        "Enter custom success message (press Enter to use default): "
    ).strip()
    failure_msg = input(
        "Enter custom failure message (press Enter to use default): "
    ).strip()
    return success_msg, failure_msg


def set_config(config_path: str) -> None:
    """Set the Slack token, channel ID, and custom messages.

    Args:
        config_path (str): Path to the config file.
    """
    print("Setting up SlackNotifPy...")
    print("Please enter your Slack token and channel ID.")
    print("You can find your Slack token and channel ID in your Slack app settings.")
    token = input("Enter your Slack token: ").strip()
    channel_id = input("Enter your Slack Channel ID: ").strip()
    success_msg, failure_msg = set_message_flow()

    config = {
        "SLACK_TOKEN": token,
        "CHANNEL_ID": channel_id,
        "SUCCESS_MSG": success_msg,
        "FAILURE_MSG": failure_msg,
    }

    with open(config_path, "w", encoding=locale.getencoding()) as config_file:
        json.dump(config, config_file)

    os.chmod(config_path, stat.S_IRUSR | stat.S_IWUSR)

    print(f"SlackNotif config has been saved to {config_path}")


def load_config(config_path: str) -> tuple[str, str, str, str]:
    """Load the Slack token, channel ID, and custom messages from the config file.

    Args:
        config_path (str): Path to the config file.

    Returns:
        tuple[str, str, str, str]: Slack token, channel ID, success message, and failure message.
    """
    if not os.path.exists(config_path):
        print(
            "SlackNotif config not set for this project. Use `slacknotif config setconfig <job_script.py>` to set it."
        )
        sys.exit(1)

    with open(config_path, "r", encoding=locale.getencoding()) as config_file:
        config = json.load(config_file)

    slack_token = config.get("SLACK_TOKEN")
    channel_id = config.get("CHANNEL_ID")
    success_msg = config.get("SUCCESS_MSG")
    failure_msg = config.get("FAILURE_MSG")

    if not slack_token or not channel_id:
        print(
            "Error: SLACK_TOKEN or CHANNEL_ID is missing in the configuration. Use `slacknotif config setconfig <job_script.py>` to reset it."
        )
        sys.exit(1)

    return slack_token, channel_id, success_msg, failure_msg


def format_message(message_template: str, job_name: str) -> str:
    """Format the message with the job name.

    Args:
        message_template (str): Message template with placeholders.
        job_name (str): Name of the job.

    Returns:
        str: Formatted message.
    """
    if not message_template:
        return None
    try:
        return message_template.format(job_name=job_name)
    except KeyError:
        print("Warning: Invalid message template. Using default message.")
        return None


def get_default_job_name(script_path: str) -> str:
    """Get the default job name from the script path.

    Args:
        script_path (str): Path to the job script.

    Returns:
        str: Default job name.
    """
    return os.path.splitext(os.path.basename(script_path))[0]


def notify(job_script: str, job_name: Optional[str] = None) -> None:
    """Send a notification to Slack.

    Args:
        job_script (str): Path to the job script.
        job_name (str): Name of the job.
    """
    if job_name is None:
        job_name = get_default_job_name(job_script)

    config_path = get_config_path(job_script)
    slack_token, channel_id, success_msg, failure_msg = load_config(config_path)

    client = WebClient(token=slack_token)
    bot_name = "SlackNotifPy"

    try:
        subprocess.run(["python", job_script], check=True)
        formatted_success = format_message(success_msg, job_name)
        message = formatted_success or f"{job_name} completed successfully"
    except subprocess.CalledProcessError:
        formatted_failure = format_message(failure_msg, job_name)
        message = formatted_failure or f"{job_name} failed"

    try:
        client.chat_postMessage(channel=channel_id, text=message, username=bot_name)
        print("Message sent successfully!")
    except SlackApiError as e:
        print(f"Error sending message: {e}")

def set_messages(config_path: str) -> None:
    """Set custom messages for success and failure notifications.

    Args:
        config_path (str): Path to the config file.
    """
    if not os.path.exists(config_path):
        print("Config file doesn't exist. Please set up the basic config first.")
        sys.exit(1)

    with open(config_path, "r", encoding=locale.getencoding()) as config_file:
        config = json.load(config_file)

    success_msg, failure_msg = set_message_flow()

    config["SUCCESS_MSG"] = success_msg
    config["FAILURE_MSG"] = failure_msg

    with open(config_path, "w", encoding=locale.getencoding()) as config_file:
        json.dump(config, config_file)

    print("Custom messages have been updated!")


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the SlackNotifPy CLI.

    Returns:
        argparse.ArgumentParser: The argument parser for the SlackNotifPy CLI.
    """
    parser = argparse.ArgumentParser(
        description="SlackNotifPy - Send Slack notifications on python job completion",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser(
        "run", help="Run a Python script and send a Slack notification"
    )
    run_parser.add_argument(
        "script", nargs="?", help="Path to the Python script to run"
    )
    run_parser.add_argument(
        "job_name",
        nargs="?",
        help="Name of the job (used in notifications), defaults to script filename",
    )

    config_parser = subparsers.add_parser(
        "config", help="Configure SlackNotifPy settings"
    )
    config_subparsers = config_parser.add_subparsers(
        dest="config_command", help="Configuration commands"
    )

    setconfig_parser = config_subparsers.add_parser(
        "setconfig", help="Set configuration (token, channel, custom messages)"
    )
    setconfig_parser.add_argument(
        "script", help="Path to a script in the project directory"
    )

    setmessages_parser = config_subparsers.add_parser(
        "setmessages", help="Set custom notification messages"
    )
    setmessages_parser.add_argument(
        "script", help="Path to a script in the project directory"
    )

    return parser


def main() -> None:
    """Main function to run the SlackNotifPy CLI."""
    parser = create_parser()
    args = parser.parse_args()
    print(args)

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "run":
        if not args.script:
            parser.parse_args(["run", "--help"])
            sys.exit(1)

        notify(args.script, args.job_name)

    elif args.command == "config":
        if not args.config_command:
            parser.parse_args(["config", "--help"])
            sys.exit(1)

        config_path = get_config_path(args.script)

        if args.config_command == "setconfig":
            set_config(config_path)
        elif args.config_command == "setmessages":
            set_messages(config_path)


if __name__ == "__main__":
    main()
