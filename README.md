# Fission Site Source Repo

This is the source for the [fission.io](https://fission.io)
website.

## Repo organization

This is a [hugo](https://gohugo.io) statically-generated site, hosted
on [netlify](https://netlify.com).  The site is automatically built by
netlify (see netlify.toml and build.sh).

All site content is stored in the `content` directory in markdown format.

```text
content/en
├── _index.html  # Landing page
├── author       # Info about blog authors
├── blog         # Blog posts
├── docs         # Documentation pages
└── search.md
```

## Contributing

### Setup

1. Clone and setup

    ```sh
    # Install NPM dependencies
    npm install
    ```

2. Run Hugo server

    ```sh
    $ hugo server
    Web Server is available at http://localhost:1313/ (bind address 127.0.0.1)
    Press Ctrl+C to stop
    ```

You can visit [localhost:1313](http://localhost:1313/) in browser to preview website.

### Making changes

1. Create a new branch
2. Make your changes
3. Verify your changes locally with Hugo server
4. Commit and push your changes to the branch
5. Raise a PR to default branch, verify changes with Netlify preview URL
6. Once PR is merged, your changes would be live on the site
