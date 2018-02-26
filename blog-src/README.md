# Fission blog

## Updating this blog

This is a hugo statically-generated site.

See here for instructions on [installing Hugo](https://gohugo.io/getting-started/installing/).

### Content 

cd to this directory, and create a new page with `hugo new
posts/something.md`.

Write your post in that new file. You can live preview with `hugo
serve -D` from the blog-src directory.

To publish:
 1. Set "draft" to "false" on top the new content file (or just delete
    the line that says "draft: true").
 2. Run `hugo` (no arguments) from this dir.
 3. `git add`, `git commit` and `git push` the new content. A few
    minutes after the git push, the new content will show up at
    [fission.io/blog](http://fission.io/blog).

### Styling, appearance, navigation etc.

Blog title, social links, etc. are in config.toml.

Styling is under themes/.  So is the site header and footer, where you
can add meta tags or Google Analytics stuff.

The CSS framework used is tachyons.io; if you're changing the styling
of the blog, there is probably a tachyons class already for what
you're trying to do.

Changes to styling are pushed the same say way as changes to content
(run `hugo`; `git add`; `git commit`; `git push`).
