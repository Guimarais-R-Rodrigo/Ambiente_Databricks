import fs from 'node:fs/promises';
import path from 'node:path';
import sharp from 'sharp';
import {OUT,write} from './lib.mjs';
const m=JSON.parse(await fs.readFile(path.join(OUT,'manifest.json'),'utf8'));
const entries=[];
for(const a of m.assets){
  for(const width of [720,900,1200]){
    const file=`qa/scales/${a.id.replace('.','_')}_${width}.png`;
    await write(path.join(OUT,file),await sharp(path.join(OUT,a.variants[0].png)).resize({width}).png().toBuffer());
    entries.push({id:a.id,width,png:file});
  }
}
await write(path.join(OUT,'qa/scales.json'),JSON.stringify(entries,null,2)+'\n');
console.log('15 scale samples (720/900/1200 px) generated.');
