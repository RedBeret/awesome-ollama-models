'use strict';

const fs = require('node:fs');
const crypto = require('node:crypto');
const MARKER = '<!-- ollama-catalog-drift:v1 -->';
const TITLE = 'Ollama cloud catalog drift';

// Called only after a successful poll in the trusted scheduled/manual workflow.
module.exports = async function publish({ github, context, core, directory = 'reports' }) {
  const changes = JSON.parse(fs.readFileSync(`${directory}/drift.json`, 'utf8'));
  const body = fs.readFileSync(`${directory}/drift.md`, 'utf8');
  const tag = /^[a-z0-9][a-z0-9._-]*(?::[a-z0-9][a-z0-9._-]*)?$/;
  if (!changes || Object.keys(changes).sort().join(',') !== 'added,removed' ||
      !['added', 'removed'].every(k => Array.isArray(changes[k]) && changes[k].length <= 1000 &&
        changes[k].every(v => typeof v === 'string' && v.length <= 128 && !/\s/.test(v) && tag.test(v)) &&
        new Set(changes[k]).size === changes[k].length) ||
      changes.added.some(v => changes.removed.includes(v))) {
    throw new Error('Invalid drift data; no issue changes made');
  }
  const digest = crypto.createHash('sha256').update(JSON.stringify({ added: changes.added, removed: changes.removed })).digest('hex');
  const digestMarker = `<!-- change-digest:${digest} -->`;
  if (!body.startsWith(MARKER + '\n' + digestMarker + '\n') || Buffer.byteLength(body, 'utf8') > 60000) {
    throw new Error('Invalid or oversized drift report; no issue changes made');
  }
  const issues = await github.paginate(github.rest.issues.listForRepo, {
    ...context.repo, state: 'open', per_page: 100,
  });
  const matches = issues.filter(i => !i.pull_request && i.title === TITLE &&
    i.user?.login === 'github-actions[bot]' && i.body?.startsWith(MARKER + '\n'));
  if (matches.length > 1) throw new Error('Multiple monitor issues found; consolidate them manually');
  const issue = matches[0];
  const drift = changes.added.length + changes.removed.length > 0;
  if (!drift) {
    if (issue) {
      await github.rest.issues.update({ ...context.repo, issue_number: issue.number, state: 'closed', state_reason: 'completed' });
      core.info('Resolved catalog drift; closed the monitor issue');
    } else core.info('No catalog drift; no issue created');
    return;
  }
  if (!issue) {
    await github.rest.issues.create({ ...context.repo, title: TITLE, body });
    core.info('Created catalog drift issue');
  } else if (!issue.body.includes(digestMarker)) {
    await github.rest.issues.update({ ...context.repo, issue_number: issue.number, body });
    core.info('Updated catalog drift issue');
  } else core.info('Drift unchanged; no notification or issue update');
};
