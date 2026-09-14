import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import sharp from 'sharp';
import YAML from 'yaml';

const TOOL=path.dirname(fileURLToPath(import.meta.url));
const ROOT=path.resolve(TOOL,'../..');
const ASSET=path.join(ROOT,'ambiente_fonte/.assistant/hub_readmes_visual_assets');
const ASSISTANT=path.join(ROOT,'ambiente_fonte/.assistant');
const ARTIFACT_ROOT=path.join(ROOT,'.artifacts/visual-v2/theme-variants');
const GENERATOR_VERSION=1;
const FAMILY_GROUPS={top:['raiz','assistant'],snippets:['snippets'],scripts:['scripts'],skills:['skills'],prompts:['prompts']};
const COLOR_KEYS=['background','background_elevated','panel','panel_high','line','text','muted','quiet','hub_custom','gradient_end','atlas_core','dossier_back','dossier_middle','dossier_fold','databricks_native','human_decision','result_evidence','supporting_method','danger'];
const TYPO_KEYS=['presentation_title_px','readme_heading_px','module_title_px','body_px','small_px'];
const GEOMETRY_KEYS=['corner_radius','connector_width','border_width','safe_margin','glow_opacity'];

function arg(name, fallback=null){
  const i=process.argv.indexOf(name);return i<0?fallback:process.argv[i+1];
}
function flag(name){return process.argv.includes(name);}
function sha(value){return crypto.createHash('sha256').update(value).digest('hex');}
function assert(condition,message){if(!condition)throw new Error(message);}
function rel(p,base=ROOT){return path.relative(base,p).split(path.sep).join('/');}
function safeThemeId(value){
  assert(typeof value==='string'&&/^[a-z0-9][a-z0-9._-]{0,127}$/.test(value),'THEME_ID_FORMAT: use um theme_id canônico.');
  return value;
}
function generatedAt(){
  const raw=process.env.SOURCE_DATE_EPOCH;
  assert(raw!==undefined&&/^[0-9]{1,12}$/.test(raw),'SOURCE_DATE_EPOCH_REQUIRED: informe epoch inteiro para geração reproduzível.');
  const seconds=Number(raw);const date=new Date(seconds*1000);
  assert(Number.isFinite(date.getTime()),'SOURCE_DATE_EPOCH_INVALID: epoch inválido.');
  return {epoch:seconds,iso:date.toISOString()};
}
function outputRoot(theme, explicit){
  const defaultPath=path.join(ARTIFACT_ROOT,theme.theme_id,theme.fingerprint.slice(0,16));
  const target=explicit?path.resolve(ROOT,explicit):defaultPath;
  const artifactBase=path.resolve(ROOT,'.artifacts')+path.sep;
  assert(target.startsWith(artifactBase),'OUTPUT_SCOPE: a saída precisa ficar em .artifacts/.');
  assert(!target.startsWith(path.resolve(ASSET)+path.sep),'OUTPUT_ACTIVE_FORBIDDEN: a V06 não sobrescreve o pacote ativo.');
  return target;
}
function bridge(themeId){
  const python=process.env.PYTHON||process.env.PYTHON3||'python';
  let stdout;
  try{
    stdout=execFileSync(python,[path.join(TOOL,'theme_bridge.py'),'--theme-id',themeId,'--context','readme'],{cwd:ROOT,encoding:'utf8',stdio:['ignore','pipe','pipe']});
  }catch(error){
    const detail=error?.stderr?String(error.stderr).trim():'falha no resolvedor';
    throw new Error(`THEME_RESOLVE_FAILED: ${detail}`);
  }
  let result;try{result=JSON.parse(stdout);}catch{throw new Error('THEME_DERIVATIVE_JSON: saída do resolvedor não é JSON.');}
  assert(result.derivative_version===1&&result.theme_id===themeId&&result.context==='readme','THEME_DERIVATIVE_CONTRACT: derivado incompatível.');
  return result;
}
function applyTheme(lib,theme){
  const values=theme.tokens;
  assert(values&&typeof values==='object','THEME_TOKENS: tokens ausentes.');
  assert(values['font.family']==='editorial_inter','THEME_FONT_UNSUPPORTED: compositor v2 só aceita a fonte editorial_inter licenciada.');
  for(const key of COLOR_KEYS){
    const value=values[`editorial.${key}`];
    assert(typeof value==='string'&&/^#[0-9A-F]{6}$/.test(value),`THEME_COLOR_MISSING: editorial.${key}`);
    lib.C[key]=value;lib.tokens.colors[key]=value;
  }
  for(const key of TYPO_KEYS){
    const value=values[`typography.${key}`];
    assert(Number.isFinite(value),`THEME_TYPOGRAPHY_MISSING: typography.${key}`);
    lib.tokens.typography[key]=value;
  }
  for(const key of GEOMETRY_KEYS){
    const value=values[`geometry.${key}`];
    assert(Number.isFinite(value),`THEME_GEOMETRY_MISSING: geometry.${key}`);
    lib.tokens.geometry[key]=value;
  }
  // canvas.width_px/height_px são metadados do contexto do tema. O contrato de
  // cada figura continua escolhendo readme_wide/readme_standard; V06 não muda
  // dimensões aprovadas silenciosamente.
}
async function readYaml(file){return YAML.parse(await fs.readFile(file,'utf8'));}
async function write(file,data){await fs.mkdir(path.dirname(file),{recursive:true});await fs.writeFile(file,data);}
async function verifiedFrozen(theme){
  const contract=JSON.parse(await fs.readFile(path.join(ASSISTANT,'hub_padroes/identidade_visual/assets.json'),'utf8'));
  const items=contract.sets?.[theme.asset_set_id];
  assert(Array.isArray(items),'ASSET_SET_UNKNOWN: conjunto de assets não existe.');
  const result=[];
  for(const item of items){
    assert(typeof item.path==='string'&&/^[a-zA-Z0-9_./-]+$/.test(item.path)&&!item.path.split('/').includes('..'),'ASSET_PATH: caminho congelado inválido.');
    const full=path.resolve(ASSISTANT,item.path);
    assert(full.startsWith(path.resolve(ASSISTANT)+path.sep),'ASSET_SCOPE: asset congelado saiu de .assistant.');
    const data=await fs.readFile(full);const actual=sha(data);
    assert(actual===item.sha256,`ASSET_HASH: bytes congelados divergiram em ${item.path}`);
    result.push({path:item.path,sha256:actual,classification:'frozen',action:'preserve_exact_bytes'});
  }
  return result;
}
async function loadRenderers(selected){
  const map={};
  for(const [moduleName,families] of [['top',['raiz','assistant']],['snippets',['snippets']],['scripts',['scripts']],['methods',['skills','prompts']]]){
    if(selected.some(f=>families.includes(f)))Object.assign(map,(await import(`./archetypes/${moduleName}.mjs`)).renderers);
  }
  return map;
}
function manifestFile(root){return path.join(root,'manifest.yaml');}
async function verifyManifest(root,theme){
  const manifest=await readYaml(manifestFile(root));
  assert(manifest?.version===1&&manifest?.generator_version===GENERATOR_VERSION,'MANIFEST_VERSION: manifesto incompatível.');
  assert(manifest.theme?.theme_id===theme.theme_id&&manifest.theme?.fingerprint===theme.fingerprint,'MANIFEST_THEME: manifesto pertence a outro tema/revisão.');
  assert(manifest.status==='candidate_not_approved','MANIFEST_STATUS: V06 só verifica candidato não aprovado.');
  for(const frozen of manifest.frozen_assets||[]){
    const full=path.resolve(ASSISTANT,frozen.path);assert(full.startsWith(path.resolve(ASSISTANT)+path.sep),'VERIFY_SCOPE: caminho congelado inválido.');
    assert(sha(await fs.readFile(full))===frozen.sha256,`VERIFY_FROZEN_HASH: ${frozen.path}`);
  }
  for(const asset of manifest.assets||[]){
    for(const [kind,fileKey,hashKey] of [['svg','svg','svg_sha256'],['png','png','sha256']]){
      const relative=asset.files?.[fileKey];assert(typeof relative==='string'&&!relative.includes('..'),'VERIFY_PATH: saída relativa inválida.');
      const full=path.resolve(root,relative);assert(full.startsWith(path.resolve(root)+path.sep),'VERIFY_SCOPE: saída escapou do diretório.');
      const data=await fs.readFile(full);assert(sha(data)===asset[hashKey],`VERIFY_HASH: ${asset.id} ${kind}`);
      if(kind==='png'){
        const meta=await sharp(data).metadata();assert(meta.width===asset.width&&meta.height===asset.height,`VERIFY_DIMENSIONS: ${asset.id}`);
      }
    }
    assert(['frozen_approved_signature','parametric_equivalent','variant_review_required'].includes(asset.classification),'VERIFY_CLASSIFICATION: classificação desconhecida.');
  }
  return {theme_id:theme.theme_id,fingerprint:theme.fingerprint,assets:manifest.assets.length,frozen_assets:manifest.frozen_assets.length,verified:true};
}

const themeId=safeThemeId(arg('--theme-id'));
const family=arg('--family','all');
assert(family==='all'||Object.hasOwn(FAMILY_GROUPS,family),'FAMILY: use top|snippets|scripts|skills|prompts|all.');
const theme=bridge(themeId);
const root=outputRoot(theme,arg('--output'));
if(flag('--verify')){
  console.log(JSON.stringify(await verifyManifest(root,theme),null,2));
  process.exit(0);
}
const time=generatedAt();
const selected=family==='all'?Object.values(FAMILY_GROUPS).flat():FAMILY_GROUPS[family];
const lib=await import('./lib.mjs');
applyTheme(lib,theme);
const contracts=(await readYaml(path.join(ASSET,'specs/visual_contracts.yaml'))).contracts;
const approved=JSON.parse(await fs.readFile(path.join(ASSET,'specs/approved_signatures.json'),'utf8'));
const renderers=await loadRenderers(selected);
const frozenAssets=await verifiedFrozen(theme);
await fs.rm(root,{recursive:true,force:true});
const records=[];
for(const c of contracts.filter(c=>selected.includes(c.id.split('.')[0]))){
  const [group,name]=c.id.split('.');
  const activeSource=`readmes/${group}/sources/${name}.svg`;
  const activePng=`readmes/${group}/png/${name}.png`;
  let svg,png,dimensions;
  if(c.prototype){
    const v=approved.assets.find(a=>a.id===c.id)?.variants.find(v=>v.mode==='readme');
    assert(v,`APPROVED_SIGNATURE_ABSENT: ${c.id}`);
    svg=await fs.readFile(path.join(ASSET,v.svg));
    png=await sharp(svg).png({compressionLevel:9}).toBuffer();
    assert(sha(svg)===v.svg_sha256&&sha(png)===v.png_sha256,`APPROVED_SIGNATURE_CHANGED: ${c.id}`);
    dimensions={width:v.width,height:v.height,minimum_display_width:v.minimum_display_width};
  }else{
    const preset=lib.tokens.presets[c.render_targets[0]];
    assert(preset&&renderers[c.id],`RENDERER_CONTRACT: renderer/preset ausente para ${c.id}`);
    const canvas=lib.newCanvas(preset.width,preset.height,c.alt);
    await renderers[c.id](canvas,c,'readme');
    svg=Buffer.from(canvas.draw.svg()+'\n');
    png=await sharp(svg).png({compressionLevel:9}).toBuffer();
    dimensions=preset;
  }
  const svgRel=`readmes/${group}/sources/${name}.svg`,pngRel=`readmes/${group}/png/${name}.png`;
  await write(path.join(root,svgRel),svg);await write(path.join(root,pngRel),png);
  const activeBytes=await fs.readFile(path.join(ASSET,activePng));
  const activeSha=sha(activeBytes),candidateSha=sha(png);
  let classification,action;
  if(c.prototype){
    assert(candidateSha===activeSha,`FROZEN_ACTIVE_DIVERGENCE: ${c.id}`);
    classification='frozen_approved_signature';action='preserve_exact_bytes';
  }else if(candidateSha===activeSha){
    classification='parametric_equivalent';action='active_bytes_unchanged';
  }else{
    classification='variant_review_required';action='create_new_revision_before_promotion';
  }
  const meta=await sharp(png).metadata();
  assert(meta.width===dimensions.width&&meta.height===dimensions.height,`RENDER_DIMENSIONS: ${c.id}`);
  records.push({id:c.id,type:'editorial_figure',variant:'readme',classification,action,theme_id:theme.theme_id,
    theme_version:theme.theme_version,width:meta.width,height:meta.height,minimum_display_width:dimensions.minimum_display_width,
    intended_use:{owner_readme:c.owner_readme,question:c.question,caption:c.caption},
    active:{png:activePng,source:activeSource,sha256:activeSha},files:{svg:svgRel,png:pngRel},sha256:candidateSha,svg_sha256:sha(svg)});
}
const manifest={version:1,generator_version:GENERATOR_VERSION,status:'candidate_not_approved',generated_by:'tools/readme_visuals/theme_assets.mjs',
  generated_at:time.iso,source_date_epoch:time.epoch,family,theme:{theme_id:theme.theme_id,theme_version:theme.theme_version,identity_id:theme.identity_id,
    context:theme.context,mode:theme.mode,asset_set_id:theme.asset_set_id,source:theme.source,raw_sha256:theme.raw_sha256,content_sha256:theme.content_sha256,
    schema_sha256:theme.schema_sha256,asset_manifest_sha256:theme.asset_manifest_sha256,fingerprint:theme.fingerprint},
  policy:{active_package_mutated:false,frozen_assets_recolored:false,parametric_changes_require_new_revision:true,approval_or_publication_performed:false},
  frozen_assets:frozenAssets,assets:records};
const yaml=YAML.stringify(manifest,{lineWidth:120});
await write(manifestFile(root),yaml);
await write(path.join(root,'manifest.sha256'),sha(Buffer.from(yaml))+'  manifest.yaml\n');
console.log(JSON.stringify({theme_id:theme.theme_id,fingerprint:theme.fingerprint,family,output:rel(root),assets:records.length,
  frozen_assets:frozenAssets.length,classifications:Object.fromEntries([...new Set(records.map(r=>r.classification))].sort().map(k=>[k,records.filter(r=>r.classification===k).length])),
  status:'candidate_not_approved'},null,2));
