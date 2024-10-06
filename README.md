# Devcord

Devcord is a CLI tool designed to help you quickly manage your tasks as well as
help you monitor your time usage. Along with all the essential to-do list functionalities, Devcord allows you to select a task and start a session on it.

During a session, your time-spent on each of your activity is monitored for you to view later. This is useful for people who want to find out where their time is spent.

None of the data is stored on any server, it is all stored locally on your machine.

# Installation

With pip:

```bash
pip install --upgrade devcord
```

# Post Installation

To avoid typing devcord repetitively, register an alias in your shell configuration file.

For bash:

```bash
alias tasks="devcord tasks"
alias task="devcord task"
```

On each upgrade, run:

```bash
$ devcord init --migrate
```

This updates the database schema if any changes were made

# Usage

## For adding tasks

Simple add task:

```bash
$ devcord tasks -a "task name"
$ devcord tasks --add "task name"
```

With description:

```bash
$ devcord tasks -a "task name" -d
$ devcord tasks --add "task name" --desc
```

_Opens scrollable text box to enter description_

With due date:

```bash
$ devcord tasks -a "task name" -dd "dd/mm/yyyy"
$ devcord tasks --add "task name" --due "dd/mm/yyyy"
```

Complete by today:

```bash
$ devcord tasks -a "task name" -t
$ devcord tasks --add "task name" --today
```

Complete in current week:

```bash
$ devcord tasks -a "task name" -w
$ devcord tasks --add "task name" --week
```

With priority (1-5):

```bash
$ devcord tasks -a "task name" -p 3
$ devcord tasks --add "task name" --priority 3
```

With labels:

```bash
$ devcord tasks -a "task name" -lb "label"
$ devcord tasks --add "task name" --label "label"
```

Add subtask:

```bash
$ devcord tasks -a "task name" -st
$ devcord tasks --add "task name" --subtask
```

## For listing tasks

By default, in-progress and pending tasks are listed, with in-progress first followed by pending tasks and completed tasks are skipped.

Simple List tasks:

```bash
$ devcord tasks -l
$ devcord tasks --list
```

List tasks by priority:

```bash
$ devcord tasks -l -p 3
$ devcord tasks --list --priority 3
```

List tasks by label:

```bash
$ devcord tasks -l -lb "label"
$ devcord tasks --list --label "label"
```

List today's tasks:

```bash
$ devcord tasks -l -t
$ devcord tasks --list --today
```

List tasks due in current week:

```bash
$ devcord tasks -l -w
$ devcord tasks --list --week
```

List tasks by status:

```bash
$ devcord tasks -l -i
$ devcord tasks --list --completed
$ devcord tasks -l --pending
```

Specify Output Format:

```bash
$ devcord tasks -l -o json
$ devcord tasks --list --output text
```

Specify Output File:

```bash
$ devcord tasks -l --path "path/to/file"
```
## For managing tasks

Pass the keyword to perform required action on the task. The command will then prompt you through a fuzzy finder to enter
the task title. The keyword action would be performed on the selected task.


Viewing description:

```bash
$ devcord task -d
$ devcord task --desc
```

_Opens a scrollable text box with description_

Show substasks:

```bash
$ devcord task -st
$ devcord task --subtasks
```

Mark as inprogress:

```bash
$ devcord task -i
$ devcord task --inprogress
```

Mark as complete:

```bash
$ devcord task -c
$ devcord task --completed
```

Mark as pending:

```bash
$ devcord task -pd
$ devcord task --pending
```

Set deadline to this week:

```bash
$ devcord task -w
$ devcord task --week
```

Set deadline to today:

```bash
$ devcord task -t
$ devcord task --today
```

Delete Task:

```bash
$ devcord task -dl
$ devcord task --delete
```


Modify Title:

```bash
$ devcord task -n "new title"
$ devcord task --name "new title"
```

Modify Priority:

```bash
$ devcord task -p 3
$ devcord task --priority 3
```

Modify Deadline:

```bash
$ devcord task -dd "dd/mm/yyyy"
$ devcord task --deadline "dd/mm/yyyy"
```

Modify Labels:

```bash
$ devcord task -lb "label"
$ devcord task --label "label"
```

Modify Completed Task:

```bash
$ devcord task -ar -n "new title"
$ devcord task --archive --name "new title"
```
## Jira Integration

With Jira integration you can view all your issues on devcord itself and sync
them as when required with a single command. On your first use of any of the following commands,
you'd be ask to setup your configuration for Jira.

Sync with Jira

```bash
$ devcord jira --sync
```

Set Organization URL

```bash
$ devcord jira --url
```

Set Organization Email

```bash
$ devcord jira --email
```

Set Jira Access token

```bash 
$ devcord jira --token
```

|**Category**                  | **Description**                                                             | **Command**|
| :---         |     :---      |          :--- |
| | | |
| **Installation**              | Installs or upgrades Devcord CLI tool.                                     | pip install --upgrade devcord                                          |
| **Post Installation**         | Register aliases to avoid repetitive typing.                               | `alias tasks="devcord tasks"`<br>`alias task="devcord task"`                                           |
|                               | Updates the database schema on upgrade.                                    | `devcord init --migrate`                                                                                 |
| **Add Tasks**                 | Adds a simple task.                                                        | `devcord tasks -a "task name"`<br>`devcord tasks --add "task name"`                                      |
|                               | Adds a task with a description (opens a scrollable text box).              | `devcord tasks -a "task name" -d`<br>`devcord tasks --add "task name" --desc`                           |
|                               | Adds a task with a due date.                                               | `devcord tasks -a "task name" -dd "dd/mm/yyyy"`<br>`devcord tasks --add "task name" --due "dd/mm/yyyy"` |
|                               | Marks the task to be completed by today.                                   | `devcord tasks -a "task name" -t`<br>`devcord tasks --add "task name" --today`                         |
|                               | Marks the task to be completed in the current week.                        | `devcord tasks -a "task name" -w`<br>`devcord tasks --add "task name" --week`                          |
|                               | Adds a task with priority (1-5).                                          | `devcord tasks -a "task name" -p 3`<br>`devcord tasks --add "task name" --priority 3`                  |
|                               | Adds a task with labels.                                                  | `devcord tasks -a "task name" -lb "label"`<br>`devcord tasks --add "task name" --label "label"`        |
|                               | Adds a subtask.                                                           | `devcord tasks -a "task name" -st`<br>`devcord tasks --add "task name" --subtask`                      |
| **List Tasks**                | Lists in-progress and pending tasks (completed tasks are skipped).        | `devcord tasks -l`<br>`devcord tasks --list`                                                             |
|                               | Lists tasks by priority.                                                  | `devcord tasks -l -p 3`<br>`devcord tasks --list --priority 3`                                          |
|                               | Lists tasks by label.                                                     | `devcord tasks -l -lb "label"`<br>`devcord tasks --list --label "label"`                                |
|                               | Lists today's tasks.                                                      | `devcord tasks -l -t`<br>`devcord tasks --list --today`                                               |
|                               | Lists tasks due in the current week.                                      | `devcord tasks -l -w`<br>`devcord tasks --list --week`                                                 |
|                               | Lists tasks by status.                                                    | `devcord tasks -l -i`<br>`devcord tasks --list --completed`<br>`devcord tasks -l --pending`             |
|                               | Specifies output format.                                                  | `devcord tasks -l -o json`<br>`devcord tasks --list --output text`                                      |
|                               | Specifies output file.                                                    | `devcord tasks -l --path "path/to/file"`                                                                 |
| **Manage Tasks**              | Views the description of a task (opens a scrollable text box).           | `devcord task -d`<br>`devcord task --desc`                                                               |
|                               | Shows subtasks of the selected task.                                      | `devcord task -st`<br>`devcord task --subtasks`                                                          |
|                               | Marks the task as in-progress.                                            | `devcord task -i`<br>`devcord task --inprogress`                                                         |
|                               | Marks the task as complete.                                               | `devcord task -c`<br>`devcord task --completed`                                                          |
|                               | Marks the task as pending.                                                | `devcord task -pd`<br>`devcord task --pending`                                                           |
|                               | Sets deadline to this week.                                               | `devcord task -w`<br>`devcord task --week`                                                               |
|                               | Sets deadline to today.                                                   | `devcord task -t`<br>`devcord task --today`                                                              |
|                               | Deletes the task.                                                         | `devcord task -dl`<br>`devcord task --delete`                                                            |
|                               | Modifies the task title.                                                  | `devcord task -n "new title"`<br>`devcord task --name "new title"`                                     |
|                               | Modifies the task priority.                                               | `devcord task -p 3`<br>`devcord task --priority 3`                                                      |
|                               | Modifies the task deadline.                                               | `devcord task -dd "dd/mm/yyyy"`<br>`devcord task --deadline "dd/mm/yyyy"`                             |
|                               | Modifies task labels.                                                    | `devcord task -lb "label"`<br>`devcord task --label "label"`                                           |
|                               | Modifies a completed task.                                               | `devcord task -ar -n "new title"`<br>`devcord task --archive --name "new title"`                       |
| **Jira Integration**          | Syncs with Jira.                                                          | `devcord jira --sync`                                                                                     |
|                               | Sets the organization URL.                                               | `devcord jira --url`                                                                                      |
|                               | Sets the organization email.                                             | `devcord jira --email`                                                                                   |
|                               | Sets the Jira access token.                                              | `devcord jira --token`                                                                                   |

