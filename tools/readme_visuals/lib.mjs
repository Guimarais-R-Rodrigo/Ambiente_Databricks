import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { SVG, registerWindow } from '@svgdotjs/svg.js';
import { createSVGWindow } from 'svgdom';
import * as fontkit from 'fontkit';
import YAML from 'yaml';

export const TOOL = path.dirname(fileURLToPath(import.meta.url));
export const ROOT = path.resolve(TOOL, '../..');
export const ASSET = path.join(ROOT, 'ambiente_fonte/.assistant/hub_readmes_visual_assets');
export const OUT = path.join(ROOT, 'READMEs_refeitos/readmes_viasual_melhorado/sprint_0');
export const sha = b => crypto.createHash('sha256').update(b).digest('hex');
export const readYaml = async p => YAML.parse(await fs.readFile(p, 'utf8'));
export const tokens = await readYaml(path.join(ASSET, 'visual_system/tokens.yaml'));
export const C = tokens.colors;
export const {labels} = await readYaml(path.join(ASSET,'specs/prototype_copy.yaml'));
const fonts = {};
for (const weight of [400, 600, 700, 800]) {
  fonts[weight] = fontkit.create(await fs.readFile(path.join(TOOL, `node_modules/@fontsource/inter/files/inter-latin-${weight}-normal.woff`)));
}
export function measure(value, size = tokens.typography.body_px, weight = 400) {
  return fonts[weight].layout(String(value)).positions.reduce((s, p) => s + p.xAdvance, 0) * size / fonts[weight].unitsPerEm;
}
export async function write(p, content) {
  await fs.mkdir(path.dirname(p), { recursive: true });
  await fs.writeFile(p, content);
}
export function newCanvas(width, height, label) {
  const window = createSVGWindow();
  registerWindow(window, window.document);
  const draw = SVG(window.document.documentElement).size(width, height).viewbox(0, 0, width, height);
  draw.attr({role:'img', 'aria-label':label});
  const bg = draw.gradient('linear', add => { add.stop(0, C.background); add.stop(.65, C.background_elevated); add.stop(1, C.gradient_end); });
  bg.from(0,0).to(1,1);
  draw.rect(width,height).fill(bg);
  // Light confined to the perimeter; information stays on flat high-contrast surfaces.
  const glow = draw.gradient('radial', add => { add.stop(0,C.databricks_native,.12); add.stop(1,C.background,0); });
  draw.ellipse(width*.85,height*1.1).move(width*.5,-height*.58).fill(glow);
  const state = { draw, width, height, texts:[], icons:[], regions:[] };
  return state;
}
export function txt(s, parent, value, x, y, options={}) {
  const {size=tokens.typography.body_px, weight=400, color=C.text, maxWidth=Infinity, essential=true, align='left'}=options;
  const font=fonts[weight], run=font.layout(String(value));
  if (run.glyphs.some(g=>g.id===0)) throw new Error(`Missing glyph: ${value}`);
  const scale=size/font.unitsPerEm;
  const width=run.positions.reduce((v,p)=>v+p.xAdvance,0)*scale;
  if(width>maxWidth+.01) throw new Error(`Text overflow (${Math.ceil(width)} > ${maxWidth}): ${value}`);
  const start=align==='center'?x-width/2:align==='right'?x-width:x;
  const g=parent.group().attr({'aria-label':String(value),'data-text':String(value)});
  let pen=0;
  run.glyphs.forEach((glyph,i)=>{
    const p=run.positions[i];
    g.path(glyph.path.toSVG()).fill(color).attr({transform:`translate(${start+(pen+p.xOffset)*scale} ${y-p.yOffset*scale}) scale(${scale} ${-scale})`});
    pen+=p.xAdvance;
  });
  s.texts.push({text:String(value),x:start,y:y-size,width,height:size*1.25,size,essential,color});
  return width;
}
export function lines(s,p,values,x,y,opts={}) {
  const gap=opts.gap||Math.round((opts.size||32)*1.25);
  values.forEach((v,i)=>txt(s,p,v,x,y+i*gap,opts));
}
export function wrap(value,width,size=32,weight=400) {
  const words=String(value).split(/\s+/), result=[]; let line='';
  for(const word of words){const next=line?`${line} ${word}`:word;if(measure(next,size,weight)>width&&line){result.push(line);line=word;}else line=next;}
  if(line)result.push(line);return result;
}
export async function icon(s,p,name,x,y,size=54,color=C.hub_custom) {
  const file=path.join(TOOL,'node_modules/lucide-static/icons',`${name}.svg`);
  const source=await fs.readFile(file,'utf8');
  const inner=source.match(/<svg[\s\S]*?>([\s\S]*?)<\/svg>/)[1];
  p.group().attr({transform:`translate(${x} ${y}) scale(${size/24})`,fill:'none',stroke:color,'stroke-width':1.5,'stroke-linecap':'round','stroke-linejoin':'round'}).svg(inner);
  s.icons.push(name);
}
export function panel(p,x,y,w,h,{fill=C.panel,stroke=C.line,radius=tokens.geometry.corner_radius}={}) {
  p.rect(w,h).move(x,y).radius(radius).fill(fill).stroke({color:stroke,width:2});
}
export function line(p,x1,y1,x2,y2,{color=C.line,width=4,dash=null}={}) {
  const el=p.line(x1,y1,x2,y2).stroke({color,width,linecap:'round'}); if(dash)el.attr({'stroke-dasharray':dash});return el;
}
export function arrow(p,points,{color=C.muted,dash=null,width=4}={}) {
  const el=p.polyline(points).fill('none').stroke({color,width,linecap:'round',linejoin:'round'});if(dash)el.attr({'stroke-dasharray':dash});
  const [a,b]=points.slice(-2),angle=Math.atan2(b[1]-a[1],b[0]-a[0]);
  const head=[[b[0]-14*Math.cos(angle-.45),b[1]-14*Math.sin(angle-.45)],b,[b[0]-14*Math.cos(angle+.45),b[1]-14*Math.sin(angle+.45)]];
  p.polyline(head).fill('none').stroke({color,width,linecap:'round',linejoin:'round'});return el;
}
export function tag(s,p,value,x,y,{color=C.hub_custom,size=24,essential=false}={}){
  const w=measure(value,size,700)+28;
  p.rect(w,38).move(x,y).radius(7).fill(C.background_elevated).stroke({color,width:1.5});
  txt(s,p,value,x+14,y+27,{size,weight:700,color,essential}); return w;
}
export function note(s,p,value,x,y,width,{size=32,color=C.muted}={}){
  lines(s,p,wrap(value,width,size),x,y,{size,color,maxWidth:width});
}
export function heading(s,p,kicker,title,{presentation=false}={}) {
  if(!presentation) return;
  txt(s,p,kicker,56,48,{size:24,weight:700,color:C.hub_custom,essential:false});
  txt(s,p,title,56,112,{size:48,weight:700,maxWidth:1490});
  line(p,56,140,1544,140,{width:1.5});
}
