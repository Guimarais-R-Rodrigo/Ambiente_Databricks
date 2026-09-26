import fs from 'node:fs/promises';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import sharp from 'sharp';
import {ROOT,OUT,ASSET,TOOL,tokens,readYaml,sha,write} from './lib.mjs';

const m=JSON.parse(await fs.readFile(path.join(OUT,'manifest.json'),'utf8'));
const contracts=(await readYaml(path.join(ASSET,'specs/visual_contracts.yaml'))).contracts;
const errors=[],warnings=[],checks=[];
function check(ok,message){checks.push({pass:!!ok,message});if(!ok)errors.push(message);}
const lum=c=>{const v=c.slice(1).match(/../g).map(h=>parseInt(h,16)/255).map(n=>n<=.04045?n/12.92:((n+.055)/1.055)**2.4);return v[0]*.2126+v[1]*.7152+v[2]*.0722;};
const contrast=(a,b)=>(Math.max(lum(a),lum(b))+.05)/(Math.min(lum(a),lum(b))+.05);
check(contracts.length===21,'21 contratos semânticos');
check(new Set(contracts.map(c=>c.id)).size===21,'IDs únicos');
check(contracts.filter(c=>c.prototype&&c.signature).length===5,'5 assinaturas em protótipo');
check(m.assets.length===5,'5 ativos renderizados');
for(const c of contracts){
  for(const key of ['owner_readme','section','question','message','archetype','semantic_scope','non_goals','fact_sources','alt','caption','text_equivalent_anchor','render_targets'])check(!!c[key]?.length,`${c.id}: contrato ${key}`);
  for(const src of c.fact_sources)check(await fs.stat(path.join(ROOT,src)).then(()=>true).catch(()=>false),`${c.id}: fonte ${src}`);
  const owner=await fs.readFile(path.join(ROOT,c.owner_readme),'utf8');
  check(owner.includes(`id="${c.text_equivalent_anchor}"`),`${c.id}: âncora explícita existente`);
}
for(const i of m.inputs)check(sha(await fs.readFile(path.join(ROOT,i.path)))===i.sha256,`hash de entrada: ${i.path}`);
for(const i of m.dependencies)check(sha(await fs.readFile(path.join(TOOL,'node_modules',i.path)))===i.sha256,`hash de dependência: ${i.path}`);
const measurements=[];
for(const a of m.assets)for(const v of a.variants){
  const name=`${a.id}/${v.mode}`,png=await fs.readFile(path.join(OUT,v.png)),svg=await fs.readFile(path.join(OUT,v.svg));
  check(sha(png)===v.png_sha256,`${name}: hash PNG`);check(sha(svg)===v.svg_sha256,`${name}: hash SVG`);
  const meta=await sharp(png).metadata();check(meta.width===v.width&&meta.height===v.height,`${name}: dimensões`);
  check(!/<text\b/.test(svg.toString()),`${name}: fontes convertidas em paths`);
  check(!/https?:\/\//.test(svg.toString().replaceAll('http://www.w3.org/2000/svg','').replaceAll('http://www.w3.org/1999/xlink','')),`${name}: sem dependências remotas`);
  const essential=v.texts.filter(t=>t.essential);
  const minimum=Math.min(...essential.map(t=>t.size*v.minimum_display_width/v.width));
  check(minimum>=tokens.typography.minimum_effective_body_px,`${name}: corpo mínimo efetivo ${minimum.toFixed(2)} px`);
  let minContrast=Infinity;
  for(const t of v.texts){
    check(t.x>=0&&t.y>=0&&t.x+t.width<=v.width&&t.y+t.height<=v.height,`${name}: bounds de «${t.text}»`);
    const cr=Math.min(...[tokens.colors.background,tokens.colors.background_elevated,tokens.colors.panel,tokens.colors.panel_high].map(bg=>contrast(t.color,bg)));
    if(t.essential)minContrast=Math.min(minContrast,cr);
    check(cr>=(t.essential?4.5:3),`${name}: contraste conservador ${cr.toFixed(2)} de «${t.text}»`);
  }
  for(let i=0;i<v.texts.length;i++)for(let j=i+1;j<v.texts.length;j++){
    const a=v.texts[i],b=v.texts[j];
    const ix=Math.min(a.x+a.width,b.x+b.width)-Math.max(a.x,b.x),iy=Math.min(a.y+a.height,b.y+b.height)-Math.max(a.y,b.y);
    // Text boxes are conservative em bounds; > 4px of vertical overlap is actionable.
    check(!(ix>2&&iy>4),`${name}: separação de textos ${i}/${j}`);
  }
  measurements.push({id:a.id,mode:v.mode,minimum_display_width:v.minimum_display_width,minimum_effective_body_px:minimum,minimum_conservative_contrast:minContrast});
}
const baseline=JSON.parse(await fs.readFile(path.join(OUT,'baseline/manifest.json'),'utf8'));
check(baseline.assets.length===22,'baseline de 22 ativos');
for(const a of baseline.assets)for(const f of a.files){
  check(sha(await fs.readFile(path.join(OUT,f.path)))===f.sha256,`baseline íntegro: ${f.path}`);
  const rel=f.path.replace(/^baseline\//,'');
  check(sha(await fs.readFile(path.join(ASSET,rel)))===f.sha256,`ativo de produção preservado: ${rel}`);
}
const readmes=['README.md',...['','hub_snippets/','hub_scripts/','skills/','hub_prompts/'].map(r=>`ambiente_fonte/.assistant/${r}README.md`)];
for(const f of readmes){const previous=execFileSync('git',['show',`${m.baseline_commit}:${f}`],{cwd:ROOT});check(sha(previous)===sha(await fs.readFile(path.join(ROOT,f))),`README ativo preservado: ${f}`);}
for(const file of ['README_SPRINT_0.md','README_COMPARACOES.md','CONTRATOS_21_FIGURAS.md','SISTEMA_VISUAL.md','ESTADO_SPRINT_0.md']){
  let data;try{data=await fs.readFile(path.join(OUT,file),'utf8');}catch{check(false,`documento presente: ${file}`);continue;}
  check(!/ADR[- ]?0*\d+/i.test(data),`${file}: sem códigos de decisões nos documentos de leitura`);
  for(const match of data.matchAll(/!?\[[^\]]*\]\(([^)]+)\)/g)){
    const link=match[1];if(/^(https?:|#)/.test(link))continue;
    check(await fs.stat(path.resolve(OUT,link.split('#')[0])).then(()=>true).catch(()=>false),`${file}: link ${link}`);
  }
}
warnings.push('A análise geométrica cobre textos, não todas as colisões de curvas, ícones ou silhuetas; revisão visual humana continua necessária.');
warnings.push('Legibilidade em compartilhamento de tela é critério de aceite humano, não resultado de teste com participantes.');
const report={status:errors.length?'failed':'passed',checks:checks.length,failures:errors,warnings,measurements};
await write(path.join(OUT,'qa/validation.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report,null,2));
process.exitCode=errors.length?1:0;
