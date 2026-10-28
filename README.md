# ecashcard.org

The parent site for [Cashu Card](https://cashucard.org) and [Fedimint Card](https://fedimintcard.org): static pages in `dist/`, served as Cloudflare Workers static assets (`wrangler.jsonc`).

- `dist/index.html` is the one page; `dist/privacy.html` the privacy policy; `dist/404.html` the not-found page.
- `dist/assets/site.css` holds every style. Figtree is bundled under `dist/assets/fonts/` (OFL).
- The two project marks under `dist/assets/` are copies from each project's site.

Preview without publishing: `npx wrangler versions upload` (its preview URL serves only that version). Publish: `npx wrangler deploy`, which serves ecashcard.org and www.
The workers.dev address belongs to the same Worker, so it always shows what ecashcard.org shows.
