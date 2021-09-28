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

1. Create a new branch
2. Make your changes
3. Install npm dependencies `npm install`
4. Run hugo server `hugo server`
5. Verify your changes locally with server
6. Commit and push your changes to the branch
7. Once you verify changes with Netlify preview URL, raise a PR to default branch
8. Once PR is merged, push to master your changes would be live on the site
