### Quick Commands

[Here's a tool to help with visualizing git structure.](https://git-school.github.io/visualizing-git/#free-remote)  
[Here's a good tutorial to learn git.](https://cs50.harvard.edu/web/2020/weeks/1/)
1. Clone this repository, go to the `develop` branch and work there.
```
git clone https://github.com/smuktevi/recipeat.git
git checkout develop
```
Make sure you set your remote repository to `origin develop`. [check here for help](https://devconnected.com/how-to-set-upstream-branch-on-git/)  
`git push -u <remote> <branch>`  
  
2. After making your changes execute:  
```
git pull                                                                      #pull from remote repository, check for confilcts
git add .                                                                     #which adds your files that you made changes in.
git commit -m "type a meaningful message here about your changes"             #commit your changes
git status                                                                    #check if any files are staged still 
git push origin develop
```
