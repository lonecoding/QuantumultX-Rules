'use strict';

// Offline configuration contracts: preserved resource coverage, valid policy
// references, and CLI output. These tests do not emulate Quantumult X routing.

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
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
  assert.deepEqual(policies.get('🎯Direct'), ['direct']);
}

test('all group selections keep routing resources and valid acyclic policy references', () => {
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
  assert.equal(config.policy.length, 5);
  const actual = bindings(config);
  assert.equal(actual['Upstream-Apple'], '🎯Direct');
  assert.equal(actual['Upstream-Microsoft'], '🎯Direct');
  assert.equal(actual['Upstream-OpenAI'], 'Proxies');
  assert.equal(actual['Upstream-Netflix'], 'Proxies');
  assert.equal(actual['Upstream-China'], 'direct');
  assert.equal(actual['China-IP'], 'direct');
  assert.equal(actual['Upstream-Hijacking'], 'Hijacking');
  assert.equal(actual['Upstream-Advertising'], 'AdBlock');
});

test('AI groups inherit selectively and independent groups can choose subscription nodes', () => {
  const config = sections(renderConfig(['AI', 'ChatGPT', 'Apple']));
  const actual = bindings(config);
  assert.equal(actual['Upstream-OpenAI'], 'ChatGPT');
  assert.equal(actual['Upstream-OpenAI'], 'ChatGPT');
  assert.equal(actual['Upstream-Claude'], 'AI');
  assert.equal(actual['Upstream-Gemini'], 'AI');
  assert.equal(actual['Upstream-Google'], 'Proxies');
  assert.ok(config.policy.includes('static=ChatGPT, AI, 🎯Direct, server-tag-regex=.*'));
  assert.ok(config.policy.includes('static=Apple, 🎯Direct, Proxies, server-tag-regex=.*'));
  assert.equal(bindings(sections(renderConfig(['ChatGPT'])))['Upstream-Claude'], 'Proxies');
});

test('specific AI/video precede Google, service lists precede broad rules and region fallback', () => {
  const lines = sections(renderConfig()).filter_remote;
  const index = tag => lines.findIndex(line => line.includes(`tag=${tag},`));
  for (const tag of ['Upstream-OpenAI', 'Upstream-Gemini', 'Upstream-YouTube']) {
    assert.ok(index(tag) < index('Upstream-Google'));
  }
  assert.ok(index('LAN') < index('Upstream-Hijacking'));
  assert.ok(index('Upstream-Google') < index('Upstream-Global'));
  assert.ok(index('Upstream-Global') < index('Upstream-China'));
  assert.ok(index('Upstream-China') < index('China-IP'));
  assert.equal(index('China-IP'), lines.length - 1);
});

test('published presets import only upstream rules and built-in resources', () => {
  assert.deepEqual(Object.keys(PRESETS), ['recommended', 'extended']);
  for (const [name, groups] of Object.entries({ ...PRESETS, full: PRESETS.recommended, daily: PRESETS.recommended })) {
    const output = renderConfig(groups);
    assert.equal(fs.readFileSync(path.join(ROOT, 'config', `${name}.conf`), 'utf8'), output);
    const config = sections(output);
    assert.equal(config.policy.length, { recommended: 11, extended: 20, full: 11, daily: 11 }[name]);
    const urls = config.filter_remote.filter(line => line.startsWith('https://'));
    assert.equal(urls.length, 18);
    assert.equal(new Set(urls.map(line => line.split(',')[0])).size, urls.length);
    for (const line of urls) {
      assert.match(line, /^https:\/\/raw\.githubusercontent\.com\/blackmatrix7\/ios_rule_script\/master\/rule\/QuantumultX\//);
      assert.match(line, /force-policy=/);
    }
    assert.ok(!output.includes('/main/rules/'));
    assert.ok(!config.policy.some(line => /^static=(LAN|China),/.test(line)));
    assert.ok(config.filter_remote.includes('FILTER_LAN, tag=LAN, force-policy=direct, inserted-resource=true, enabled=true'));
    assert.deepEqual(config.filter_local, ['final, ✈️Final']);
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

test('CLI exports presets, custom and interactive selections without mixing prompts into files', t => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'qx-export-'));
  t.after(() => fs.rmSync(directory, { recursive: true, force: true }));
  const script = path.join(ROOT, 'scripts/generate_profiles.js');
  const choices = [
    [[], PRESETS.recommended],
    [['--preset', 'extended'], PRESETS.extended],
    [['--groups', 'AI,Telegram'], ['AI', 'Telegram']],
    [['--groups', 'none'], []],
    [['--interactive'], ['Google', 'YouTube'], 'Google,YouTube\n'],
    [['--interactive'], PRESETS.recommended, '\n'],
  ];
  for (const [i, [args, groups, input]] of choices.entries()) {
    const file = `custom ${i}.conf`;
    const result = spawnSync(process.execPath, [script, '--output', file, ...args], {
      cwd: directory, encoding: 'utf8', input, timeout: 5000,
    });
    assert.equal(result.status, 0, result.stderr);
    assert.equal(result.stdout, '');
    assert.match(result.stderr, /Saved:/);
    assert.equal(fs.readFileSync(path.join(directory, file), 'utf8'), renderConfig(groups));
  }
});

test('CLI export preserves existing files, directories and symlink targets', t => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'qx-preserve-'));
  t.after(() => fs.rmSync(directory, { recursive: true, force: true }));
  const existing = path.join(directory, 'existing.conf');
  const link = path.join(directory, 'link.conf');
  const dangling = path.join(directory, 'dangling.conf');
  const missing = path.join(directory, 'missing.conf');
  const original = '# User configuration with private local changes\n';
  fs.writeFileSync(existing, original);
  fs.symlinkSync(existing, link);
  fs.symlinkSync(missing, dangling);
  for (const file of [existing, link, dangling, directory]) {
    const result = spawnSync(process.execPath, ['scripts/generate_profiles.js', '--groups', 'AI', '--output', file], {
      cwd: ROOT, encoding: 'utf8', timeout: 5000,
    });
    assert.equal(result.status, 1, result.stderr);
    assert.equal(result.stdout, '');
    assert.match(result.stderr, /File already exists/);
    assert.equal(fs.readFileSync(existing, 'utf8'), original);
    assert.equal(fs.existsSync(missing), false);
  }
  assert.equal(fs.lstatSync(link).isSymbolicLink(), true);
  assert.equal(fs.lstatSync(dangling).isSymbolicLink(), true);
});

test('CLI errors and closed interactive input produce no export and a failure status', t => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'qx-invalid-'));
  t.after(() => fs.rmSync(directory, { recursive: true, force: true }));
  const file = path.join(directory, 'new.conf');
  for (const args of [
    ['--groups', 'Typo'], ['--groups', 'AI,AI'], ['--preset', 'unknown'],
    ['--write'], ['--check'], ['--help'], ['--interactive'],
    ['--output', path.join(directory, 'duplicate.conf')],
    ['--preset', 'extended', '--groups', 'AI'],
  ]) {
    const result = spawnSync(process.execPath, ['scripts/generate_profiles.js', ...args, '--output', file], {
      cwd: ROOT, encoding: 'utf8', input: '', timeout: 5000,
    });
    assert.equal(result.status, 1, result.stderr);
    assert.equal(result.stdout, '');
    assert.notEqual(result.stderr, '');
    assert.deepEqual(fs.readdirSync(directory), []);
  }
  for (const args of [['--output'], ['--output', ''], ['--output', '--groups', 'AI'], ['--interactive']]) {
    const result = spawnSync(process.execPath, ['scripts/generate_profiles.js', ...args], {
      cwd: ROOT, encoding: 'utf8', input: '', timeout: 5000,
    });
    assert.equal(result.status, 1, result.stderr);
    assert.equal(result.stdout, '');
  }
  const missingParent = spawnSync(process.execPath, ['scripts/generate_profiles.js', '--output', path.join(directory, 'absent', 'out.conf')], {
    cwd: ROOT, encoding: 'utf8', timeout: 5000,
  });
  assert.equal(missingParent.status, 1);
  assert.match(missingParent.stderr, /Cannot save configuration/);
  assert.deepEqual(fs.readdirSync(directory), []);
});


test('blocking controls are independent and direct remains fixed in every template', () => {
  for (const name of ['recommended', 'extended', 'full', 'daily']) {
    const text = fs.readFileSync(path.join(ROOT, 'config', `${name}.conf`), 'utf8');
    const line = text.split('\n').find(line => line.startsWith('static=🎯Direct,'));
    assert.ok(line);
    assert.deepEqual(line.split(',').slice(1).map(v => v.trim()).filter(v => !v.includes('=')), ['direct']);
  }
  const config = sections(renderConfig());
  const actual = bindings(config);
  assert.equal(actual['Upstream-Advertising'], 'AdBlock');
  assert.equal(actual['Upstream-Hijacking'], 'Hijacking');
  assert.ok(config.policy.includes('static=AdBlock, reject, direct'));
  assert.ok(config.policy.includes('static=Hijacking, reject, direct'));
});

test('vendor services bind upstream lists to independent policies before broad lists', () => {
  for (const groups of [[], PRESETS.recommended, PRESETS.extended, ['Copilot'], ['AppleTV', 'AppleNews']]) {
    const config = sections(renderConfig(groups));
    const actual = bindings(config);
    const position = tag => config.filter_remote.findIndex(line => line.includes(`tag=${tag},`));
    for (const service of ['AppleTV', 'AppleNews']) {
      assert.equal(actual[`Upstream-${service}`], groups.includes(service) ? service : 'Proxies');
      assert.ok(position(`Upstream-${service}`) < position('Upstream-Apple'));
    }
    const policy = groups.includes('Copilot') ? 'Copilot' : groups.includes('AI') ? 'AI' : 'Proxies';
    assert.equal(actual['Upstream-Copilot'], policy);
    assert.ok(position('Upstream-OpenAI') < position('Upstream-Copilot'));
    assert.ok(position('Upstream-Copilot') < position('Upstream-Microsoft'));
    assert.deepEqual(config.filter_local, ['final, ✈️Final']);
  }
});

test('YouTube inherits Google when available and supports custom independent choices', () => {
  const config = sections(renderConfig(PRESETS.recommended));
  assert.ok(config.policy.includes('static=YouTube, Google, 🎯Direct, server-tag-regex=.*'));
  assert.ok(config.policy.findIndex(line => line.startsWith('static=Google,')) < config.policy.findIndex(line => line.startsWith('static=YouTube,')));
  assert.equal(bindings(sections(renderConfig(['Google'])))['Upstream-YouTube'], 'Google');
  assert.equal(bindings(sections(renderConfig([])))['Upstream-YouTube'], 'Proxies');
  assert.ok(sections(renderConfig(['YouTube'])).policy.includes('static=YouTube, Proxies, 🎯Direct, server-tag-regex=.*'));
});
