# V4 content audit & release checklist

## Source inventory
- Existing public articles inventoried from repository tree: Linux, Docker, Kubernetes/Helm, DevOps/Ansible/CI-CD, Git, PostgreSQL, Microservices, Windows.
- Existing RU and EN PDF resumes are linked from V4; no PDF content is rewritten.
- Career timeline is based on CV_ParamonovD.html, which contains an outdated “present” label. Confirm dates and current role against the latest resume.
- Published profile describes 20+ years in IT and 9+ years in DevOps/SRE; confirm exact wording before production.
- LinkedIn URL and public contact email are inherited from the published profile.

## Release gates
- [ ] Owner verifies current role, dates, achievements, education and language level.
- [ ] Owner approves all case studies and confirms no confidential material.
- [ ] Run MLflow lab on Docker Desktop / Linux and verify commands against pinned images.
- [ ] Test every tool in current Chrome, Firefox and Safari; check mobile layout.
- [ ] Verify internal and external links, keyboard focus and screen-reader labels.
- [ ] Check contrast, reduced-motion behavior, browser console and network failures.
- [ ] Check external font/CDN fallback behavior and consider self-hosting dependencies.
- [ ] Reconcile SEO metadata, canonical URLs, structured data and sitemap only during an approved migration.
- [ ] Explicit approval required before changing production routes.
