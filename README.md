# Fission Site Source Repo

This is the source for the [fission.io](https://fission.io)
website.

## Repo organization and building

This is a [hugo](https://gohugo.io) statically-generated site, hosted
on [netlify](https://netlify.com).  The site is automatically built by
netlify (see netlify.toml and build.sh).

 * `build.sh` is run by netlify. It runs hugo and places the generated
   site under `dist/public`

## Making changes

### Adding a new page

* You have to install **extended** version of Hugo in order to support SCSS/SASS.

```
$ cd docs/
$ npm install -D --save autoprefixer postcss-cli
$ hugo new how-to-use-ShinyNewThing.md
```

### Modifying an existing page

Find the doc under `content`, edit it, make a pull request.  You
can use GitHub's handy UI for editing pages.

## Previewing your changes

```
$ hugo serve -D
# This will output a link that you can open in a browser.
```

## Publishing your changes

When the pull request is merged the site will automatically be updated by netlify.
