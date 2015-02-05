wksp
====

A simple workspace manager for OS X.

About
====

wksp allows you to open Terminal tabs, set their color, and run arbitrary bash commands in each to bootstrap a workspace from the command line. The workspace is configured with a simple JSON format.

Setup
=====

The `.bash_profile` file contains a bash function to place in your own bash profile. You will need to fill in both the path to the `wksp.py` script in this repo and the path to a directory containing your workspace definitions. Workspace definitions are JSON files described below.

Usage
=====

To launch the workspace defined in `example_project.json` in your workspaces directory, simply run

```
wksp example_project
```

Defining a workspace
====================

The `project.json` file outlines the basic schema for a workspace definition. Arbitrary bash commands can be run either with or without a corresponding Terminal tab, defined in the "headless" and "headed" sections respectively.

The following project config headlessly launches a saved Sublime Text workspace and opens a Terminal window with a specified color and 3 tabs. In each tab it navigates to a desired directory. In the second tab it sets up port forwarding and in the third tab it pulls the repo and launches a development server.

```
{
	"headless": {
		"commands": [
			["subl", "/Users/clayton/code/workspaces/hermes.sublime-workspace"]
		]
	},
	"headed": {
		"tabs": [
			{
				"commands": [
					["cd", "/Users/clayton/code/hermes"]
				]
			},
			{
				"commands": [
					["cd", "/Users/clayton/code/hermes"],
					["authbind", "nginx", "-s", "stop"],
					["authbind", "nginx"]
				]
			},
			{
				"commands": [
					["cd", "/Users/clayton/code/hermes"],
					["git", "pull", "--rebase"],
					["authbind", "npm", "start"]
				]
			}
		],
		"color": "#003839"
	}
}
```

