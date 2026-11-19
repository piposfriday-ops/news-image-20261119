// News-image entry for 19 November 2026 (Node 22, standard library only).
// The image is entry.png beside this file; the program copies it to
// /output/entry.png. The gate takes a whole PNG or JPEG of at most 1 MiB
// and 1024 by 1024 pixels, and the judge sees exactly the bytes copied.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
//
// The image itself is drawn by draw.py (Python + Pillow, deterministic,
// no network): a newspaper front page for Thursday 19 November 2026.

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

copyFileSync(
  new URL('./entry.png', import.meta.url),
  join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'),
);
