# Contributing

There are many areas we can use contributions - ranging from code, documentation, feature proposals, issue triage, samples, and content creation. 

First, please read the [code of conduct](https://github.com/fission/.github/blob/main/CODE_OF_CONDUCT.md). By participating, you're expected to uphold this code.

## Setup

1. Clone and setup
```sh
# Clone all submodules
git submodule update --init --recursive
# Install NPM dependencies
npm install
```
2. Run Hugo server
```
$ hugo server
Web Server is available at http://localhost:1313/ (bind address 127.0.0.1)
Press Ctrl+C to stop
```
You can visit [localhost:1313](http://localhost:1313/) in browser to preview website.

## Making changes

1. Create a new branch
2. Make your changes
3. Verify your changes locally with Hugo server
4. Commit and push your changes to the branch
5. Raise a PR to default branch, verify changes with Netlify preview URL
6. Once PR is merged, your changes would be live on the site
