# Downloading Samples

This page describes how to download samples for use with InterSystems IRIS® data platform, as well as how to create a namespace and database to hold the samples.

## 1 Introduction to Samples

The installation kit for InterSystems IRIS does not include samples; this enables the kit to be as small as possible. Instead,
samples are available online at GitHub. In GitHub terms, each sample is provided as a repository or repo.

Each of the sample repos includes:

- A detailed README file with specific setup instructions

- A specialized routine that sets up the sample after you have downloaded it to a local disk.

Note that the InterSystems account (https://github.com/intersystems) includes many other repos. The repos that are meant for use with the InterSystems IRIS documentation are tagged with intersystems-samples and have names starting with Samples.

If you are familiar with GitHub, skip ahead to Creating a Namespace and Database to Hold Samples.

If you are not familiar with GitHub, see the next section for how to download samples. You do not need a GitHub account.

## 2 Downloading a Sample

You can download a GitHub repo as a single packaged unit, which you can then uncompress as a directory with multiple
files. Choose which method you prefer:

- Using a Web Browser to Download a Repo

- Using Linux or UNIX® Command Line to Download a Repo If Git is installed on your machine, you can access the repo by cloning it, as described in Cloning a repository on the GitHub website (https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository)

### 2.1 Using a Web Browser to Download a Repo

To download a repo using a web browser:

1. Click the link for that repo. The upper part of the page summarizes the contents, and the lower part displays the

README file for the repo.

2. Click the Clone or download button, visible from the default Code tab. Then click Download ZIP.

3. The browser downloads a .zip file that contains the full repo. Depending on your bro wser settings, you may get prompted

for a location. If not, check the usual download location for your browser.

4. Uncompress the .zip file. The uncompressed directory contains a README.md file, a LICENSE file, a buildsample

subdirectory, and other files and subdirectories.

Creating a Namespace and Database to Hold Samples

### 2.2 Using Linux or UNIX® Command Line to Download a Repo

To download a repo using Linux or UNIX® command line:

1. From the shell, type:

wget -qO- https://github.com/intersystems/repo-name/archive/master.tar.gz | tar xvz -C /samples

where repo-name is the name of the repo you want, and /samples is an existing directory.

2. Press Enter to download the repo into the /samples directory.

The uncompressed directory contains a README.md file, a LICENSE file, a buildsample subdirectory, and other files and subdirectories.

## 3 Creating a Namespace and Database to Hold Samples

Many of the samples include InterSystems IRIS classes or routines and are meant to be loaded into an InterSystems IRIS instance. InterSystems recommends that you create a dedicated namespace and database called SAMPLES for this purpose and then load the samples into this namespace.

To create the SAMPLES namespace and database:

1.

2.

In the Management Portal, click System Administration > Configuration > System Configuration > Namespaces.

In the Name of the Namespace, enter SAMPLES.

3. Next to Select an existing database for Globals, click Create New Database.

In the next step, you are starting to create the namespace.

4. For Enter the name of your database, enter SAMPLES. The name is not case-sensitive.

5. For Database directory, enter SAMPLES.

6. Click Next.

7. Accept all other values as default.

8. Click Finish.

This step finishes creating the database.

9. For Select an existing database for Routines, select the database that you just created.

Note that for a production system, you would use a different database to store routines and classes.

10. Accept all other values as default.

11. Click Save.

## 4 Completing README.md Steps

Now that you have downloaded the repo and created a namespace, complete the other setup steps in the README.md file that is included with the GitHub repo.
