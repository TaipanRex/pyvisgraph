## Contributing

Please take a moment to review this document in order to make the contribution 
process easy and effective for everyone involved.

## Using the issue tracker

The issue tracker is the preferred channel for bug reports, features requests 
and submitting pull requests.

### Bug reports

A bug is a demonstrable problem that is caused by the code in the repository. Good bug 
reports are extremely helpful - thank you!

A good bug report shouldn't leave others needing to chase you up for more information. 
Please try to be as detailed as possible in your report. What is your environment? What 
steps will reproduce the issue? What OS experience the problem? What would you expect 
to be the outcome? All these details will help people to fix any potential bugs.

Example:

> Short and descriptive example bug report title
>
> A summary of the issue and the OS environment in which it occurs. If suitable, include the steps required to reproduce the bug.
>
> This is the first step  
> This is the second step  
> Further steps, etc.  
> Any data, like the relevant `Point`s and so on  
>
> Any other information you want to share that is relevant to the issue being reported. This might include the lines of code that you have identified as causing the bug, and potential solutions (and your opinions on their merits).

Below is an actual (slightly modified) example submitted by @tjansson60:

> Floating point representation error in angle2()
>
> While processing the shoreline set GSHHS_c_L1 with 742 shapes a
> problem was encountered where cos_value = 1.00000000000048 which meant
> that the acos raised an ValueError: math domain error and the graph
> could not be built.
>
> Examples of values in angle2 when problem was first encountered:  
> point_a = (112.96, -25.49)  
> point_b = (45.00, -25.49)  
> point_c = (45.00, -25.49)  
> a = 6.938890000001394e-07  
> b = 4618.002849783456  
> c = 4618.11606498842  
> cos_value = 1.00000000000048  
>
> A possible solution is to check if the arguments are very close 
> to -1 or 1 and returns the expected values. If the values are not 
> close to either of these values the ValueError is still raised.

### Feature requests
Feature requests are welcome. But take a moment to find out whether your idea fits 
with the scope and aims of the project. It's up to you to make a strong case to convince 
the project's developers of the merits of this feature. Please provide as much detail 
and context as possible.

### Pull requests
Good pull requests - patches, improvements, new features - are a fantastic help. They 
should remain focused in scope and avoid containing unrelated commits.

Please ask first before embarking on any significant pull request (e.g. implementing 
features, refactoring code, porting to a different language), otherwise you risk spending 
a lot of time working on something that the project's developers might not want to merge 
into the project.

**IMPORTANT**: By submitting a patch, you agree to allow the project owner to license 
your work under the same license as that used by the project.

## Commit message rules
1. Separate subject from body with a blank line
2. Limit the subject line to 50 characters
3. Use the imperative mood in the subject line (i.e. `Fix bug xxx`, not `Fixed bug xxx`)
4. Use the body to explain *what* and *why* vs. *how*
5. Add references to GitHub issues/PRs at the bottom

Example commit message:

```
Summarize changes in around 50 characters or less

More detailed explanatory text, if necessary.In some contexts, the 
first line is treated as the subject of the commit and the rest of 
the text as the body. The blank line separating the summary from 
the body is critical (unless you omit the body entirely); various 
tools like `log`, `shortlog` and `rebase` can get confused if you
run the two together.

Explain the problem that this commit is solving. Focus on why you
are making this change as opposed to how (the code explains that).
Are there side effects or other unintuitive consequences of this
change? Here's the place to explain them.

Further paragraphs come after blank lines.

 - Bullet points are okay, too

 - Typically a hyphen or asterisk is used for the bullet, preceded
   by a single space, with blank lines in between

References to specific GitHub issues/PRs should be added like below.
When you then view the commit on GitHub, there will automatically
be links to the issues/PRs. Note that when using the 'Resolves' 
reference, GitHub will automatically close the referenced issue.

Resolves: #123
See also: #456, #789
```

In many cases a commit will not require both a subject and a body. Sometimes a single line is fine, especially 
when the change is so simple that no further context is necessary. For example:

```
Fix typo in README.MD
```

See: [How to Write a Git Commit Message](https://chris.beams.io/posts/git-commit/)

## Git branch naming conventions

Git branches should be named as follows: `<type>/<name>`

### type

```
bug    - Code changes linked to a known issue.
ft     - New feature.
```

### name

Always use dashes to seperate words, and keep it short.

### Examples

```
ft/progressbar
bug/angle2-floatingpoint
```

## Creating a Fork

Just head over to the [Pyvisgraph](https://github.com/TaipanRex/pyvisgraph) GitHub page 
and click the "Fork" button. Once you've done that, you need to clone the forked repo to your local machine:

```shell
git clone git@github.com:USERNAME/pyvisgraph.git
```

## Keeping Your Fork Up to Date

While this isn't an absolutely necessary step, if you plan on doing anything more than just a 
tiny quick fix, you'll want to make sure you keep your fork up to date by tracking the 
original "upstream" repo that you forked. To do this, you'll need to add a remote:

```shell
# Add 'upstream' repo to list of remotes
git remote add upstream https://github.com/TaipanRex/pyvisgraph.git

# Verify the new remote named 'upstream'
git remote -v
```

Whenever you want to update your fork with the latest upstream changes, you'll need to first 
fetch the upstream repo's branches and latest commits to bring them into your repository:

```shell
# Fetch from upstream remote
git fetch upstream

# View all branches, including those from upstream
git branch -va
```

Now, checkout your own master branch and merge the upstream repo's master branch:

```shell
# Checkout your master branch and merge upstream
git checkout master
git merge upstream/master
```

If there are no unique commits on the local master branch, git will simply perform a fast-forward. 
However, if you have been making changes on master (in the vast majority of cases you probably 
shouldn't be - [see the next section](#doing-your-work), you may have to deal with conflicts. 
When doing so, be careful to respect the changes made upstream.

Now, your local master branch is up-to-date with everything modified upstream.

## Doing Your Work

### Create a Branch

Whenever you begin work on a new feature or bugfix, it's important that you create a new branch. 
Not only is it proper git workflow, but it also keeps your changes organized and separated 
from the master branch so that you can easily submit and manage multiple pull requests for 
very task you complete.

To create a new branch and start working on it (note the [branch naming conventions](#git-branch-naming-conventions)):

```shell
# Checkout the master branch - you want your new branch to come from master
git checkout master

# Create a new branch named <type>/<name>, f.ex. ft/newfeature
git branch ft/newfeature

# Switch to your new branch
git checkout ft/newfeature
```

Now you can start making changes to the code.

## Submitting a Pull Request

### Cleaning Up Your Work

Prior to submitting your pull request, you might want to do a few things to clean up your 
branch and make it as simple as possible for the original repo's maintainer to test, 
accept, and merge your work.

If any commits have been made to the upstream master branch, you should rebase your 
development branch so that merging it will be a simple fast-forward that won't require 
any conflict resolution work.

```shell
# Fetch upstream master and merge with your repo's master branch
git fetch upstream
git checkout master
git merge upstream/master

# If there were any new commits, rebase your development branch
git checkout ft/newfeature
git rebase master
```

Now, it may be desirable to squash some of your smaller commits down into a small number 
of larger more cohesive commits. You can do this with an interactive rebase:

```shell
# Rebase all commits on your development branch
git checkout ft/newfeature
git rebase -i master
```

This will open up a text editor where you can specify which commits to squash.

### Submitting

Once you've committed and pushed all of your changes to GitHub, go to the page for your 
fork on GitHub, select your development branch, and click the pull request button. If 
you need to make any adjustments to your pull request, just push the updates to GitHub. 
Your pull request will automatically track the changes on your development branch and update.

## Accepting and merging a Pull Request

The following sections are written from the perspective of the repository owner who is 
handling an incoming pull request. Thus, where the "forker" was referring to the original 
repository as upstream, we're now looking at it as the owner of that original repository 
and the standard origin remote.

### Checking out a Pull Request locally

```shell
# Creates a local branch <BRANCHNAME>. <PR ID> is the Github PR number.
git fetch origin pull/<PR ID>/head:<BRANCHNAME>
```

If you want to push the branch to the repo:

```shell
git push origin <BRANCHNAME>
```

See: [Checking out pull requests locally](https://help.github.com/articles/checking-out-pull-requests-locally/)

### Automatically Merging a Pull Request

In cases where the merge would be a simple fast-forward, you can automatically do the merge by just clicking the 
button on the pull request page on GitHub.

### Manually Merging a Pull Request

The target branch must [pulled locally](#checking-out-a-pull-request-locally) first.

```shell
# Checkout the branch you're merging to in the target repo
git checkout master

# Merge the development branch
git merge ft/newfeature

# Push master with the new feature merged into it
git push origin master
```

### Cherry picking commits from a Pull Request

If you only want to merge certain commits from a Pull Request, use `cherry-pick`. Again make sure the
target branch is [pulled locally](#checking-out-a-pull-request-locally) first.

```shell
# Make sure you are on the branch you want to apply the commit to.
git checkout master
git cherry-pick <commit-hash>
```

See: [What does cherry picking a commit with git mean](https://stackoverflow.com/questions/9339429/what-does-cherry-picking-a-commit-with-git-mean)

### Deleting development branches

When you are done with a development branch, you're free to delete it. If it has been merged, all commit history and 
graphical log will be preserved.

```shell
git branch -d newfeature

# If you want to delete a remote branch (this will also close any Pull Request tied to it)
git push -d origin branchname
```

## Releasing a new version on PyPi

_Note: with the release of [pypi.org](www.pypi.org), below will become deprecated. [This](https://packaging.python.org/tutorials/packaging-projects/) explains how to update the workflow._

Make sure all changes have been commited, we will then make a release commit. Change `setup.py` 
in two places with the new version number: `version = 'x.x.x',` and `download_url = 'https://github.com/TaipanRex/pyvisgraph/tarball/x.x.x',`.

```shell
git add setup.py
git commit -m "push x.x.x"
# Write release notes in tag annotation. First line should be release number, x.x.x
git tag -a x.x.x
git push origin master
git push --tags origin master
sudo python setup.py sdist upload -r pypi
```

See: [How to submit a package to PyPI](http://peterdowns.com/posts/first-time-with-pypi.html)
