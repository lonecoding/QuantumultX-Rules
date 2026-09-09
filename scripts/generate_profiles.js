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
  node scripts/generate_profiles.js --write         Regenerate all published presets
  node scripts/generate_profiles.js --check         Check published presets without writing

Presets: ${Object.keys(PRESETS).join(', ')}
Groups: ${SERVICES.map(service => service.id).join(', ')}
Use --groups none for base groups only. Service rules remain active when groups
are omitted. Add subscriptions only on your device; this tool never fetches them.
Redirect custom output to a file outside this repository before importing it.
Example: node scripts/generate_profiles.js --groups AI,Telegram > ../my-quantumultx.conf
Setup and policy defaults: docs/profiles.md
`;

async function main(args) {
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
    const readline = require('node:readline/promises');
    const rl = readline.createInterface({ input: process.stdin, output: process.stderr });
    try {
      process.stderr.write(`可选策略组：${SERVICES.map(service => service.id).join(', ')}\n`);
      const answer = (await rl.question('输入逗号分隔的组名，留空使用标准版，none 仅保留基础组：')).trim();
      process.stdout.write(renderConfig(answer === '' ? PRESETS.recommended : parseGroups(answer)));
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
  process.stdout.write(renderConfig(groups));
}

function parseGroups(value) {
  if (value === 'none') return [];
  return value.split(',').map(group => group.trim());
}

main(process.argv.slice(2)).catch(error => {
  process.stderr.write(`${error.message}\n`);
  process.exitCode = 1;
});
