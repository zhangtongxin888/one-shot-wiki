# one-shot.wiki build

Static site served by GitHub Pages from the repo root (`main`, `/`).
Edit page bodies in `_build/pages/<key>.html` and metadata/lastmod in `_build/registry.py`,
then run `npm run check` (build → lint → SEO audit → HTTP test). Commit the generated HTML.

- Only the homepage title/H1 may contain "One Shot Wiki".
- A code may be listed as working only with 3+ named sources (`data-source-count`).
- Change `lastmod` only when the visible answer changes.
