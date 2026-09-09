'use strict';

// Offline configuration contracts: preserved resource coverage, valid policy
// references, and CLI output. These tests do not emulate Quantumult X routing.

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const { SERVICES, PRESETS, renderConfig, PARSER_URL } = require('../scripts/config-builder.js');
const ROOT = path.resolve(__dirname, '..');

function sections(text) {
  const result = {};
  let current;
  for (const raw of text.split('\n')) {
    const line = raw.trim();
    if (!line || line.startsWith('#')) continue;
    if (line.startsWith('[')) {
      current = line.slice(1, -1);
      assert.equal(result[current], undefined, `Duplicate section ${current}`);
      result[current] = [];
    } else {
      assert.ok(current, 'Setting outside section');
      result[current].push(line);
    }
  }
  return result;
}

function bindings(config) {
  return Object.fromEntries(config.filter_remote.map(line => {
    const fields = Object.fromEntries(line.split(', ').slice(1).map(field => field.split('=')));
    return [fields.tag, fields['force-policy']];
  }));
}

function checkReferences(config) {
  const policies = new Map(config.policy.map(line => {
    const [name, ...fields] = line.slice('static='.length).split(', ');
    return [name, fields.filter(field => !field.includes('='))];
  }));
  assert.equal(policies.size, config.policy.length);
  const known = new Set([...policies.keys(), 'direct', 'reject']);
  for (const [name, candidates] of policies) {
    for (const candidate of candidates) assert.ok(known.has(candidate), `${name} -> ${candidate}`);
  }
  for (const policy of Object.values(bindings(config))) assert.ok(known.has(policy), policy);
  for (const name of policies.keys()) {
    function visit(node, trail) {
      assert.ok(!trail.has(node), `Policy cycle: ${node}`);
      for (const child of policies.get(node) || []) visit(child, new Set([...trail, node]));
    }
    visit(name, new Set());
  }
  assert.deepEqual(config.filter_local, ['final, ✈️Final']);
}

test('all 4096 group selections keep routing resources and valid acyclic policy references', () => {
  const resources = sections(renderConfig([])).filter_remote.map(line => line.split(',')[0]);
  for (let mask = 0; mask < 2 ** SERVICES.length; mask++) {
    const groups = SERVICES.filter((_, i) => mask & (1 << i)).map(service => service.id);
    const config = sections(renderConfig(groups));
    assert.deepEqual(config.filter_remote.map(line => line.split(',')[0]), resources);
    checkReferences(config);
  }
});

test('custom base-only selection retains Apple/Microsoft direct and overseas proxy bindings', () => {
  const config = sections(renderConfig([]));
  assert.equal(config.policy.length, 4);
  const actual = bindings(config);
  assert.equal(actual['Local-Apple'], '🎯Direct');
  assert.equal(actual['Upstream-Microsoft'], '🎯Direct');
  assert.equal(actual['Local-ChatGPT'], 'Proxies');
  assert.equal(actual['Upstream-Netflix'], 'Proxies');
  assert.equal(actual['Upstream-China'], 'direct');
  assert.equal(actual['China-IP'], 'direct');
  assert.equal(actual['Upstream-Hijacking'], 'AdBlock');
  assert.equal(actual['Local-Advertising'], 'AdBlock');
});

test('AI groups inherit selectively and independent groups can choose subscription nodes', () => {
  const config = sections(renderConfig(['AI', 'ChatGPT', 'Apple']));
  const actual = bindings(config);
  assert.equal(actual['Local-ChatGPT'], 'ChatGPT');
  assert.equal(actual['Upstream-OpenAI'], 'ChatGPT');
  assert.equal(actual['Local-Claude'], 'AI');
  assert.equal(actual['Upstream-Gemini'], 'AI');
  assert.equal(actual['Local-Google'], 'Proxies');
  assert.ok(config.policy.includes('static=ChatGPT, AI, 🎯Direct, server-tag-regex=.*'));
  assert.ok(config.policy.includes('static=Apple, 🎯Direct, Proxies, server-tag-regex=.*'));
  assert.equal(bindings(sections(renderConfig(['ChatGPT'])))['Local-Claude'], 'Proxies');
});

test('specific AI/video precede Google, service lists precede broad rules and region fallback', () => {
  const lines = sections(renderConfig()).filter_remote;
  const index = tag => lines.findIndex(line => line.includes(`tag=${tag},`));
  for (const tag of ['Local-ChatGPT', 'Upstream-OpenAI', 'Upstream-Gemini', 'Upstream-YouTube']) {
    assert.ok(index(tag) < index('Local-Google'));
  }
  assert.ok(index('Local-LAN') < index('Upstream-Hijacking'));
  assert.ok(index('Upstream-Google') < index('Upstream-Global'));
  assert.ok(index('Upstream-Global') < index('Upstream-China'));
  assert.ok(index('Upstream-China') < index('China-IP'));
  assert.equal(index('China-IP'), lines.length - 1);
});

test('published presets match generator and every own rule exists and is bound explicitly', () => {
  assert.deepEqual(Object.keys(PRESETS), ['recommended', 'extended']);
  assert.ok(!fs.existsSync(path.join(ROOT, 'config/lite.conf')));
  for (const [name, groups] of Object.entries(PRESETS)) {
    const output = renderConfig(groups);
    assert.equal(fs.readFileSync(path.join(ROOT, 'config', `${name}.conf`), 'utf8'), output);
    const config = sections(output);
    assert.equal(config.policy.length, { recommended: 10, extended: 16 }[name]);
    const own = config.filter_remote.filter(line => line.includes('/lonecoding/'));
    assert.equal(own.length, 11);
    for (const line of own) {
      const file = new URL(line.split(',')[0]).pathname.split('/main/')[1];
      assert.ok(fs.existsSync(path.join(ROOT, file)), file);
      assert.match(line, /force-policy=/);
    }
  }
});

test('parser, DNS, credentials and empty rewrite sections have safe explicit defaults', () => {
  const output = renderConfig();
  const config = sections(output);
  assert.ok(config.general.includes(`resource_parser_url=${PARSER_URL}`));
  assert.equal(config.general.filter(line => line.startsWith('resource_parser_url=')).length, 1);
  assert.ok(config.dns.includes('no-ipv6'));
  assert.ok(!config.dns.includes('no-system'));
  for (const section of ['server_remote', 'server_local', 'rewrite_remote', 'rewrite_local', 'task_local', 'mitm']) {
    assert.deepEqual(config[section], []);
  }
  assert.match(output, /# https:\/\/example.com\/subscription, .*opt-parser=true/);
  assert.ok(!config.filter_remote.some(line => line.includes('opt-parser=')));
  assert.ok(!output.includes('fallback_udp_policy=direct'));
});

test('invalid groups and injection attempts fail before rendering', () => {
  for (const groups of [['AI', 'AI'], ['Unknown'], ['AI\n[mitm]'], [''], 'AI']) {
    assert.throws(() => renderConfig(groups));
  }
});

test('CLI selection, interactive choice, and errors produce importable output or no config', () => {
  const run = (args, input) => spawnSync(process.execPath, ['scripts/generate_profiles.js', ...args], {
    cwd: ROOT, input, encoding: 'utf8',
  });
  for (const [args, groups] of [
    [[], PRESETS.recommended], [['--preset', 'extended'], PRESETS.extended],
    [['--groups', 'AI,Telegram'], ['AI', 'Telegram']], [['--groups', 'none'], []],
  ]) {
    const result = run(args);
    assert.equal(result.status, 0, result.stderr);
    assert.equal(result.stdout, renderConfig(groups));
  }
  const interactive = run(['--interactive'], 'AI,Telegram\n');
  assert.equal(interactive.status, 0, interactive.stderr);
  assert.equal(interactive.stdout, renderConfig(['AI', 'Telegram']));
  for (const args of [['--preset', 'lite'], ['--preset', 'toString'], ['--groups', ''], ['--groups', 'AI,AI'], ['--preset'], ['--write', '--groups', 'AI']]) {
    const result = run(args);
    assert.notEqual(result.status, 0);
    assert.equal(result.stdout, '');
  }
});
