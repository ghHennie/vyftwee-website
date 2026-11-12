# vyftwee-website

The vyftwee.co.za website: Vyf Twee, its ventures and company details.

- `site/` is what is published (Azure Static Web App, app location `/site`).
- Edit the values at the top of `build.py`, then run `python build.py`; it rewrites the pages in `site/`.
- Policy pages (`/terms`, `/privacy`, `/refunds`, `/cancellations`, `/delivery`) come from `content/policies/*.md`; the logo and icons are copied from `brand/`.
- CI does not run `build.py`: commit the generated files in `site/`.
