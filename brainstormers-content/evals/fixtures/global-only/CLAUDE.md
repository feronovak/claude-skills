# freight-blog

Static site for the company blog. Astro 5 + Tailwind, deploys to Netlify on push
to `main`.

## Layout

- `src/content/posts/` — one MDX file per post, frontmatter `title`, `date`, `tags`
- `src/layouts/` — `Base.astro` wraps everything; `Post.astro` adds the article header
- `public/` — static assets, served from the root

## Commands

```
npm run dev       # localhost:4321
npm run build     # outputs to dist/
npm run preview   # serve dist/ locally
```

## Conventions

- Posts are drafts until `draft: false` — the build skips drafts
- Images go in `src/assets/`, referenced relatively so Astro can optimise them
- Tags are lowercase, hyphenated, and reused rather than invented per post
