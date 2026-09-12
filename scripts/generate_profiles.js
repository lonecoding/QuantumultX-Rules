#!/usr/bin/env node
'use strict';

const fs = require('node:fs');
const path = require('node:path');
const { PRESETS, SERVICES, renderConfig } = require('./config-builder.js');
const ROOT = path.resolve(__dirname, '..');
const HELP = `Generate complete Quantumult X configurations (Node.js 22+; no dependencies).

  node scripts/generate_profiles.js                 Print the recommended config
  node scripts/generate_profiles.js --preset extended   Print a preset
  node scripts/generate_profiles.js --groups AI,Telegram,YouTube
  node scripts/generate_profiles.js --interactive   Choose groups interactively
  node scripts/generate_profiles.js --groups AI,Telegram --output ../my-quantumultx.conf
  node scripts/generate_profiles.js --write         Regenerate all published presets
  node scripts/generate_profiles.js --check         Check published presets without writing

Presets: ${Object.keys(PRESETS).join(', ')}
Groups: ${SERVICES.map(service => service.id).join(', ')}
Use --groups none for base groups only. Service rules remain active when groups
are omitted. Add subscriptions only on your device; this tool never fetches them.
Use --output PATH to save a new file (also works with --preset or --interactive).
Existing files are never overwritten. The parent directory must already exist.
Without --output, the configuration is printed to stdout as before.
Prefer --output over shell redirection, which can truncate a file even on errors.
Save custom configurations outside this repository before adding subscriptions.
Setup and policy defaults: docs/profiles.md
`;

async function main(args) {
  const { mode, output } = parseOutput(args);
  args = mode;
  if (args.length === 1 && args[0] === '--help') {
    process.stdout.write(HELP);
    return;
  }
  if (args.length === 1 && ['--write', '--check'].includes(args[0])) {
    let stale = false;
    const outputs = { ...PRESETS, full: PRESETS.recommended, daily: PRESETS.recommended };
    for (const [preset, groups] of Object.entries(outputs)) {
      const file = path.join(ROOT, 'config', `${preset}.conf`);
      const expected = renderConfig(groups);
      if (fs.existsSync(file) && fs.readFileSync(file, 'utf8') === expected) continue;
      if (args[0] === '--check') {
        process.stderr.write(`Outdated: config/${preset}.conf\n`);
        stale = true;
      } else {
        fs.writeFileSync(file, expected, 'utf8');
        process.stderr.write(`Updated: config/${preset}.conf\n`);
      }
    }
    if (stale) throw new Error('Run node scripts/generate_profiles.js --write');
    return;
  }
  if (args.length === 1 && args[0] === '--interactive') {
    const readline = require('node:readline');
    const rl = readline.createInterface({ input: process.stdin, output: process.stderr });
    try {
      process.stderr.write(`可选策略组：${SERVICES.map(service => service.id).join(', ')}\n`);
      const answer = (await new Promise((resolve, reject) => {
        // readline does not call the question callback on EOF or Ctrl+C.
        rl.once('close', () => reject(new Error('Input closed before a selection was received; no configuration generated.')));
        rl.once('SIGINT', () => {
          const error = new Error('Cancelled; no configuration generated.');
          error.exitCode = 130;
          reject(error);
          rl.close();
        });
        rl.question('输入逗号分隔的组名，留空使用标准版，none 仅保留基础组：', resolve);
      })).trim();
      saveConfig(renderConfig(answer === '' ? PRESETS.recommended : parseGroups(answer)), output);
    } finally {
      rl.close();
    }
    return;
  }
  let groups = PRESETS.recommended;
  if (args.length === 2 && args[0] === '--preset') {
    if (!Object.hasOwn(PRESETS, args[1])) throw new Error(`Unknown preset: ${args[1]}`);
    groups = PRESETS[args[1]];
  } else if (args.length === 2 && args[0] === '--groups') {
    groups = parseGroups(args[1]);
  } else if (args.length) {
    throw new Error('Invalid arguments. Use --help; choose one mode at a time.');
  }
  saveConfig(renderConfig(groups), output);
}

function parseOutput(args) {
  const mode = [];
  let output;
  for (let i = 0; i < args.length; i++) {
    if (args[i] !== '--output') {
      mode.push(args[i]);
      continue;
    }
    if (output !== undefined) throw new Error('Use --output only once.');
    output = args[++i];
    if (!output || output.startsWith('--')) throw new Error('--output requires a file path.');
  }
  if (output !== undefined && mode.some(arg => ['--write', '--check', '--help'].includes(arg))) {
    throw new Error('--output cannot be combined with --write, --check or --help.');
  }
  return { mode, output };
}

function saveConfig(config, output) {
  if (output === undefined) {
    process.stdout.write(config);
    return;
  }
  // Exclusive creation also refuses symlinks; an existence check alone would race.
  try {
    fs.writeFileSync(output, config, { encoding: 'utf8', flag: 'wx', mode: 0o600 });
  } catch (error) {
    if (error.code === 'EEXIST') throw new Error(`File already exists: ${output}. Choose a new filename; nothing was overwritten.`);
    throw new Error(`Cannot save configuration to ${output}: ${error.message}`);
  }
  process.stderr.write(`Saved: ${path.resolve(output)}\n`);
}

function parseGroups(value) {
  if (value === 'none') return [];
  return value.split(',').map(group => group.trim());
}

main(process.argv.slice(2)).catch(error => {
  process.stderr.write(`${error.message}\n`);
  process.exitCode = error.exitCode || 1;
});
