import fs from 'node:fs/promises';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import sharp from 'sharp';
import YAML from 'yaml';
import { ROOT, ASSET, OUT, TOOL, tokens, readYaml, sha, write, newCanvas } from './lib.mjs';
import { renderers } from './archetypes/signatures.mjs';

const contracts=await readYaml(path.join(ASSET,'specs/visual_contracts.yaml'));
const previous=await readYaml(path.join(ASSET,'manifest.yaml'));
if(previous.version>=2) throw new Error('Sprint 0 is frozen. Use production.mjs --family all for the active v2 package.');
const baselineCommit='f5461d8';
const titles={
  'raiz.01_mapa_ecossistema':'01 — Ecossistema',
  'assistant.02_arquitetura_de_uso':'02 — Contexto e execução',
  'scripts.02_catalogo_diagnosticos':'03 — Bancada dos Hub Scripts',
  'skills.03_anatomia_skill':'04 — Anatomia de uma Agent Skill',
  'prompts.03_anatomia_briefing':'05 — Blueprint do briefing'
};
const baselineIds={
  'skills.03_anatomia_skill':'skills.03_camadas_de_uma_skill',
  'prompts.03_anatomia_briefing':'prompts.03_anatomia_do_briefing'
};

// Baseline is frozen from the known Git commit, not from a subsequently edited PNG.
const baseline=[];
for(const item of previous.assets){
  const record={id:item.id,files:[]};
  for(const rel of [item.source,item.published]){
    const repoPath=`ambiente_databricks/.assistant/hub_readmes_visual_assets/${rel}`;
    const bytes=execFileSync('git',['show',`${baselineCommit}:${repoPath}`],{cwd:ROOT,maxBuffer:20*1024*1024});
    const dest=path.join(OUT,'baseline',rel);
    let exists;try{exists=await fs.readFile(dest);}catch(e){if(e.code!=='ENOENT')throw e;}
    if(exists&&sha(exists)!==sha(bytes))throw new Error(`Frozen baseline changed: ${rel}`);
    if(!exists)await write(dest,bytes);
    record.files.push({path:`baseline/${rel}`,sha256:sha(bytes)});
  }
  baseline.push(record);
}
await write(path.join(OUT,'baseline/manifest.json'),JSON.stringify({commit:baselineCommit,assets:baseline},null,2)+'\n');

const outputs=[];
for(const c of contracts.contracts.filter(c=>c.prototype)){
  const name=c.id.replace('.','_');
  const base=previous.assets.find(a=>a.id===(baselineIds[c.id]||c.id));
  const record={id:c.id,title:titles[c.id],alt:c.alt,caption:c.caption,question:c.question,archetype:c.archetype,baseline:`baseline/${base.published}`,variants:[]};
  for(const mode of ['readme','presentation']){
    const preset=tokens.presets[mode==='readme'?c.render_targets[0]:'presentation_hero'];
    const state=newCanvas(preset.width,preset.height,c.alt);
    const before=state.texts.length;
    await renderers[c.id](state,c,mode);
    const {dx,dy,scale}=state.contentTransform;
    // Root chrome lies outside the transformed group. Track every label at its final coordinates.
    const chromeCount=mode==='presentation'?4:0;
    state.texts=state.texts.map((t,i)=>i<chromeCount?t:{...t,x:dx+t.x*scale,y:dy+t.y*scale,width:t.width*scale,height:t.height*scale,size:t.size*scale});
    const svg=state.draw.svg();
    const svgRel=`renders/${mode}/${name}.svg`,pngRel=`renders/${mode}/${name}.png`;
    await write(path.join(OUT,svgRel),svg+'\n');
    const png=await sharp(Buffer.from(svg)).png({compressionLevel:9}).toBuffer();
    await write(path.join(OUT,pngRel),png);
    record.variants.push({mode,width:preset.width,height:preset.height,minimum_display_width:preset.minimum_display_width,svg:svgRel,png:pngRel,svg_sha256:sha(Buffer.from(svg+'\n')),png_sha256:sha(png),texts:state.texts,icons:[...new Set(state.icons)]});
  }
  outputs.push(record);
}
const sourcePaths=['specs/visual_contracts.yaml','specs/prototype_copy.yaml','visual_system/tokens.yaml','visual_system/semantic_roles.yaml','visual_system/archetypes.yaml'];
const inputs=[];
for(const rel of sourcePaths){
  const bytes=await fs.readFile(path.join(ASSET,rel));
  await write(path.join(OUT,'contracts',rel),bytes);
  inputs.push({path:`ambiente_databricks/.assistant/hub_readmes_visual_assets/${rel}`,sha256:sha(bytes)});
}
for(const rel of ['tools/readme_visuals/lib.mjs','tools/readme_visuals/render.mjs','tools/readme_visuals/archetypes/signatures.mjs','tools/readme_visuals/package.json','tools/readme_visuals/pnpm-lock.yaml','tools/readme_visuals/.node-version','tools/readme_visuals/document.mjs','tools/readme_visuals/contact_sheet.mjs','tools/readme_visuals/scale_samples.mjs','tools/readme_visuals/validate.mjs']) {
  inputs.push({path:rel,sha256:sha(await fs.readFile(path.join(ROOT,rel)))});
}
const factFiles=new Set();
for(const c of contracts.contracts)for(const rel of c.fact_sources) {
  const file=path.join(ROOT,rel);
  if((await fs.stat(file)).isFile())factFiles.add(rel);
  else for(const name of await fs.readdir(file,{recursive:true})) {
    if(/\.(py|md)$/.test(name)&&!name.includes('__pycache__'))factFiles.add(`${rel}/${name.replaceAll('\\','/')}`);
  }
}
for(const rel of [...factFiles].sort())inputs.push({path:rel,kind:'fact_source',sha256:sha(await fs.readFile(path.join(ROOT,rel)))});
const dependencies=[];
for(const weight of [400,600,700,800]) {
  const rel=`@fontsource/inter/files/inter-latin-${weight}-normal.woff`;
  dependencies.push({path:rel,sha256:sha(await fs.readFile(path.join(TOOL,'node_modules',rel)))});
}
for(const name of new Set(outputs.flatMap(a=>a.variants.flatMap(v=>v.icons)))) {
  const rel=`lucide-static/icons/${name}.svg`;
  dependencies.push({path:rel,sha256:sha(await fs.readFile(path.join(TOOL,'node_modules',rel)))});
}
const manifest={schema_version:1,status:'awaiting_user_visual_review',baseline_commit:baselineCommit,generated_by:'tools/readme_visuals/render.mjs',node:process.version,sharp:sharp.versions,inputs,dependencies,assets:outputs};
await write(path.join(OUT,'manifest.json'),JSON.stringify(manifest,null,2)+'\n');
await write(path.join(OUT,'licenses/Inter-OFL.txt'),await fs.readFile(path.join(TOOL,'node_modules/@fontsource/inter/LICENSE')));
await write(path.join(OUT,'licenses/Lucide-ISC.txt'),await fs.readFile(path.join(TOOL,'node_modules/lucide-static/LICENSE')));

const intro='# Sprint 0 — Cinco protótipos para avaliação\n\nEsta galeria reúne as cinco figuras assinatura da proposta visual. As figuras foram geradas de forma reproduzível, com tipografia Inter e ícones Lucide licenciados.\n\nOs READMEs ativos continuam como referência. A aprovação desta galeria congela a direção visual antes das sprints documentais.\n\n';
let md=intro;
for(const item of outputs){
  const v=item.variants[0],hero=item.variants[1];
  md+=`## ${item.title}\n\n${item.question}\n\n![${item.alt}](${v.png})\n\n${item.caption}\n\n[Versão de apresentação](${hero.png}) · [Comparação com o baseline](comparisons/${item.id.replace('.','_')}.png)\n\n`;
}
md+='## Como avaliar\n\nCompare clareza, estética, leitura dos rótulos e diferença entre os cinco tipos de composição. Abra o notebook visualizador para navegar no Databricks.\n\n- [Comparações individuais](README_COMPARACOES.md)\n- [Contratos das 21 figuras](CONTRATOS_21_FIGURAS.md)\n- [Sistema visual candidato](SISTEMA_VISUAL.md)\n- [Estado da Sprint 0](ESTADO_SPRINT_0.md)\n';
await write(path.join(OUT,'README_SPRINT_0.md'),md);
// Databricks notebook-relative navigation differs from Markdown image paths.
// Keep the .md portable; adapt only non-image links in the notebook companion.
const notebookMd=md.replace(/(?<!!)\[([^\]]+)\]\((?!https?:|#)([^)]+)\)/g,(_all,label,target)=>`[${label}]($./${target})`);
const cells=notebookMd.split(/(?=^## )/m);
const notebook='# Databricks notebook source\n'+cells.map(cell=>'# MAGIC %md\n'+cell.trimEnd().split('\n').map(l=>'# MAGIC'+(l?' '+l:'')).join('\n')).join('\n\n# COMMAND ----------\n\n')+'\n';
await write(path.join(OUT,'VISUALIZADOR_SPRINT_0.py'),notebook);
console.log(`Rendered ${outputs.length} prototypes, ${outputs.length*2} PNG/SVG pairs. Baseline: ${baseline.length} frozen assets.`);
