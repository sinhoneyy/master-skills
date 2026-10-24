import test from 'node:test';
import assert from 'node:assert/strict';
import path from 'node:path';
import { runStitch } from '../skills/full-page-screenshot/scripts/stitch-data.mjs';

test('screenshot filenames stay inert across shell and Python metacharacters', () => {
  const hostile = ['name with spaces.png', 'quote";print(123);#.png',
    '$(touch sentinel).png', '`touch sentinel`.png', "single'quote.png",
    'C:\\temp\\new\\tile.png', '-c.png', 'unicode-☃.png', 'newline\n.png'];
  for (const output of hostile) {
    const tiles = [[output, 0], ['second.png', 10]];
    let calls = 0;
    const result = runStitch('-script.py', output, tiles, (program, args, options) => {
      calls++;
      assert.equal(program, 'python3');
      assert.equal(args.length, 2);
      assert.equal(args[0], path.resolve('-script.py'));
      assert.deepEqual(JSON.parse(args[1]), { output, tiles });
      assert.notEqual(options.shell, true);
      assert.equal(options.timeout, 60000);
      return 'stitched';
    });
    assert.equal(result, 'stitched');
    assert.equal(calls, 1);
  }
});
