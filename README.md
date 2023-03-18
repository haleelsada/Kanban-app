# Kanban-app
A platform that helps to manage and track tasks
Kanban-app helps people to track and manage tasks and works.
## Frameworks used
- Flask for application code
- Jinja2 templates + Bootstrap for HTML generation and styling
- SQLite for data storage
- All demos should be possible on a standalone platform like replit.com and should not require setting up new servers for database and frontend management


## Features
- User can create tasks and group them
- Users can see statistical data related to tasks
- Indicate deadline of task passed or not

## Installation

To run this app on your local machine, follow these steps:

Install `DB Browser for SQlite` to manage database

1.Clone this repository
```
git clone https://github.com/haleelsada/Kanban-app.git
```
2.open terminal inside this repository and run local_setup.sh to setup environment and isntall packages needed
```
cd Kanban-app
sh local_setup.sh
```
3.activate virtual environment
```
source .env/bin/activate
```
4.run local_run.sh to run the app
```
sh local_run.sh
```
5.open a new terminal branch to run celery worker
```
sh local_workers.sh
```
6.open another terminal to run celery beat
```
sh local_beat.sh
```
7.open browser and search
```
http://127.0.0.1:8080/
```
```
here are few default users:
name: batman@gmail.com
password: batman
name: thomasshelby@gmail.com
password: thomas
name: jacksparrow@gmail.com
password: jack
name: jamesbond@gmail.cm
password: james
name: joker@gmail.com
password: joker
```

## Contributers
[Haleel Sada](https://github.com/haleelsada)
## Licence
This project is licensed under the MIT License - see the [LICENSE](https://github.com/haleelsada/Netvork/blob/main/LICENSE) file for details.

