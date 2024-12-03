
#### GIT - SHELVE LOCAL CHANGES:
In Git, you can shelve local changes to temporarily store them aside and switch to a different branch. 

This allows you to save your changes without committing them, and then later reapply them when you switch back to the original branch.

Here's how to shelve changes in Git:

1. Open the terminal and navigate to the root directory of the Git repository.
2. Run the following command to view the changes in your working tree:
```
git status
```

3. Shelve the changes using the following command:
```
git stash save "stash message"
```



The stash message is an optional description of the changes you are stashing. This can be useful for later reference when you want to reapply the changes.

Your changes will now be temporarily stored in the stash and your working tree will be clean. You can switch to a different branch, make changes, and then switch back to the original branch and reapply the stash.

To reapply the stash, run the following command:

```
git stash apply
```

Note: You can have multiple stashes in your repository. To see a list of stashes, use the following command:

```
git stash list
```

You can reapply a specific stash by using its stash ID, which is displayed in the list. To reapply a stash, run the following command:

```kotlin
git stash apply stash@{stash_id}
```

Replace `stash_id` with the ID of the stash you want to reapply.