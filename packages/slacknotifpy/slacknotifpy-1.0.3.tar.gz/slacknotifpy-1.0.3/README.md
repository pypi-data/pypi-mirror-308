# SlackNotifPy

A Python command-line tool to send Slack notifications for job completion. This tool allows you to set up a Slack bot token and channel ID for each project, enabling job-specific notifications.

## Installation

Install the package in your project:

```bash
pip install .
```

## Usage

### 1. Set the Slack Configuration

To configure the Slack token and channel for the project, run:

```bash
slacknotif config setconfig <job_script.py>
```

This command prompts you to enter your Slack bot token and channel ID, storing them in a `.slacknotif_config` file in the project directory where `<job_script.py>` is located.

### 2. Run a Job and Notify

Once configured, you can run a job and send a notification to the specified Slack channel upon completion:

```bash
slacknotif <job_script.py> <job_name>
```

-   `<job_script.py>`: The Python script you want to run.
-   `<job_name>`: A name for the job, used in the Slack message.

For example, if `job_script.py` completes successfully, the Slack message will read:

> "job_name completed successfully"

If the script fails, the message will read:

> "job_name failed"

## Configuration Details

The configuration file `.slacknotif_config` is saved in the same directory as the job script. It contains:

-   `SLACK_TOKEN`: Your Slack bot token, which is used for authentication.
-   `CHANNEL_ID`: The Slack channel ID where notifications will be sent.

Each project directory with a `.slacknotif_config` file can have its own Slack configuration, making it easy to set up notifications for different projects.

## Security

The `.slacknotif_config` file is saved with restricted permissions (readable and writable only by the file owner) to ensure the security of your Slack token and channel ID.

## Example

1. Set Configuration:

```bash
slacknotif config setconfig job_script.py
```

Enter your Slack token and channel ID when prompted.

2. Run Job with Notification:

```bash
slacknotif job_script.py "Data Processing Job"
```

This will run job_script.py and send a message to Slack with the status of "Data Processing Job".

## Dependencies

-   `slack_sdk`: Used for sending messages to Slack.

## License

This project is licensed under the MIT License.
