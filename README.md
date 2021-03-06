# logs-analysis

This is a project to uses psycopg2 to query a mock PostgreSQL database for a fictional news website.

There are three database inside the database `news`, which are `authors`, `artilces` and `log`.

Table `author` has following columns:

- id interger
- name text
- bio text

Table `articles` has following columns:

- author integer
- title text
- slug text
- lead text
- body text
- time timestamp
- id integer

Table `log` has following columns:

- path text
- ip inet
- method text
- status text
- time timestamp
- id integer

With the data from all these three tables, I will try to answer following questions:

1. What are the most popular three articles of all time? Which articles have been accessed the most?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

Please follow my steps to see how I get the result of these questions.

## Prerequisite

Installing Git, Virtual Box, and Vagrant

### Install Git

If you don't already have Git installed, download Git from git-scm.com. Install the version for your operating system.

On Windows, Git will provide you with a Unix-style terminal and shell (Git Bash). (On Mac or Linux systems you can use the regular terminal program.)

You will need Git to install the configuration for the VM.

### Install VirtualBox

VirtualBox is the software that actually runs the VM. You can download it from [virtual box](virtualbox.org). Install the platform package for your operating system. You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it.

Note: Currently (October 2017), the version of VirtualBox you should install is 5.1. Newer versions are not yet compatible with Vagrant.

Ubuntu 14.04 Note: If you are running Ubuntu 14.04, install VirtualBox using the Ubuntu Software Center, not the virtualbox.org web site. Due to a reported bug, installing VirtualBox from the site may uninstall other software you need.

### Install Vagrant

Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. You can download it from [vagrantup](vagrantup.com). Install the version for your operating system.

## Start up virtual machine

```shell
cd vagrant
vagrant up
vagrant ssh
```

## Load data to local database

Next, [download the data here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). You will need to unzip this file after downloading it. The file inside is called newsdata.sql. Put this file into the vagrant directory, which is shared with your virtual machine.

To build the reporting tool, you'll need to load the site's data into your local database.

To load the data, cd into the vagrant directory and use below PostgreSQL command:

```shell
cd /vagrant
psql - d news -f newsdata.sql
```

Running this command will connect to your installed database server and execute the SQL commands in the newsdata.sql file, creating tables and populating them with data.

## Create view for question 3

To simplify the solution for question 3, I used `CREATE VIEW` statements in an sql file . Before you run the pythone code, you need to run below code to import the views to the `news` database. You would only need to do this once, when you initially set up the database:

```shell
psql -d news -f create_views.sql
```

## Run the python code

### Run code and save result to .text file

1. Go to vagrant working directory

    ```shell
    cd /vagrant
    ```

2. Run the analysis code
  
    Run below code and save the result to the same directory

    ```shell
    python logs_analysis.py > result.txt
    ```

3. You can see my result in file `result.txt`.

### Run code and view result directly in shell

Alternatively, you can view my result directly in your shell window by running below code:

```shell
python logs_analysis.py
```