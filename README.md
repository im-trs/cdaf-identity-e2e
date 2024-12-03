# cdaf-lovehoney

## TODO:
Document the git flow strategy:
- feature/...
- test/...
- fix/...
- pull requests
- merge strategy after reviews
- git stash && git checkout master && git fetch && git pull && git stash pop

## Notes on installation on Mac

**Prerequisites**

pip
> *	python -m pip install --upgrade pip 

brew
> *   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
> *   echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> /Users/user/.zprofile
> *   eval "$(/opt/homebrew/bin/brew shellenv)"


Chromedriver
> *	brew install --cask chromedriver
> *	xattr -d com.apple.quarantine /opt/homebrew/bin/chromedriver



#  
### CDAF-Framework
> *	git clone https://imannella2022@bitbucket.org/imannella2022/cdaf-lovehoney.git 
> *	cd cdaf-lovehoney	
> *	python3 -m venv venv  *OR*  python.exe -m venv venv 
> *	source venv/bin/activate *OR* .\venv\Scripts\Activate.ps1
> *	pip install -r requirements.txt

#  
```	
Guide:

$ python3.10 -m venv venv

$ source venv/bin/activate

	• Install python 3.10.6 as minimum
	
	• Create a new venv folder (if python3.10 using for Python 3.10)
$ python3.10 -m venv venv
	• Activate venv
$ source venv/bin/activate
	• Install saved dependencies
$ pip install -r requirements.txt
	• Re-open PyCharm and change the interpreter if needed
```
	
#
### PyCharm - Debug Features
		Right click on 'features'
		> debug features
		Test execution starts


#
### Python Libraries
	TestRail: https://github.com/travispavek/testrail-python


# ------------------------- 
# Development notes
```
1. Create new Page objects see `class EmptyPageObject` of `empty.py`

2. Add its mapping into the `mapping.py` array `PAGE_OBJECTS` to link its name to the actual class 
    eg: 'empty': EmptyPageObject,

3. If the page has its own URL configure it on the properties.cfg:
    [confused]
    url: https://confused.com/
    title: Confused.com
```


# ------------------------- 
# Test Automation Training

*   The objective of this repository is to provide a skills development and training guideline specifically to 
    support Kinetic Skunk's test automation strategy.
*   We adopt a first principles approach to developing skills required become experts in Agile - DevOps Automated Testing.
*   This repository is setup based on the first principles approach.

## Instructions
1.  Using the 'CONTRIBUTING.md' file to document contributions. Use markdown language when documenting contributions.
    
    1.1 [Markdown Cheat Sheet](https://www.markdownguide.org/cheat-sheet/)
    
    1.2 [Markdown Syntax](https://guides.github.com/pdfs/markdown-cheatsheet-online.pdf)
    
    1.3 [Another Markdown Cheat Sheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)
    
2.  Complete the tutorials in numerical order
3.  Setup your test automation virtual machine

## Tutorials

Do these tutorials in numerical order. By doing so you'll get a solid understanding of:
* Python for Automated testing
* Git
* Git-Flow
* Selenium
* Toolium
* Page Object Model
* Running automated tests in Docker

### Learn Python Programming and Package Management
1.  Go to Kinetic Skunk's [Python Training channel](https://teams.microsoft.com/l/channel/19%3Aba801583608d42e0941609f3f19986ab%40thread.tacv2/tab%3A%3A875b0a53-c1a3-49e7-898e-78e3a2349cfc?groupId=ab961109-2947-40cf-be7d-4fdae92da4ee&tenantId=d4a39087-ec22-44f5-9bb7-68b71271c26a)
2.  Choose one of the Python Programming Books to work through.
```text
Note that you do not have to be an advanced Python Programmer to be good at Automated Testing or to progress through this training guide.
However if you want to become a great Test Engineer then become great at least at one programming language.
Kinetic Skunk recommends Python.
```
3.  We use [Pipenv](https://realpython.com/pipenv-guide/) to manage Python Virtual Environments.

3.1 Go through [Hitchhikers guide to Pipenv and Virtual Environments](https://docs.python-guide.org/dev/virtualenvs/)
    Each Test Automation project will have it's own virtual Python Environment.

## Git and Git-flow
```text
We treat our Test Automation Code as if it's production code.
As such we implement a Git-Flow branching strategy.
This ensures that we always have a set of executable automated tests in a master branch.
```
1. Complete the [git](https://www.atlassian.com/git/tutorials) tutorial
1. Learn [gitflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)

### Behave Driven Testing
```text
BDT is our preferred test design methodology.
We implement BDT for UI, API, Load, Penetration and Infrastructure Testing.
```
1. Go through [Behave](https://jenisys.github.io/behave.example)

### Selenium
```text
It is of paramount importance to have a deep understanding of Selenium.
The resources in this section will provide you with that understanding.
```
1.  [Python Bindings](https://selenium-python.readthedocs.io/installation.html)
2.  [Expected Conditions](https://www.selenium.dev/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.expected_conditions.html)
3.  [Action Chains](https://www.selenium.dev/selenium/docs/api/py/webdriver/selenium.webdriver.common.action_chains.html)
4.  [More Action Chains](http://allselenium.info/python-selenium-all-mouse-actions-using-actionchains)
5.  [Desired Capabilities](https://github.com/SeleniumHQ/selenium/wiki/DesiredCapabilities)

### Page Object Model
```text
POM has become the standard Test Automation Design Methodology.
It is practical and easy to understand. However it doesn't mean that we shouldn't innovate novel approaches.
```
1.  [Develop Page Object Selenium Tests Using Python](https://blog.testproject.io/2019/07/16/develop-page-object-selenium-tests-using-python)
2.  [Implementing the Page Object Model](https://qxf2.com/blog/page-object-model-selenium/)
3.  [selenium-page-factory](https://pypi.org/project/selenium-page-factory)
4.  [Selenium-page-factory Code](https://github.com/NayakwadiS/selenium-page-factory)

### Toolium
```text
Toolium is Python implementation of POM and a wrapper around Selenium and Appium.
It is central to the implementation of Kinetic Skunk's Agile-DevOps Test Strategy.
```
1.  [Template](https://github.com/Telefonica/toolium-template)
2.  [Examples](https://github.com/Telefonica/toolium-examples)
3.  [Toolium](https://github.com/Telefonica/toolium)
4.  [Documentation](https://toolium.readthedocs.io/en/latest/browser_configuration.html)
5.  [Toolium PDF](https://toolium.readthedocs.io/_/downloads/en/latest/pdf)

## Setup Test Automation Virtual Machine
```text
In this section you will setup your Test Automation Virtual Machine and your test automation repository.
You will learn how to run your automated tests in docker and how to debug your tests using the docker debug containers.
```
1.  [Install VirtualBox](https://www.nakivo.com/blog/how-to-update-virtualbox/)

2.  [Install the Ubuntu 20.04 LTS in VirtualBox](https://www.wikihow.com/Install-Ubuntu-on-VirtualBox)
    2.1 Download Ubuntu 20.04 LTS [here](https://ubuntu.com/download/desktop)
    ```text
    Ubuntu 20.04 LTS comes with a refreshed state-of-the-art toolchain including new upstream releases of glibc 2.31, 
    OpenJDK 11, rustc 1.41, GCC 9.3, Python 3.8.2, ruby 2.7.0, php 7.4, perl 5.30 and golang 1.13.
    ```
    
3.  In your Ubuntu VM:

    3.1 Install [Pipenv](https://realpython.com/pipenv-guide/)
    
    3.2 [Fork](https://docs.gitlab.com/ee/user/project/repository/forking_workflow.html#creating-a-fork) this [repository](https://gitlab.com/kineticskunk/skills-development/automated-testing/web-user-interface-testing.git) 
    
    3.3 Implement [gitflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
    
    3.4 Commit and push your changes
    
    3.4 Install [Docker](https://docs.docker.com/engine/install/ubuntu/)
    
## Running Automated Tests in Docker Containers

## Run Tests in Docker Containers
### Docker Chrome
```shell script
docker run -v $(pwd):/opt/toolium -it kineticskunk/standalone-chrome-toolium:0.0.1 bash
```
### Docker Firefox
```shell script
docker run -v $(pwd):/opt/toolium -it kineticskunk/standalone-firefox-toolium:0.0.1 bash
```
### Docker Opera
```shell script
docker run -v $(pwd):/opt/toolium -it kineticskunk/standalone-opera-toolium:0.0.1 bash
```
### Debug Container

You can acquire the port that the VNC server is exposed to by running:
(Assuming that we mapped the ports like this: 49338:5900)
```shell script
$ docker port <container-name|container-id> 5900
#=> 0.0.0.0:49338
```

In case you have [RealVNC](https://www.realvnc.com/) binary `vnc` in your path, you can always take a look, 
view only to avoid messing around your tests with an unintended mouse click or keyboard interrupt:
```shell script
$ ./bin/vncview 127.0.0.1:49338
```

If you are running Boot2Docker on Mac then you already have a [VNC client](http://www.davidtheexpert.com/post.php?id=5)
built-in. You can connect by entering `vnc://<boot2docker-ip>:49160` in Safari or [Alfred](http://www.alfredapp.com/)

When you are prompted for the password it is __secret__.
If you wish to change this you can define a docker image that derives from the posted ones which reconfigures it:

```dockerfile
FROM registry.gitlab.com/kineticskunk.io/infrastructure/kineticskunk-selenium/toolium-chrome-debug:3.141.59

RUN x11vnc -storepasswd <your-password-here> /home/seluser/.vnc/passwd
```

```shell script
docker run -d -p 4444:4444 -p 5900:5900 -v $(pwd):/opt/toolium --name chrome-debug \
registry.gitlab.com/kineticskunk.io/infrastructure/kineticskunk-selenium/toolium-chrome-debug:3.141.59
docker port chrome-debug 5900
```

## Practice Sites
* [dummy-automation-websites](https://ultimateqa.com/dummy-automation-websites/)






