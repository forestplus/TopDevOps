#!/usr/bin/env node
/**
 * Sync public GitHub data for the TopDevOps personal page.
 *
 * Reads the public profile + repositories of a GitHub account and writes a
 * single static snapshot (data/github-projects.json) that the site renders
 * without any runtime API calls, rate limits or client secrets.
 *
 * Usage:
 *   node scripts/sync-github-projects.mjs
 *   GITHUB_OWNER=forestplus GITHUB_TOKEN=ghp_xxx node scripts/sync-github-projects.mjs
 *
 * Environment:
 *   GITHUB_OWNER  account to sync (default: forestplus)
 *   GITHUB_TOKEN  optional token; raises the rate limit and is never written
 *                 to the output file. In GitHub Actions the built-in
 *                 GITHUB_TOKEN is enough for public data.
 *
 * Exit codes: 0 = snapshot written, 1 = fatal error.
 */

import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const OWNER = (process.env.GITHUB_OWNER || 'forestplus').trim();
const TOKEN = (process.env.GITHUB_TOKEN || '').trim();
const API = 'https://api.github.com';
const API_VERSION = '2022-11-28';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const OUT_FILE = resolve(ROOT, 'data', 'github-projects.json');

/**
 * Repositories whose GitHub Pages site does not live on the default
 * <owner>.github.io/<repo>/ URL (custom domain, CNAME in the repo, etc.).
 */
const PAGES_OVERRIDES = {
  TopDevOps: 'https://topdevops.pro/',
};

const HEADERS = {
  accept: 'application/vnd.github+json',
  'user-agent': 'topdevops-projects-sync',
  'x-github-api-version': API_VERSION,
};
if (TOKEN) HEADERS.authorization = `Bearer ${TOKEN}`;

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function api(path, attempt = 1) {
  const url = path.startsWith('http') ? path : `${API}${path}`;
  let res;
  try {
    res = await fetch(url, { headers: HEADERS });
  } catch (err) {
    if (attempt < 4) {
      await sleep(attempt * 1500);
      return api(path, attempt + 1);
    }
    throw new Error(`Network error for ${url}: ${err.message}`);
  }

  if (res.status === 403 || res.status === 429) {
    const remaining = res.headers.get('x-ratelimit-remaining');
    const reset = Number(res.headers.get('x-ratelimit-reset') || 0) * 1000;
    const retryAfter = Number(res.headers.get('retry-after') || 0) * 1000;
    const waitMs = Math.max(retryAfter, reset - Date.now(), 0);
    if (attempt < 3 && (remaining === '0' || retryAfter || waitMs > 0)) {
      const wait = Math.min(Math.max(waitMs, 2000), 20000);
      console.warn(`Rate limited on ${url}, retrying in ${Math.round(wait / 1000)}s...`);
      await sleep(wait);
      return api(path, attempt + 1);
    }
    throw new Error(
      `GitHub API rate limit hit for ${url}. ` +
        'Set GITHUB_TOKEN to raise the limit to 5000 requests/hour.',
    );
  }

  if (res.status === 404) {
    const err = new Error(`Not found: ${url}`);
    err.status = 404;
    throw err;
  }

  if (!res.ok) {
    const body = await res.text().catch(() => '');
    throw new Error(`GitHub API ${res.status} for ${url}: ${body.slice(0, 300)}`);
  }

  return res.json();
}

async function fetchAllRepos() {
  const repos = [];
  for (let page = 1; page <= 10; page += 1) {
    const batch = await api(
      `/users/${encodeURIComponent(OWNER)}/repos?per_page=100&page=${page}&sort=pushed&type=owner`,
    );
    if (!Array.isArray(batch) || batch.length === 0) break;
    repos.push(...batch);
    if (batch.length < 100) break;
  }
  return repos;
}

function pagesUrl(repo) {
  if (!repo.has_pages) return null;
  if (PAGES_OVERRIDES[repo.name]) return PAGES_OVERRIDES[repo.name];
  if (repo.name.toLowerCase() === `${OWNER.toLowerCase()}.github.io`) {
    return `https://${OWNER}.github.io/`;
  }
  return `https://${OWNER}.github.io/${repo.name}/`;
}

function normalizeRepo(repo) {
  const topics = Array.isArray(repo.topics) ? repo.topics.filter(Boolean) : [];
  return {
    name: repo.name,
    full_name: repo.full_name,
    html_url: repo.html_url,
    description: repo.description ? repo.description.trim() : null,
    homepage: repo.homepage ? repo.homepage.trim() : null,
    language: repo.language || null,
    topics,
    stars: repo.stargazers_count || 0,
    forks: repo.forks_count || 0,
    open_issues: repo.open_issues_count || 0,
    size_kb: repo.size || 0,
    has_pages: Boolean(repo.has_pages),
    pages_url: pagesUrl(repo),
    fork: Boolean(repo.fork),
    archived: Boolean(repo.archived),
    license: repo.license ? repo.license.spdx_id || null : null,
    created_at: repo.created_at || null,
    updated_at: repo.updated_at || null,
    pushed_at: repo.pushed_at || null,
    default_branch: repo.default_branch || 'main',
  };
}

function compareRepos(a, b) {
  if (a.fork !== b.fork) return a.fork ? 1 : -1;
  if (b.stars !== a.stars) return b.stars - a.stars;
  const at = new Date(a.pushed_at || 0).getTime();
  const bt = new Date(b.pushed_at || 0).getTime();
  if (bt !== at) return bt - at;
  return a.name.localeCompare(b.name);
}

function buildStats(repos) {
  const languageCounts = new Map();
  for (const repo of repos) {
    if (!repo.language) continue;
    languageCounts.set(repo.language, (languageCounts.get(repo.language) || 0) + 1);
  }

  const languages = [...languageCounts.entries()]
    .map(([name, count]) => ({ name, count }))
    .sort((a, b) => b.count - a.count || a.name.localeCompare(b.name));

  const pushedTimes = repos
    .map((r) => new Date(r.pushed_at || 0).getTime())
    .filter((t) => Number.isFinite(t) && t > 0);

  const latest = repos
    .filter((r) => r.pushed_at)
    .sort((a, b) => new Date(b.pushed_at) - new Date(a.pushed_at))[0];

  return {
    repos: repos.length,
    source_repos: repos.filter((r) => !r.fork).length,
    forks: repos.filter((r) => r.fork).length,
    stars: repos.reduce((sum, r) => sum + r.stars, 0),
    forks_count: repos.reduce((sum, r) => sum + r.forks, 0),
    languages,
    primary_language: languages.length ? languages[0].name : null,
    last_push_at: pushedTimes.length ? new Date(Math.max(...pushedTimes)).toISOString() : null,
    latest_repo: latest ? latest.name : null,
  };
}

async function main() {
  console.log(`Syncing public GitHub data for "${OWNER}"...`);

  const [profile, rawRepos] = await Promise.all([
    api(`/users/${encodeURIComponent(OWNER)}`),
    fetchAllRepos(),
  ]);

  const repos = rawRepos.map(normalizeRepo).sort(compareRepos);
  const stats = buildStats(repos);

  const payload = {
    owner: OWNER,
    generated_at: new Date().toISOString(),
    profile: {
      login: profile.login,
      name: profile.name || null,
      avatar_url: profile.avatar_url,
      html_url: profile.html_url,
      bio: profile.bio || null,
      company: profile.company || null,
      location: profile.location || null,
      blog: profile.blog || null,
      public_repos: profile.public_repos || 0,
      followers: profile.followers || 0,
      following: profile.following || 0,
      created_at: profile.created_at || null,
    },
    stats,
    repos,
  };

  const rel = OUT_FILE.slice(ROOT.length + 1).replace(/\\/g, '/');

  // Keep the committed snapshot byte-stable when nothing actually changed, so the
  // scheduled workflow does not create one empty commit per day.
  const previous = await readFile(OUT_FILE, 'utf8').catch(() => null);
  if (previous) {
    try {
      const prev = JSON.parse(previous);
      const strip = (data) => {
        const copy = JSON.parse(JSON.stringify(data));
        delete copy.generated_at;
        return JSON.stringify(copy);
      };
      if (strip(prev) === strip(payload)) {
        console.log(`No changes for ${rel} (data is up to date).`);
        return;
      }
    } catch {
      // Corrupted or unreadable previous snapshot: overwrite it.
    }
  }

  await mkdir(dirname(OUT_FILE), { recursive: true });
  await writeFile(OUT_FILE, `${JSON.stringify(payload, null, 2)}\n`, 'utf8');

  console.log(
    `Wrote ${rel}: ${stats.repos} repos, ${stats.stars} stars, ` +
      `${stats.languages.length} languages (auth: ${TOKEN ? 'token' : 'anonymous'}).`,
  );
}

main().catch((err) => {
  console.error(`sync-github-projects failed: ${err.message}`);
  process.exitCode = 1;
});
