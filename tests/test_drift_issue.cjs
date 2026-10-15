'use strict';
const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const crypto = require('node:crypto');
const publish = require('../.github/scripts/drift-issue.cjs');

async function run(changes, issues = [], alterBody) {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'ollama-drift-'));
  const digest = crypto.createHash('sha256').update(JSON.stringify(changes)).digest('hex');
  let body = `<!-- ollama-catalog-drift:v1 -->\n<!-- change-digest:${digest} -->\n# Report\n`;
  if (alterBody) body = alterBody(body);
  fs.writeFileSync(path.join(directory, 'drift.json'), JSON.stringify(changes));
  fs.writeFileSync(path.join(directory, 'drift.md'), body);
  const calls = [];
  const github = { paginate: async () => issues, rest: { issues: {
    listForRepo: () => {}, create: async x => calls.push(['create', x]),
    update: async x => calls.push(['update', x]),
  } } };
  try {
    await publish({ github, context: { repo: { owner: 'test', repo: 'test' } }, core: { info: () => {} }, directory });
    return { calls, body };
  } finally { fs.rmSync(directory, { recursive: true }); }
}
const issue = body => ({ number: 1, title: 'Ollama cloud catalog drift', body, user: { login: 'github-actions[bot]' } });
const clean = { added: [], removed: [] };
const drift = { added: ['new-model'], removed: [] };

test('clean listing creates no issue', async () => assert.deepEqual((await run(clean)).calls, []));
test('new drift creates one issue', async () => assert.equal((await run(drift)).calls[0][0], 'create'));
test('unchanged drift performs no writes', async () => {
  const { body } = await run(drift);
  assert.deepEqual((await run(drift, [issue(body)])).calls, []);
});
test('changed drift updates existing issue', async () => {
  const result = await run(drift, [issue('<!-- ollama-catalog-drift:v1 -->\nold')]);
  assert.equal(result.calls[0][0], 'update'); assert.equal(result.calls[0][1].issue_number, 1);
});
test('resolved drift closes existing monitor issue', async () => {
  const result = await run(clean, [issue('<!-- ollama-catalog-drift:v1 -->\nold')]);
  assert.equal(result.calls[0][1].state, 'closed');
});
test('user-authored marker cannot redirect bot updates', async () => {
  const other = { ...issue('<!-- ollama-catalog-drift:v1 -->\nold'), user: { login: 'someone' } };
  assert.equal((await run(drift, [other])).calls[0][0], 'create');
});
test('duplicate monitor issues fail without publishing another', async () => {
  const existing = issue('<!-- ollama-catalog-drift:v1 -->\nold');
  await assert.rejects(run(drift, [existing, { ...existing, number: 2 }]), /Multiple monitor issues/);
});
test('malformed report and injected model names fail', async () => {
  await assert.rejects(run({ added: ['evil`\n@all'], removed: [] }), /Invalid drift data/);
  await assert.rejects(run({ added: ['new-model\n'], removed: [] }), /Invalid drift data/);
  await assert.rejects(run({ added: ['a', 'a'], removed: [] }), /Invalid drift data/);
  await assert.rejects(run({ added: ['a'], removed: ['a'] }), /Invalid drift data/);
  await assert.rejects(run(drift, [], () => 'bad'), /Invalid or oversized/);
});
