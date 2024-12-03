### Guidelines for the default branching strategy in Git:

The default branching strategy using Git is a simple and straightforward way to manage your code. It consists of these main branches:

* **master** - Master is the main branch and is the default branch. It contains the latest, stable version of your code.
* **feature** - Feature branches are used to develop new features. They are created from the master branch and are merged back into the master branch when they are complete. When you are developing a new feature, you should create a new branch for the feature. This will allow you to isolate the changes that you are making to the feature and make it easier to test the feature.
* **release** - Release branches are created to prepare for a new release. They are created from the master branch and contain all the changes that will be included in the release. Once the release is complete, the release branch is merged back into the master branch and deleted. When you are making changes to the test automation framework, you should create a new branch for the changes. This will allow you to isolate the changes that you are making to the test automation framework and make it easier to test the test automation framework.
* **fix** - Fix branches are created to fix critical bugs on the framework. They are created from the master branch and contain only the changes that are necessary to fix the bug. Once a fix branch is complete, it should be merged back into the main master branch. When you are fixing a bug, you should create a new branch for the bug fix. This will allow you to isolate the changes that you are making to the bug fix and make it easier to test the bug fix.

In addition to these main branches, you may also want or need to create other branches for things like hotfixes, testing, and documentation. We can discuss from time to time

Here are some guidelines for using the default branching strategy:

* **Always work on feature branches.** Never work on the master branch directly. This will help to keep the master branch clean and stable.
* **Use pull requests to merge changes into the master branch.** This will help to ensure that changes are reviewed and tested before they are merged into the master branch.
* **Delete feature branches when they are merged into the master branch.** This will help to keep your repository clean and organized.

Another Example. 

When you are migrating to a new version of a library or framework. You can create a new migration branch to migrate the code to the new version in isolation. This will help to prevent the migration from breaking existing code.


### Here are some additional guidelines for using the default branching strategy in Git:

* **Give your feature branches descriptive names.** This will help you and other developers to easily identify what each branch is for.
* **Commit frequently.** This will help you to track your progress and make it easier to roll back changes if necessary.
* **Use pull requests to review and test your code before it is merged into the `master` branch.** This will help to catch any potential problems before they are released to production.
* **Delete feature branches once they have been merged into the `master` branch.** This will help to keep the `master` branch clean and organized.

Using a branching strategy is a simple and effective way to manage code changes. It is a good choice for teams of all sizes and can be used with any type of project.


### Suggested Git conflict solution

* `git checkout master `
* `git fetch `
* `git pull` 
* `git checkout <branch name>`
* `git merge master`
* resolve conflict on local and `git commit -m 'message'`
* `git push`


### Git Stash
The git stash command is a powerful tool that allows you to save your current working directory and index in a temporary location, so that you can switch branches or do other work without losing your changes. Once you're done, you can reapply the stash to bring your working directory back to the state it was in when you created the stash.

Here are some of the main git stash commands:

* `git stash`: This creates a new stash and saves your current working directory and index.
* `git stash apply`: This applies the most recent stash to your working directory.
* `git stash pop`: This applies the most recent stash to your working directory and then removes it from the stash list.
* `git stash list`: This lists all the available stashes.
* `git stash drop`: This removes a specific stash from the stash list.
* `git stash show`: This shows the contents of a specific stash.
* `git stash clear`: This removes all the stashes from the stash list.

***Example Scenario***

Here is an example of how to use the git stash command:

* You are working on a feature branch, and you have made some changes to the code.
* You want to switch to the main `master` branch to fix a bug.
* You don't want to lose the changes you have made to the feature branch.

To save your changes to the feature branch, you can use the `git stash` command. For example:

```
git stash -m 'my comment'
```

This will create a new stash and save your current working directory and index. The `-m` option allows you to specify a comment for the stash.

Once you have saved your changes, you can switch to the main branch. For example:

```
git checkout master
```

Now you can fix the bug. Once you are done, you can reapply the stash to your working directory. For example:

```
git stash pop
```

This will apply the most recent stash to your working directory and then remove it from the stash list.

If you want to keep the stash, you can use the `git stash apply` command instead of the `git stash pop` command. The `git stash apply` command will apply the most recent stash to your working directory, but it will not remove it from the stash list.

You can also use the `git stash list` command to see a list of all the available stashes. For example:

```
git stash list
```

This will output a list of all the available stashes, including the name of the stash, the date and time it was created, and the comment that was associated with it.

You can use the `git stash drop` command to remove a specific stash from the list. For example:

```
git stash drop stash@{0}
```

This will remove the most recent stash from the list. You can also use the `git stash clear` command to remove all the stashes from the list.

