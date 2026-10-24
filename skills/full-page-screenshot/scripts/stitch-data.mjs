// Filenames travel as argv data, never as shell syntax or Python source.
import { execFileSync } from 'node:child_process';
import path from 'node:path';

export function pythonImageData(outputFile, tiles) {
  return JSON.stringify({ output: outputFile, tiles });
}

export function runStitch(scriptPath, outputFile, tiles, run = execFileSync) {
  return run('python3', [path.resolve(scriptPath), pythonImageData(outputFile, tiles)], {
    encoding: 'utf-8', timeout: 60000,
  });
}
