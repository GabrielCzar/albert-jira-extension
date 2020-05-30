# Simple Jira extension

![jira](readme-resources/jira.png)

### Installation

`sh -c "$(wget -O- https://raw.githubusercontent.com/gabrielczar/albert-jira-extension/master/install.sh)"`

### Configuration

In the first time that you type 'jira' will be necessary configure a Jira Server.

Just write the host of your jira server like `https://jira.server.com`.

This is a message that you see:

![alert message when the server configuration is missing](readme-resources/config-jira.png)

### Commands

- Open jira issue

Just type the word 'jira' following the issue ticket to open the Jira in your browser.

![image of the result after type 'jira'](readme-resources/project-jira.png)

- Remove jira server configuration

Just type `jira remove server`, then the action will start automatically.

![alert message when is trying to remove server configuration](readme-resources/remove-jira-server.png)
