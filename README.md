# Devcord

Devcord is a CLI tool designed to help you quickly manage your tasks as well as
help you monitor your time usage. Along with all the essential to-do list functionalities, Devcord allows you to select a task and start a session on it.

During a session, your time-spent on each of your activity is monitored for you to view later. This is useful for people who want to find out where their time is spent.

None of the data is stored on any server, it is all stored locally on your machine.

# Installation

With pip:

pip install devcord

# Usage

## For adding tasks

Simple add task:
- devcord tasks -a "task name" - devcord tasks --add "task name"

With description:
- devcord tasks -a "task name" -d - devcord tasks --add "task name" --description

_Opens scrollable text box to enter description_

With due date:
- devcord tasks -a "task name" -dd "dd/mm/yyyy" - devcord tasks --add "task name" --due "dd/mm/yyyy"

Complete by today:
- devcord tasks -a "task name" -t - devcord tasks --add "task name" --today

Complete in next 7 days:
- devcord tasks -a "task name" -w - devcord tasks --add "task name" --week

With priority (1-5):
- devcord tasks -a "task name" -p 3 - devcord tasks --add "task name" --priority 3

With labels:
- devcord tasks -a "task name" -lb "label" - devcord tasks --add "task name" --label "label"

Add subtask:
- devcord tasks -a "task name" -pid task_id - devcord tasks --add "task name" --parent task_id

## For listing tasks

Simple List tasks:
- devcord tasks -l - devcord tasks --list

List tasks by priority:
- devcord tasks -l -p 3 - devcord tasks --list --priority 3

List tasks by label:
- devcord tasks -l -lb "label" - devcord tasks --list --label "label"

List today's tasks:
- devcord tasks -l -t - devcord tasks --list --today

List tasks due in next 7 days:
- devcord tasks -l -w - devcord tasks --list --week

## For managing tasks

Selecting a task:
- devcord task -s task_id - devcord task --select task_id

Viewing description:
- devcord task -d - devcord task --description

_Opens a scrollable text box with description_

Show substask:
- devcord task -st - devcord task --subtask

Mark as inprogress:
- devcord task -i - devcord task --inprogress

Mark as complete:
- devcord task -c - devcord task --complete
