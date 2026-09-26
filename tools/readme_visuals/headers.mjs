import fs from 'node:fs/promises';
import path from 'node:path';
import sharp from 'sharp';
import { OUT, TOOL, ASSET, C, newCanvas, txt, write, sha } from './lib.mjs';

// Production owns header inputs. The approved prototype remains a frozen reference.
const root = path.join(ASSET, 'headers');
const spec = JSON.parse(await fs.readFile(path.join(root, 'src/copy.json'), 'utf8'));
const { width, height, minimum_display_width: minimumWidth } = spec.canvas;
const original = await fs.readFile(path.join(root, 'src/fundo_tecnologico_original.png'));
const originalMeta = await sharp(original).metadata();
const checks = [];
function check(ok, detail) {
  checks.push({ ok: Boolean(ok), detail });
  if (!ok) throw new Error(detail);
}
const originalRatio = originalMeta.width / originalMeta.height;
const artWidth = Math.round(height * originalRatio);
check(artWidth < width, 'Artwork fits without crop or distortion');
const bgCanvas = newCanvas(width, height, 'Fundo decorativo, sem informação operacional');
bgCanvas.draw.clear();
bgCanvas.draw.rect(width, height).fill(C.background);
bgCanvas.draw.image(`data:image/png;base64,${original.toString('base64')}`)
  .size(artWidth, height).move(width - artWidth, 0);
// Blend the left edge of the contained illustration into the flat text safe zone.
const blend = bgCanvas.draw.gradient('linear', add => {
  add.stop(0, C.background, 1);
  add.stop(.56, C.background, 1);
  add.stop(.72, C.background, .6);
  add.stop(1, C.background, 0);
});
blend.from(0, 0).to(1, 0);
bgCanvas.draw.rect(1450, height).fill(blend);
const background = await sharp(Buffer.from(bgCanvas.draw.svg())).png().toBuffer();
const { data: pixels, info } = await sharp(background).removeAlpha().raw().toBuffer({ resolveWithObject: true });
const lum = rgb => rgb.map(v => { const c = v / 255; return c <= .04045 ? c / 12.92 : ((c + .055) / 1.055) ** 2.4; })
  .reduce((s, c, i) => s + c * [.2126, .7152, .0722][i], 0);
const luminanceOfHex = hex => lum([1, 3, 5].map(i => parseInt(hex.slice(i, i + 2), 16)));
const entries = [];
for (const header of spec.headers) {
  const s = newCanvas(width, height, header.alt);
  s.draw.clear();
  // This editable SVG contains exact type paths only; it is not the complete artwork.
  for (const row of header.lines) {
    txt(s, s.draw, row.text, row.x, row.baseline, {
      size: row.size, weight: row.weight, color: row.color, maxWidth: row.max_width,
    });
  }
  check(header.lines.map(row => row.text).join(' ') === header.alt.replace(' — ', ' '), `${header.id}: verbatim approved copy`);
  for (const t of s.texts) {
    check(t.x >= 64 && t.x + t.width <= 1170 && t.y >= 56 && t.y + t.height <= height - 56, `${header.id}: safe zone: ${t.text}`);
    check(t.size * minimumWidth / width >= 18, `${header.id}: minimum effective type at ${minimumWidth}px: ${t.text}`);
    let worst = Infinity;
    const fg = luminanceOfHex(t.color);
    for (let y = Math.floor(t.y); y < Math.ceil(t.y + t.height); y++) {
      for (let x = Math.floor(t.x); x < Math.ceil(t.x + t.width); x++) {
        const i = (y * width + x) * info.channels;
        const bg = lum([pixels[i], pixels[i + 1], pixels[i + 2]]);
        const ratio = (Math.max(fg, bg) + .05) / (Math.min(fg, bg) + .05);
        worst = Math.min(worst, ratio);
      }
    }
    t.contrast_against_background_min = Number(worst.toFixed(3));
    check(worst >= 4.5, `${header.id}: contrast >= 4.5: ${t.text}`);
  }
  for (let i = 0; i < s.texts.length; i++) for (let j = i + 1; j < s.texts.length; j++) {
    const a = s.texts[i], b = s.texts[j];
    check(a.x + a.width <= b.x || b.x + b.width <= a.x || a.y + a.height <= b.y || b.y + b.height <= a.y, `${header.id}: separate text boxes ${i}/${j}`);
  }
  const overlay = Buffer.from(s.draw.svg());
  await write(path.join(root, `src/${header.id}_tipografia.svg`), overlay);
  const result = await sharp(background).composite([{ input: overlay }]).png({ compressionLevel: 9 }).toBuffer();
  const output = `png/${header.id}.png`;
  await write(path.join(root, output), result);
  const reduced = [];
  for (const w of [720, 960]) {
    const samplePath = `qa/${header.id}_${w}.png`;
    const sample = await sharp(result).resize({ width: w }).png().toBuffer();
    await write(path.join(root, samplePath), sample);
    reduced.push({ path: samplePath, sha256: sha(sample), display_width: w });
  }
  entries.push({ id: header.id, alt: header.alt, uses: header.uses, path: output,
    width, height, bytes: result.length, sha256: sha(result), texts: s.texts, reduced });
}
const inputPaths = [
  ['copy', path.join(root, 'src/copy.json')],
  ['generator', path.join(TOOL, 'headers.mjs')],
  ['shared_library', path.join(TOOL, 'lib.mjs')],
  ['visual_tokens', path.join(ASSET, 'visual_system/tokens.yaml')],
  ['dependency_lock', path.join(TOOL, 'pnpm-lock.yaml')],
  ...[400, 600, 700].map(w => [`inter_${w}`, path.join(TOOL, `node_modules/@fontsource/inter/files/inter-latin-${w}-normal.woff`)]),
];
const inputHashes = Object.fromEntries(await Promise.all(inputPaths.map(async ([key, p]) => [key, sha(await fs.readFile(p))])));
await write(path.join(root, 'manifest.json'), JSON.stringify({
  schema_version: 1, status: spec.status, scope: 'shared_readme_notebook_headers',
  render_mode: 'frozen_generated_background_plus_deterministic_typography',
  original: { path: 'src/fundo_tecnologico_original.png', width: originalMeta.width, height: originalMeta.height, sha256: sha(original) },
  input_hashes: inputHashes, headers: entries,
}, null, 2) + '\n');
await write(path.join(root, 'qa/validation.json'), JSON.stringify({
  status: 'pass', check_count: checks.length, checks,
  limitations: ['Technical checks do not replace visual inspection in the consuming Markdown surface.'],
}, null, 2) + '\n');
console.log(JSON.stringify({ outputs: entries.map(e => ({ path: e.path, bytes: e.bytes, sha256: e.sha256 })), checks: checks.length, status: 'pass' }, null, 2));
