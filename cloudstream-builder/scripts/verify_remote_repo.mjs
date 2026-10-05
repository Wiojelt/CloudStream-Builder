#!/usr/bin/env node
// Audit the exact public CloudStream install chain after a repository push.
import { createHash } from 'node:crypto';

const roots = process.argv.slice(2);
if (roots.length === 0) {
  console.error('Usage: node verify_remote_repo.mjs <repo.json URL> [more repo.json URLs]');
  process.exit(2);
}

async function get(url) {
  const response = await fetch(url, { cache: 'no-store', signal: AbortSignal.timeout(15000) });
  if (!response.ok) throw new Error(`${response.status} ${url}`);
  return response;
}

let failures = 0;
for (const root of roots) {
  try {
    const repository = await (await get(root)).json();
    if (!Array.isArray(repository.pluginLists) || repository.pluginLists.length === 0) {
      throw new Error(`repo.json has no pluginLists: ${root}`);
    }
    for (const catalogUrl of repository.pluginLists) {
      const entries = await (await get(catalogUrl)).json();
      if (!Array.isArray(entries)) throw new Error(`Catalog is not an array: ${catalogUrl}`);
      let passed = 0;
      for (const entry of entries) {
        try {
          const bytes = Buffer.from(await (await get(entry.url)).arrayBuffer());
          const digest = createHash('sha256').update(bytes).digest('hex');
          const valid = entry.fileSize === bytes.length && entry.fileHash === `sha256-${digest}` &&
            (entry.hash === undefined || entry.hash === digest);
          if (!valid) {
            failures++;
            console.error(`MISMATCH ${entry.internalName}: expected ${entry.fileSize} ${entry.fileHash}; downloaded ${bytes.length} sha256-${digest}`);
          } else {
            passed++;
          }
        } catch (error) {
          failures++;
          console.error(`ERROR ${entry.internalName ?? '<unnamed>'}: ${error.message}`);
        }
      }
      console.log(`${root}: ${passed}/${entries.length} packages match ${catalogUrl}`);
    }
  } catch (error) {
    failures++;
    console.error(`ERROR ${root}: ${error.message}`);
  }
}
process.exitCode = failures ? 1 : 0;
