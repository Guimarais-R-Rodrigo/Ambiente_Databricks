import fs from 'node:fs/promises';
import path from 'node:path';
import sharp from 'sharp';
import { OUT, write, newCanvas, txt, C } from './lib.mjs';

const manifest=JSON.parse(await fs.readFile(path.join(OUT,'manifest.json'),'utf8'));
const resized=[];
let md='# Comparações — baseline e proposta\n\nAs composições têm proporções diferentes. Cada imagem foi encaixada sem distorção; a altura vazia da comparação não faz parte do protótipo.\n\n';
for(const item of manifest.assets){
  const state=newCanvas(1680,780,item.title);
  txt(state,state.draw,'BASELINE',40,48,{size:24,color:C.muted,weight:700});
  txt(state,state.draw,'PROPOSTA · SPRINT 0',875,48,{size:24,color:C.hub_custom,weight:700});
  const bg=await sharp(Buffer.from(state.draw.svg())).png().toBuffer();
  const old=await sharp(path.join(OUT,item.baseline)).resize({width:790,height:650,fit:'contain',background:C.background}).png().toBuffer();
  const next=await sharp(path.join(OUT,item.variants[0].png)).resize({width:790,height:650,fit:'contain',background:C.background}).png().toBuffer();
  const png=await sharp(bg).composite([{input:old,left:40,top:85},{input:next,left:850,top:85}]).png().toBuffer();
  const rel=`comparisons/${item.id.replace('.','_')}.png`;
  await write(path.join(OUT,rel),png);
  resized.push(await sharp(png).resize(1400,650).png().toBuffer());
  md+=`## ${item.title}\n\n![Comparação de ${item.title}](${rel})\n\n${item.caption}\n\n`;
}
await write(path.join(OUT,'README_COMPARACOES.md'),md);
const sheet=await sharp({create:{width:1400,height:650*resized.length,channels:3,background:C.background}}).composite(resized.map((input,i)=>({input,left:0,top:i*650}))).png().toBuffer();
await write(path.join(OUT,'comparisons/visao_geral.png'),sheet);
console.log('Five comparison sheets and one overview created.');
