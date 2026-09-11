import fs from 'node:fs/promises';
import path from 'node:path';
import sharp from 'sharp';
import YAML from 'yaml';
import {ROOT,OUT,ASSET,TOOL,tokens,readYaml,sha,write,newCanvas} from './lib.mjs';

const family=process.argv[process.argv.indexOf('--family')+1];
if(!['top','snippets','scripts','skills','prompts','all'].includes(family)) throw new Error('Use --family top|snippets|scripts|skills|prompts|all');
const groups={top:['raiz','assistant'],snippets:['snippets'],scripts:['scripts'],skills:['skills'],prompts:['prompts']};
const selected=family==='all'?Object.values(groups).flat():groups[family];
const contracts=(await readYaml(path.join(ASSET,'specs/visual_contracts.yaml'))).contracts;
const approved=JSON.parse(await fs.readFile(path.join(ASSET,'specs/approved_signatures.json'),'utf8'));
const map={};
for(const [moduleName,families] of [['top',['raiz','assistant']],['snippets',['snippets']],['scripts',['scripts']],['methods',['skills','prompts']]]){
  if(selected.some(f=>families.includes(f))) Object.assign(map,(await import(`./archetypes/${moduleName}.mjs`)).renderers);
}
const metadataDir=path.join(ASSET,'qa/figures');
const produced=[];
for(const c of contracts.filter(c=>selected.includes(c.id.split('.')[0]))){
  const [group,name]=c.id.split('.');
  const source=`readmes/${group}/sources/${name}.svg`,published=`readmes/${group}/png/${name}.png`;
  let svg,png,texts,icons,dimensions;
  if(c.prototype){
    // Copy the approved signature, do not interpret or regenerate its visual design.
    const v=approved.assets.find(a=>a.id===c.id)?.variants.find(v=>v.mode==='readme');
    if(!v)throw new Error(`Approved signature absent: ${c.id}`);
    svg=await fs.readFile(path.join(ASSET,v.svg));
    png=await sharp(svg).png({compressionLevel:9}).toBuffer();
    if(sha(svg)!==v.svg_sha256||sha(png)!==v.png_sha256)throw new Error(`Approval baseline changed: ${c.id}`);
    ({texts,icons}=v);dimensions={width:v.width,height:v.height,minimum_display_width:v.minimum_display_width};
  }else{
    const preset=tokens.presets[c.render_targets[0]];
    const s=newCanvas(preset.width,preset.height,c.alt);
    if(!map[c.id]) throw new Error(`Renderer absent: ${c.id}`);
    await map[c.id](s,c,'readme');
    svg=Buffer.from(s.draw.svg()+'\n');png=await sharp(svg).png({compressionLevel:9}).toBuffer();
    ({texts,icons}=s);dimensions=preset;
  }
  await write(path.join(ASSET,source),svg);await write(path.join(ASSET,published),png);
  const record={id:c.id,archetype:c.archetype,source,published,sha256:sha(png),svg_sha256:sha(svg),
    ...dimensions,question:c.question,alt:c.alt,caption:c.caption,owner_readme:c.owner_readme,
    anchor:c.planned_ascii_anchor,approved_signature:c.prototype,texts,icons:[...new Set(icons)]};
  await write(path.join(metadataDir,`${c.id}.json`),JSON.stringify(record,null,2)+'\n');
  await write(path.join(ROOT,'.artifacts/visual-v2/scales',`${c.id}_720.png`),await sharp(png).resize({width:720}).png().toBuffer());
  produced.push(c.id);
}
// Publish a complete index only after all sprint outputs are available.
const metadata=[];
for(const c of contracts){try{metadata.push(JSON.parse(await fs.readFile(path.join(metadataDir,`${c.id}.json`),'utf8')));}catch(e){if(e.code!=='ENOENT')throw e;}}
if(metadata.length===contracts.length){
  const headerManifest=JSON.parse(await fs.readFile(path.join(ASSET,'headers/manifest.json'),'utf8'));
  const inputs=[];
  const assetPrefix=path.relative(ROOT,ASSET).split(path.sep).join('/');
  const inputPaths=['tools/readme_visuals/production.mjs','tools/readme_visuals/validate_production.mjs','tools/readme_visuals/lib.mjs','tools/readme_visuals/headers.mjs','tools/readme_visuals/archetypes/top.mjs','tools/readme_visuals/archetypes/snippets.mjs','tools/readme_visuals/archetypes/scripts.mjs','tools/readme_visuals/archetypes/methods.mjs','tools/readme_visuals/package.json','tools/readme_visuals/pnpm-lock.yaml',
    ...['specs/visual_contracts.yaml','specs/approved_signatures.json','specs/approved_headers.json','specs/editorial_corrections.json','specs/prototype_copy.yaml','visual_system/tokens.yaml','visual_system/semantic_roles.yaml','visual_system/archetypes.yaml','headers/src/copy.json','headers/src/fundo_tecnologico_original.png'].map(p=>`${assetPrefix}/${p}`),
    ...[400,600,700,800].map(w=>`tools/readme_visuals/node_modules/@fontsource/inter/files/inter-latin-${w}-normal.woff`),
    ...[...new Set(metadata.flatMap(m=>m.icons))].sort().map(i=>`tools/readme_visuals/node_modules/lucide-static/icons/${i}.svg`)];
  for(const rel of inputPaths){
    inputs.push({path:rel,sha256:sha(await fs.readFile(path.join(ROOT,rel)))});
  }
  const manifest={version:2,generated_by:'tools/readme_visuals/production.mjs',approved_direction:'sprint_0',
    contracts:'specs/visual_contracts.yaml',inputs,
    assets:metadata.map(({texts,icons,...item})=>item),
    headers:headerManifest.headers.map(({texts,reduced,...h})=>({...h,path:`headers/${h.path}`}))};
  await write(path.join(ASSET,'manifest.yaml'),YAML.stringify(manifest,{lineWidth:110}));
  let transcript='# Conteúdo textual das figuras\n\nEste índice auxilia manutenção e leitura sem imagem. Os READMEs preservam as explicações e os exemplos copiáveis. Cabeçalhos são identidade decorativa, não instruções.\n\n';
  for(const a of metadata){
    transcript+=`## ${a.id}\n\n**Pergunta:** ${a.question}\n\n![${a.alt}](${a.published})\n\n${a.caption}\n\n`;
    transcript+=a.texts.map(t=>`- ${t.text}`).join('\n')+'\n\n';
  }
  await write(path.join(ASSET,'CONTEUDO_FIGURAS.md'),transcript);
  if(process.argv.includes('--retire-legacy')){
    const baseline=JSON.parse(await fs.readFile(path.join(OUT,'baseline/manifest.json'),'utf8'));
    const currentPaths=new Set(metadata.flatMap(a=>[a.source,a.published]));
    const productRoot=path.join(ROOT,'ambiente_fonte');
    const consumers=[path.join(ROOT,'README.md'),...(await fs.readdir(productRoot,{recursive:true})).filter(p=>p.endsWith('.md')).map(p=>path.join(productRoot,p))];
    const consumerTexts=await Promise.all(consumers.map(async file=>({file,body:await fs.readFile(file,'utf8')})));
    const retired=[];
    for(const a of baseline.assets) for(const f of a.files){
      const rel=f.path.replace(/^baseline\//,'');if(currentPaths.has(rel))continue;
      const target=path.resolve(ASSET,rel);
      if(!target.startsWith(path.resolve(ASSET)+path.sep)||!/^readmes\/[a-z]+\/(sources|png)\/[^/]+\.(svg|png)$/.test(rel))throw new Error('Unsafe retirement target');
      const ref=consumerTexts.find(c=>c.body.includes(rel));
      if(ref)throw new Error(`Legacy asset still referenced in ${path.relative(ROOT,ref.file)}: ${rel}`);
      const frozen=await fs.readFile(path.join(OUT,f.path));if(sha(frozen)!==f.sha256)throw new Error('Baseline missing or altered');
      try{const active=await fs.readFile(target);if(sha(active)!==f.sha256)throw new Error(`Preserve independently modified legacy asset ${rel}`);await fs.unlink(target);retired.push(rel);}catch(e){if(e.code!=='ENOENT')throw e;}
    }
    const receipt=path.join(ROOT,'.artifacts/visual-v2/retired.json');
    const previous=await fs.readFile(receipt,'utf8').then(JSON.parse).catch(e=>{if(e.code==='ENOENT')return {retired:[]};throw e;});
    await write(receipt,JSON.stringify({baseline: 'sprint_0/baseline',retired:[...new Set([...previous.retired,...retired])]},null,2)+'\n');
  }
}
console.log(JSON.stringify({family,produced,complete_manifest:metadata.length===contracts.length},null,2));
