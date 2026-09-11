import fs from 'node:fs/promises';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import sharp from 'sharp';
import {ROOT,OUT,ASSET,TOOL,tokens,readYaml,sha,write} from './lib.mjs';

const family=process.argv[process.argv.indexOf('--family')+1];
const partial=['top','snippets','scripts','skills','prompts'].includes(family);
const selected=family==='top'?['raiz','assistant']:partial?[family]:null;
const contracts=(await readYaml(path.join(ASSET,'specs/visual_contracts.yaml'))).contracts;
const errors=[],checks=[],measurements=[];
function check(ok,msg){checks.push({pass:!!ok,message:msg});if(!ok)errors.push(msg);}
const lum=c=>{const v=c.slice(1).match(/../g).map(h=>parseInt(h,16)/255).map(n=>n<=.04045?n/12.92:((n+.055)/1.055)**2.4);return v[0]*.2126+v[1]*.7152+v[2]*.0722;};
const contrast=(a,b)=>(Math.max(lum(a),lum(b))+.05)/(Math.min(lum(a),lum(b))+.05);
check(contracts.length===21 && new Set(contracts.map(c=>c.id)).size===21,'21 contratos únicos');
const readmes=['README.md',...['','hub_snippets/','hub_scripts/','skills/','hub_prompts/'].map(p=>`ambiente_fonte/.assistant/${p}README.md`)];
const editorial=JSON.parse(await fs.readFile(path.join(ASSET,'specs/editorial_corrections.json'),'utf8'));
for(const c of editorial.corrections)check(sha(await fs.readFile(path.join(ROOT,c.source)))===c.source_sha256,`Fonte da correção factual: ${c.source}`);
for(const c of contracts.filter(c=>!selected||selected.includes(c.id.split('.')[0]))){
  const m=JSON.parse(await fs.readFile(path.join(ASSET,'qa/figures',`${c.id}.json`),'utf8'));
  const png=await fs.readFile(path.join(ASSET,m.published)),svg=await fs.readFile(path.join(ASSET,m.source));
  check(sha(png)===m.sha256,`${c.id}: hash PNG`);check(sha(svg)===m.svg_sha256,`${c.id}: hash SVG`);
  const meta=await sharp(png).metadata();check(meta.width===m.width&&meta.height===m.height,`${c.id}: dimensões`);
  check(!/<text\b/.test(svg.toString()),`${c.id}: Inter em paths`);
  check(!/https?:\/\//.test(svg.toString().replaceAll('http://www.w3.org/2000/svg','').replaceAll('http://www.w3.org/1999/xlink','')),`${c.id}: sem dependências remotas`);
  let min=Infinity,minContrast=Infinity;
  for(const t of m.texts){
    check(t.x>=0&&t.y>=0&&t.x+t.width<=m.width&&t.y+t.height<=m.height,`${c.id}: bounds ${t.text}`);
    const cr=Math.min(...[tokens.colors.background,tokens.colors.background_elevated,tokens.colors.panel,tokens.colors.panel_high].map(bg=>contrast(t.color,bg)));
    check(cr>=(t.essential?4.5:3),`${c.id}: contraste ${t.text} (${cr.toFixed(2)})`);
    if(t.essential){min=Math.min(min,t.size*720/m.width);minContrast=Math.min(minContrast,cr);}
  }
  check(min>=14,`${c.id}: fonte essencial >=14px a720 (atual ${min.toFixed(2)})`);
  for(let i=0;i<m.texts.length;i++)for(let j=i+1;j<m.texts.length;j++){
    const a=m.texts[i],b=m.texts[j],ix=Math.min(a.x+a.width,b.x+b.width)-Math.max(a.x,b.x),iy=Math.min(a.y+a.height,b.y+b.height)-Math.max(a.y,b.y);
    check(!(ix>2&&iy>4),`${c.id}: colisão ${i}/${j}: ${a.text} / ${b.text}`);
  }
  if(!process.argv.includes('--figures-only')){
    const md=await fs.readFile(path.join(ROOT,c.owner_readme),'utf8');
    check(md.includes(`id="${c.planned_ascii_anchor}"`),`${c.id}: âncora de integração`);
    check(md.includes(m.published),`${c.id}: imagem no consumidor canônico`);
  }
  if(c.prototype){const a=JSON.parse(await fs.readFile(path.join(ASSET,'specs/approved_signatures.json'),'utf8')).assets.find(a=>a.id===c.id).variants[0];check(m.sha256===a.png_sha256,`${c.id}: assinatura aprovada intacta`);}
  measurements.push({id:c.id,min_effective_px:min,min_contrast:minContrast});
}
if(!partial){
  const manifest=await readYaml(path.join(ASSET,'manifest.yaml'));
  check(manifest.version===2&&manifest.assets.length===21&&manifest.headers.length===2,'manifesto ativo completo');
  for(const i of manifest.inputs)check(sha(await fs.readFile(path.join(ROOT,i.path)))===i.sha256,`entrada atual: ${i.path}`);
  const headerApproval=JSON.parse(await fs.readFile(path.join(ASSET,'specs/approved_headers.json'),'utf8'));
  for(const h of manifest.headers){check(sha(await fs.readFile(path.join(ASSET,h.path)))===h.sha256,`${h.id}: hash`);check(h.sha256===headerApproval.headers.find(a=>a.id===h.id).sha256,`${h.id}: aprovado intacto`);}
  let diagramOccurrences=0,headerOccurrences=0;
  const referencedDiagrams=new Set();
  for(const file of readmes){
    const md=await fs.readFile(path.join(ROOT,file),'utf8');
    const baseline=execFileSync('git',['show',`f5461d8:${file}`],{cwd:ROOT,maxBuffer:10*1024*1024}).toString('utf8');
    const heads=s=>[...s.matchAll(/^#{1,6} .+$/gm)].map(m=>m[0]);
    let pos=-1;for(const h of heads(baseline)){const i=heads(md).indexOf(h,pos+1);check(i>=0,`${file}: preservar tópico ${h}`);pos=i;}
    const blocks=s=>[...s.matchAll(/```(?:python|sql)\r?\n([\s\S]*?)```/g)].map(m=>m[1].replaceAll('\r',''));
    for(const b of blocks(baseline)){
      const correction=editorial.corrections.find(c=>c.file===file&&c.old_sha256===sha(b));
      const valid=correction?blocks(md).some(n=>sha(n)===correction.new_sha256):blocks(md).includes(b);
      check(valid,`${file}: ${correction?'correção factual exata e rastreada':'exemplo Python/SQL preservado'}`);
    }
    check(!/ADR[- ]?0*\d+/i.test(md),`${file}: sem códigos de decisões`);
    check(!/```mermaid/.test(md),`${file}: PNG em vez de Mermaid`);
    check(md.includes('headers/png/cabecalho_crm.png'),`${file}: header compartilhado`);
    check(md.startsWith('![CRM — Missão Modelos Analíticos CRM]('),`${file}: header aprovado antes do título`);
    for(const m of md.matchAll(/!\[[^\]]*\]\(([^)]+)\)/g)){
      if(m[1].includes('headers/png/cabecalho_crm.png')) headerOccurrences++;
      if(m[1].includes('hub_readmes_visual_assets/readmes/')){
        diagramOccurrences++;
        const rel=m[1].split('hub_readmes_visual_assets/')[1];referencedDiagrams.add(rel);
        const a=manifest.assets.find(a=>a.published===rel);
        check(!!a,`${file}: imagem consta no inventário: ${rel}`);
        if(a)check(m[0].startsWith(`![${a.alt}](`),`${file}: alt canônico: ${rel}`);
      }
    }
    const stripped=md.replace(/```[\s\S]*?```/g,'');
    for(const m of stripped.matchAll(/!?\[[^\]]*\]\(([^)]+)\)/g)){
      if(/^https?:/.test(m[1]))continue;
      const [rel,anchor]=m[1].split('#');const target=rel?path.resolve(path.dirname(path.join(ROOT,file)),rel):path.join(ROOT,file);
      check(await fs.stat(target).then(()=>true).catch(()=>false),`${file}: link ${m[1]}`);
      if(anchor&&!rel)check(md.includes(`id="${anchor}"`),`${file}: âncora local ${anchor}`);
    }
  }
  check(diagramOccurrences===23,'23 ocorrências de diagramas nos seis READMEs físicos');
  check(headerOccurrences===6,'6 ocorrências do único cabeçalho CRM');
  check(referencedDiagrams.size===21,'Todos os 21 diagramas ativos usados nos READMEs');
  // Runtime, skill definitions and prompt templates must remain byte-for-byte unchanged.
  const baseFiles=execFileSync('git',['ls-tree','-r','--name-only','f5461d8','ambiente_fonte'],{cwd:ROOT}).toString().trim().split('\n');
  for(const file of baseFiles.filter(f=>!readmes.includes(f)&&!f.includes('hub_readmes_visual_assets/'))){
    const old=execFileSync('git',['show',`f5461d8:${file}`],{cwd:ROOT,maxBuffer:10*1024*1024});
    check(sha(old)===sha(await fs.readFile(path.join(ROOT,file))),`contrato/runtime preservado: ${file}`);
  }
}
const report={status:errors.length?'failed':'passed',scope:partial?family:'all',checks:checks.length,failures:errors,measurements,
  limits:['A geometria automatizada não cobre todas as curvas e silhuetas; revisão visual independente complementa os checks.','Não é homologação de runtime nem teste conversacional da Genie Code.']};
await write(path.join(ASSET,'qa',partial?`sprint_${family}.json`:'validation.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report,null,2));process.exitCode=errors.length?1:0;
