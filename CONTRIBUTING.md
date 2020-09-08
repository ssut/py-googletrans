# Contributing to this library are always welcome and highly encouraged :)

This is a guide for you to get some ideas~

## Dependencies

To make sure that the following instructions work, please install the following dependencies
on you machine:

- coveralls==1.1

## Installation

To get the source of `py-googletrans`, clone the git repository via:

````
$ git clone https://github.com/ssut/py-googletrans
````
This will clone the complete source to your local machine.

## Issue Reporting

Feel free to report any issues that you come up with!
Please follow the steps before reporting. We love keeping everything in a good manner :p

### Step 1: Checking Previous Issues

There may be a lot of different issues related to different aspects.  
Here we list 12 main types:  

* [bug](https://github.com/ssut/py-googletrans/labels/bug)
* [compromised](https://github.com/ssut/py-googletrans/labels/compromised)
* [dependencies](https://github.com/ssut/py-googletrans/labels/dependencies)
* [duplicate](https://github.com/ssut/py-googletrans/labels/duplicate)
* [enhancement](https://github.com/ssut/py-googletrans/labels/enhancement)
* [help wanted](https://github.com/ssut/py-googletrans/labels/help%20wanted)
* [in progress](https://github.com/ssut/py-googletrans/labels/help%20wanted)
* [invalid](https://github.com/ssut/py-googletrans/labels/invalid)  

Please see [About labels](https://docs.github.com/en/github/managing-your-work-on-github/about-labels) for more information.  

Note there is no labels for closed issues but still remember to have a look!  

### Step 2: Formatting Your Comment

Please see the [Issue Template](ISSUE_TEMPLATE.md).

## Pull Request Submitting

> Inspired by [angular-translate](https://github.com/angular-translate/angular-translate/blob/master/CONTRIBUTING.md).  
- Check out a new branch based on <code>master</code> and name it to what you intend to do:
  - Example:
    ````
    $ git checkout -b BRANCH_NAME origin/master
    ````
    If you get an error, you may need to fetch master first by using
    ````
    $ git remote update && git fetch
    ````
  - Use one branch per fix/feature
- Make your changes
  - Make sure to provide a spec for unit tests.
  - Run the tests ``pytest``.
  - Add a test for your feature or bug fix.
  - When all tests pass, everything's fine. If your changes are not 100% covered, go back and 
    run the tests ``pytest`` again
- Commit your changes
  - Please provide a git message that explains what you've done.
  - Please make sure your commits follow the [conventions](https://www.conventionalcommits.org/en/v1.0.0/)
  - Commit to the forked repository.
- Make a pull request
  - Make sure you send the PR to the <code>master</code> branch.
  - Link the bug issue if there is one.
  - Travis CI is watching you!

If you follow these instructions, your PR will land pretty safely in the main repo!  
  