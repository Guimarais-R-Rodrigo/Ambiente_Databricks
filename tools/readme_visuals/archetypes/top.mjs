import { C, txt, lines, icon, panel, arrow, line, note } from '../lib.mjs';

export async function architecture(s) {
  const p=s.draw;
  txt(s,p,'FONTE VERSIONADA',56,66,{size:34,weight:700});
  p.path('M 66 176 H 414 L 454 217 V 553 H 66 Z').fill(C.panel).stroke({color:C.hub_custom,width:3});
  p.path('M 414 176 V 217 H 454').fill(C.panel_high).stroke({color:C.hub_custom,width:2});
  await icon(s,p,'folder-git-2',94,208,58,C.hub_custom);
  txt(s,p,'ambiente_databricks/',94,321,{size:32,weight:700,maxWidth:346});
  lines(s,p,['Instruções','Skills','Biblioteca','Guias'],94,385,{size:32,color:C.muted,gap:45});
  arrow(p,[[454,352],[480,352]],{color:C.hub_custom,width:5});
  txt(s,p,'publicar e conferir',56,127,{size:32,color:C.muted});
  // The workspace contains two planes; it is not a universal execution chain.
  p.path('M 491 105 L 530 77 H 1544 V 664 H 491 Z').fill(C.background_elevated).stroke({color:C.line,width:3});
  txt(s,p,'WORKSPACE',530,58,{size:34,weight:700,color:C.databricks_native});
  txt(s,p,'CONTEXTO APLICÁVEL',536,144,{size:32,weight:700});
  txt(s,p,'Instruções e skills',536,195,{size:32,weight:700,color:C.databricks_native});
  txt(s,p,'relevância / hierarquia',536,239,{size:32,color:C.muted});
  line(p,963,211,1260,211,{color:C.databricks_native,dash:'3 11'});
  txt(s,p,'Briefings e padrões',536,290,{size:32,weight:700,color:C.hub_custom});
  txt(s,p,'contexto explícito',536,334,{size:32,color:C.muted});
  arrow(p,[[963,307],[1164,307],[1260,276]],{color:C.hub_custom,dash:'10 9'});
  await icon(s,p,'sparkles',1322,156,66,C.databricks_native);
  txt(s,p,'Genie Code',1355,278,{size:34,weight:700,align:'center'});
  line(p,527,355,1508,355,{width:2,dash:'8 10'});
  txt(s,p,'EXECUÇÃO EXPLÍCITA',536,412,{size:34,weight:700});
  for(const [from,to] of [[645,900],[900,1155],[1155,1410]]){
    arrow(p,[[from+40,483],[to-40,483]],{color:to===1410?C.result_evidence:C.muted,width:4});
  }
  for(const n of [
    {x:645,name:'Helpers Hub',sub:'API explícita',ico:'package-open',color:C.hub_custom},
    {x:900,name:'Notebook',sub:'código',ico:'notebook-tabs',color:C.databricks_native},
    {x:1155,name:'Runtime',sub:'execução',ico:'cpu',color:C.databricks_native},
    {x:1410,name:'Evidência',sub:'saída / limites',ico:'file-check-2',color:C.result_evidence},
  ]) {
    p.circle(72).center(n.x,483).fill(C.panel).stroke({color:n.color,width:2});
    await icon(s,p,n.ico,n.x-21,462,42,n.color);
    txt(s,p,n.name,n.x,566,{size:33,weight:700,align:'center'});
    txt(s,p,n.sub,n.x,611,{size:32,color:C.muted,align:'center'});
  }
  txt(s,p,'O notebook pode usar helpers sem passar pela conversa.',56,722,{size:32,color:C.muted});
}

export async function lifecycle(s) {
  const p=s.draw;
  txt(s,p,'POLÍTICA DO PROJETO · SETE GATES',56,68,{size:36,weight:700,color:C.human_decision});
  txt(s,p,'Fonte editável e evidências acompanham todo o percurso.',56,122,{size:32,color:C.muted});
  // A rising track signals promotion; the rework rail points only to the source.
  const xs=[125,346,567,788,1009,1230,1451],ys=[380,356,332,308,284,260,236];
  p.polyline(xs.map((x,i)=>[x,ys[i]])).fill('none').stroke({color:C.line,width:13,linecap:'round'});
  const labels=[['Editar','a fonte'],['Validar','contratos'],['Renderizar','o espelho'],['Publicar','e verificar'],['Testar','por impacto'],['Registrar e','versionar'],['Promover','ao destino']];
  const icons=['file-pen-line','list-checks','copy-check','upload','flask-conical','git-commit-horizontal','flag'];
  for(let i=0;i<7;i++){
    if(i<6) arrow(p,[[xs[i]+47,ys[i]-5],[xs[i+1]-47,ys[i+1]+5]],{color:C.muted,width:4});
    p.circle(82).center(xs[i],ys[i]).fill(C.panel).stroke({color:C.human_decision,width:3});
    await icon(s,p,icons[i],xs[i]-23,ys[i]-23,46,C.human_decision);
    txt(s,p,String(i+1),xs[i],ys[i]-68,{size:38,weight:800,align:'center',color:C.muted});
    lines(s,p,labels[i],xs[i],449,{size:32,weight:600,align:'center',gap:44});
  }
  // A shared rail below all seven labels makes rework global, not exclusive to gate 7.
  for(const x of xs) line(p,x,526,x,575,{color:C.human_decision,width:3,dash:'7 8'});
  line(p,125,575,1451,575,{color:C.human_decision,width:3,dash:'7 8'});
  arrow(p,[[346,575],[125,575],[125,525]],{color:C.human_decision,width:4,dash:'7 8'});
  txt(s,p,'Falha em qualquer gate: corrigir na fonte e repetir o percurso.',800,643,{size:32,align:'center',color:C.human_decision,maxWidth:1488});
  txt(s,p,'Publicar inclui conferir o remoto. Promover não é uma ação automática.',56,722,{size:32,color:C.muted});
}

export async function compass(s) {
  const p=s.draw;
  txt(s,p,'COMECE PELA SUA NECESSIDADE',56,65,{size:35,weight:700});
  txt(s,p,'Os componentes podem se complementar na mesma tarefa.',56,117,{size:28,color:C.muted});
  // Five directional petals, not a quantitative radar or a sequential menu.
  const cx=703,cy=460;
  const nodes=[
    {x:708,y:239,tx:708,ty:179,align:'center',ico:'route',title:'Preciso de método',target:'Agent Skill'},
    {x:1120,y:396,tx:1110,ty:489,align:'center',ico:'notebook-pen',title:'Quero estruturar',title2:'o pedido',target:'Hub Prompt'},
    {x:985,y:695,tx:985,ty:775,align:'center',ico:'package-open',title:'Quero reutilizar código',target:'Hub Snippet'},
    {x:390,y:695,tx:390,ty:775,align:'center',ico:'scan-search',title:'Preciso de diagnóstico',target:'Hub Script'},
    {x:274,y:396,tx:274,ty:489,align:'center',ico:'blocks',title:'Vou criar um',title2:'componente',target:'Hub Padrão'},
  ];
  for(const n of nodes){
    line(p,cx,cy,n.x,n.y,{color:C.line,width:3,dash:'4 10'});
    if(n.target==='Agent Skill'){
      p.circle(100).center(n.x,n.y).fill(C.panel_high).stroke({color:C.databricks_native,width:3});
      p.circle(15).center(n.x+38,n.y+38).fill(C.hub_custom);
    }else{
      p.path(`M ${n.x-50} ${n.y-50} H ${n.x+30} L ${n.x+50} ${n.y-30} V ${n.y+50} H ${n.x-50} Z`).fill(C.panel_high).stroke({color:C.hub_custom,width:2});
    }
    await icon(s,p,n.ico,n.x-29,n.y-29,58,C.hub_custom);
    txt(s,p,n.title,n.tx,n.ty,{size:28,weight:600,align:n.align});
    if(n.title2) txt(s,p,n.title2,n.tx,n.ty+39,{size:28,weight:600,align:n.align});
    const destY=n.ty+(n.title2?88:43);
    if(n.ty===179){
      txt(s,p,n.target,n.tx,321,{size:31,weight:700,align:n.align,color:C.databricks_native});
      txt(s,p,'mecanismo nativo · conteúdo Hub',n.tx,356,{size:28,align:n.align,color:C.muted});
    }
    else txt(s,p,n.target,n.tx,destY,{size:31,weight:700,align:n.align,color:C.hub_custom});
  }
  p.polygon('703,381 820,432 820,540 703,600 586,540 586,432').fill(C.background_elevated).stroke({color:C.human_decision,width:3});
  lines(s,p,['Qual resultado','você precisa?'],703,464,{size:29,weight:700,align:'center',gap:44});
}

export async function confluence(s) {
  const p=s.draw;
  txt(s,p,'FONTES DIFERENTES, CONTEXTO APLICÁVEL',56,63,{size:34,weight:700});
  const inputs=[
    ['Código e histórico','célula, consulta, conversa','notebook-tabs'],
    ['Metadados permitidos','nomes, schemas e descrições','database'],
    ['Instruções aplicáveis','pessoais, workspace, hierarquia','file-check-2'],
    ['Skills e recursos','método e conteúdo fornecido','route'],
  ];
  for(let i=0;i<inputs.length;i++){
    const y=185+i*157, [title,sub,ico]=inputs[i];
    p.path(`M 567 ${y} C 762 ${y} 735 442 870 442`).fill('none').stroke({color:i===3?C.supporting_method:C.line,width:4,dasharray:'3 11'});
    p.circle(66).center(88,y).fill(C.panel).stroke({color:i===3?C.hub_custom:C.databricks_native,width:2});
    await icon(s,p,ico,67,y-21,42,i===3?C.hub_custom:C.databricks_native);
    txt(s,p,title,147,y-5,{size:31,weight:700,maxWidth:430});
    txt(s,p,sub,147,y+41,{size:28,color:C.muted,maxWidth:430});
  }
  p.path('M 567 690 C 695 735 752 627 892 516').fill('none').stroke({color:C.hub_custom,width:4,dasharray:'10 9'});
  arrow(p,[[878,527],[892,516]],{color:C.hub_custom,width:4});
  txt(s,p,'relevância',658,578,{size:28,color:C.supporting_method});
  txt(s,p,'@ / Add Context: seleção explícita',56,750,{size:28,color:C.hub_custom});
  p.circle(270).center(1005,442).fill(C.panel).stroke({color:C.databricks_native,width:3});
  await icon(s,p,'sparkles',970,331,70,C.databricks_native);
  txt(s,p,'Genie Code',1005,450,{size:40,weight:800,align:'center'});
  txt(s,p,'contexto da tarefa',1005,495,{size:28,align:'center',color:C.muted});
  lines(s,p,['Explicação, plano ou código;', 'ações conforme escopo e política.'],1005,654,{size:28,align:'center',color:C.muted,gap:42});
  line(p,56,785,1344,785,{width:2});
  txt(s,p,'Uma pasta existir não faz todo o seu conteúdo entrar na conversa.',56,846,{size:28,color:C.muted});
}

export const renderers={
  'raiz.02_arquitetura_ecossistema':architecture,
  'raiz.03_ciclo_de_vida':lifecycle,
  'assistant.01_escolha_ponto_de_partida':compass,
  'assistant.03_contexto_e_execucao':confluence,
};
