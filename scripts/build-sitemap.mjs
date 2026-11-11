#!/usr/bin/env node
/**
 * Builds sitemap.xml from the site structure, using the last git commit date
 * of every page as <lastmod> (falls back to today when history is unavailable).
 *
 * Usage: node scripts/build-sitemap.mjs
 */

import { readdirSync, writeFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const BASE = 'https://topdevops.pro';
const TODAY = new Date().toISOString().slice(0, 10);
const NOTE_DIRS = ['microservices', 'docker', 'k8s', 'linux', 'windows', 'git', 'postgresql', 'devops'];

function lastCommit(path) {
  try {
    const out = execFileSync('git', ['log', '-1', '--format=%cs', '--', path], {
      cwd: ROOT,
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'ignore'],
    }).trim();
    return /^\d{4}-\d{2}-\d{2}$/.test(out) ? out : TODAY;
  } catch {
    return TODAY;
  }
}

const pages = [
  { file: 'index.html', url: '/', changefreq: 'weekly', priority: '1.0' },
  { file: 'CV_ParamonovD.html', url: '/CV_ParamonovD.html', changefreq: 'monthly', priority: '0.7' },
  { file: 'resume_slides_en.html', url: '/resume_slides_en.html', changefreq: 'monthly', priority: '0.6' },
];

for (const dir of NOTE_DIRS) {
  for (const name of readdirSync(resolve(ROOT, dir)).sort()) {
    if (!name.endsWith('.html')) continue;
    pages.push({
      file: `${dir}/${name}`,
      url: `/${dir}/${name}`,
      changefreq: 'monthly',
      priority: '0.8',
    });
  }
}

const entries = pages.map((page) => ({
  loc: BASE + page.url,
  lastmod: lastCommit(page.file),
  changefreq: page.changefreq,
  priority: page.priority,
}));

entries.sort((a, b) => (a.loc === BASE + '/' ? -1 : b.loc === BASE + '/' ? 1 : a.loc.localeCompare(b.loc)));

const xml =
  '<?xml version="1.0" encoding="UTF-8"?>\n' +
  '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
  entries.map((e) => `  <url>\n    <loc>${e.loc}</loc>\n    <lastmod>${e.lastmod}</lastmod>\n    <changefreq>${e.changefreq}</changefreq>\n    <priority>${e.priority}</priority>\n  </url>`).join('\n') +
  '\n</urlset>\n';

writeFileSync(resolve(ROOT, 'sitemap.xml'), xml, 'utf8');
console.log(`sitemap.xml: ${entries.length} urls`);
