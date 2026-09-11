import { C, labels, txt, lines, wrap, icon, panel, line, arrow, tag, note, heading } from '../lib.mjs';

function frame(s, contract, title, area, mode) {
  const presentation=mode==='presentation';
  heading(s,s.draw,`HUB .ASSISTANT  /  ${area}`,title,{presentation});
  const g=s.draw.group();
  if(presentation) {
    const scale=contract.render_targets[0]==='readme_standard'?.80:.90;
    const dx=contract.render_targets[0]==='readme_standard'?240:80;
    g.attr({transform:`translate(${dx} 160) scale(${scale})`});
    s.contentTransform={scale,dx,dy:160};
    txt(s,s.draw,labels.arquitetura_e_metodo_proposta_visual,56,868,{size:22,color:C.quiet,essential:false});
    txt(s,s.draw,labels.sprint_0,1544,868,{size:22,color:C.quiet,align:'right',essential:false});
  } else s.contentTransform={scale:1,dx:0,dy:0};
  return g;
}

export async function atlas(s,c,mode) {
  const p=frame(s,c,labels.cinco_componentes_responsabilidades_claras,labels.visao_do_ecossistema,mode);
  // Membership rails: dotted, without arrowheads; they are not execution paths.
  p.path('M 635 330 H 134 Q 88 330 88 284 V 200 M 635 402 C 540 352 420 352 102 352 V 375 M 965 300 C 1010 300 1054 252 1054 200 M 965 402 C 993 392 1020 378 1054 375 M 800 522 L 800 575')
    .fill('none').stroke({color:C.line,width:4,dasharray:'3 12',linecap:'round'});
  txt(s,p,labels.contexto_e_metodo,58,56,{size:32,weight:700,color:C.text});
  txt(s,p,labels.codigo_e_utilitarios,970,56,{size:32,weight:700,color:C.text});
  p.polygon('800,170 965,258 965,434 800,522 635,434 635,258').fill(C.atlas_core).stroke({color:C.line,width:2});
  p.polygon('800,210 930,280 930,412 800,482 670,412 670,280').fill(C.panel_high).stroke({color:C.hub_custom,width:3});
  await icon(s,p,'network',772,255,56,C.hub_custom);
  txt(s,p,labels.ecossistema,800,346,{size:34,weight:700,align:'center'});
  txt(s,p,labels.assistant,800,391,{size:38,weight:800,align:'center',color:C.hub_custom});
  txt(s,p,labels.organizacao,800,439,{size:21,weight:700,align:'center',color:C.muted,essential:false});
  const nodes=[
    {x:58,y:112,title:labels.agent_skills,icon:'route',a:[labels.metodo_guardrails],b:[labels.relevancia_ou],special:true},
    {x:58,y:375,title:labels.hub_prompts,icon:'notebook-pen',a:[labels.briefing_aceite],b:[labels.contexto_explicito]},
    {x:1010,y:112,title:labels.hub_snippets,icon:'package-open',a:[labels.funcoes_reutilizaveis],b:[labels.importacao_explicita]},
    {x:1010,y:375,title:labels.hub_scripts,icon:'scan-search',a:[labels.utilitarios_diagnosticos],b:[labels.execucao_sob_demanda]}
  ];
  for(const n of nodes){
    const color=n.special?C.databricks_native:C.hub_custom;
    p.circle(88).move(n.x,n.y).fill(C.panel_high).stroke({color,width:2});
    await icon(s,p,n.icon,n.x+18,n.y+18,52,color);
    txt(s,p,n.title,n.x+108,n.y+47,{size:35,weight:700});
    lines(s,p,n.a,n.x+108,n.y+100,{size:32,color:C.muted});
    lines(s,p,n.b,n.x+108,n.y+145,{size:32,color});
    if(n.special) txt(s,p,labels.mecanismo_nativo_conteudo_hub,n.x+108,n.y+187,{size:24,color:C.muted,essential:false});
    else txt(s,p,labels.conteudo_hub,n.x+108,n.y+187,{size:24,color:C.muted,essential:false});
  }
  // A supporting foundation, deliberately outside the two primary lanes.
  p.path('M 470 599 L 502 575 H 1098 L 1130 599 V 686 H 470 Z').fill(C.panel).stroke({color:C.hub_custom,width:2});
  await icon(s,p,'blocks',504,605,48,C.hub_custom);
  txt(s,p,labels.hub_padroes,580,619,{size:33,weight:700});
  txt(s,p,labels.moldes_para_criar_e_manter,580,665,{size:32,color:C.muted});
  txt(s,p,labels.as_ligacoes_mostram_organizacao_cada_componente_tem_sua_propria_forma_,800,734,{size:28,align:'center',color:C.muted,essential:false});
}

export async function routes(s,c,mode) {
  const p=frame(s,c,labels.contexto_orienta_codigo_executa,labels.duas_rotas_de_uso,mode);
  tag(s,p,labels.contexto,54,28,{color:C.databricks_native});
  tag(s,p,labels.execucao,54,449,{color:C.hub_custom});
  const top=[
    {x:235,title:labels.objetivo_e_recursos,note:labels.pedido_e_add_context,icon:'scan-search'},
    {x:750,title:labels.contexto_aplicavel,note:labels.instrucoes_skill_e_briefing,icon:'layers-3'},
    {x:1265,title:labels.genie_code,note:labels.plano_codigo_ou_acoes,icon:'sparkles'}
  ];
  arrow(p,[[235,142],[1265,142]],{color:C.databricks_native,width:6});
  for(const n of top){
    p.circle(104).center(n.x,142).fill(C.background_elevated).stroke({color:C.databricks_native,width:3});
    await icon(s,p,n.icon,n.x-28,114,56,C.databricks_native);
    txt(s,p,n.title,n.x,244,{size:34,weight:700,align:'center'});
    txt(s,p,n.note,n.x,290,{size:32,align:'center',color:C.muted});
  }
  // The review bridge identifies project practice without asserting a universal platform lock.
  arrow(p,[[1265,314],[1265,380],[670,380],[670,480]],{color:C.human_decision,width:4});
  p.polygon('990,345 1025,380 990,415 955,380').fill(C.background_elevated).stroke({color:C.human_decision,width:3});
  await icon(s,p,'user-round-check',971,361,38,C.human_decision);
  panel(p,335,324,570,103,{stroke:C.human_decision,fill:C.background_elevated,radius:10});
  txt(s,p,labels.revisao_de_proposta_e_escopo,360,365,{size:32,weight:600,color:C.human_decision});
  txt(s,p,labels.conforme_politica_configurada,360,407,{size:32,color:C.muted});
  arrow(p,[[160,544],[1425,544]],{color:C.muted,width:6});
  const bottom=[
    {x:165,title:labels.helpers_hub,lines:[labels.snippets_scripts],icon:'package-open'},
    {x:670,title:labels.notebook,lines:[labels.importa_e_chama],icon:'notebook-tabs'},
    {x:1115,title:labels.runtime,lines:[labels.python_spark_sql],icon:'cpu'},
    {x:1450,title:labels.evidencia,lines:['resultado + limites'],icon:'badge-check'}
  ];
  for(const n of bottom){
    const color=n.x===1450?C.result_evidence:n.x===165?C.hub_custom:C.databricks_native;
    p.circle(92).center(n.x,544).fill(C.background_elevated).stroke({color,width:3});
    await icon(s,p,n.icon,n.x-25,519,50,color);
    txt(s,p,n.title,n.x,636,{size:33,weight:700,align:'center'});
    if(n.x===1450) lines(s,p,[labels.resultado,labels.limites],n.x,676,{size:32,color:C.muted,anchor:'middle',align:'center',gap:40});
    else txt(s,p,n.lines[0],n.x,680,{size:32,color:C.muted,align:'center'});
  }
  txt(s,p,labels.acao_explicita,408,522,{size:26,color:C.hub_custom,align:'center',essential:false});
  txt(s,p,labels.rota_de_reuso_no_notebook_helpers_tambem_podem_ser_utilizados_diretame,56,736,{size:27,color:C.muted,essential:false});
}

export async function workbench(s,c,mode) {
  const p=frame(s,c,labels.uma_bancada_sete_contratos_de_saida,labels.hub_scripts_2,mode);
  tag(s,p,labels.execucao_sob_demanda_2,54,26,{color:C.hub_custom});
  txt(s,p,labels.utilitarios_diagnosticos_2,1544,55,{size:27,weight:700,align:'right',color:C.muted,essential:false});
  // Four measured work surfaces; accent bars classify zones, the Hub badge owns provenance.
  const tiles=[
    {x:54,y:106,w:726,h:252,title:labels.qualidade_e_perfil,icon:'scan-search',tools:c.prototype_content.zones[0].tools,topic:labels.inspecionar_a_base},
    {x:820,y:106,w:726,h:252,title:labels.estabilidade,icon:'activity',tools:c.prototype_content.zones[1].tools,topic:labels.comparar_distribuicoes},
    {x:54,y:393,w:726,h:280,title:labels.transformacao_analitica,icon:'users-round',tools:c.prototype_content.zones[2].tools,topic:labels.construir_features},
    {x:820,y:393,w:726,h:280,title:labels.governanca_tecnica,icon:'files',tools:c.prototype_content.zones[3].tools,topic:labels.descrever_e_conferir}
  ];
  for(const n of tiles){
    p.path(`M ${n.x} ${n.y+22} L ${n.x+22} ${n.y} H ${n.x+n.w-22} L ${n.x+n.w} ${n.y+22} V ${n.y+n.h} H ${n.x} Z`).fill(C.panel).stroke({color:C.line,width:2});
    p.rect(n.w-88,3).move(n.x+44,n.y+93).fill(C.line);
    await icon(s,p,n.icon,n.x+26,n.y+22,48,C.hub_custom);
    txt(s,p,n.title,n.x+94,n.y+59,{size:34,weight:700,maxWidth:n.w-118});
    let yy=n.y+135;
    for(const [name,result] of n.tools){
      txt(s,p,name,n.x+30,yy,{size:32,weight:600,maxWidth:350});
      txt(s,p,result,n.x+n.w-28,yy,{size:32,color:C.muted,align:'right',maxWidth:340});
      yy+=47;
    }
    if(n.tools.length===1){
      const specific=n.title===labels.estabilidade?labels.classifica_somente_com_limiares_definidos:labels.recencia_frequencia_e_valor_por_entidade;
      txt(s,p,specific,n.x+30,yy+22,{size:32,color:C.muted,maxWidth:n.w-60});
    }
    txt(s,p,n.topic,n.x+30,n.y+n.h-22,{size:22,color:C.quiet,weight:700,essential:false});
  }
  await icon(s,p,'sliders-horizontal',54,708,30,C.human_decision);
  txt(s,p,labels.cada_ferramenta_tem_seu_contrato_a_politica_consumidora_define_a_reaca,104,734,{size:32,color:C.muted});
}

export async function dossier(s,c,mode) {
  const p=frame(s,c,labels.uma_skill_por_dentro,labels.agent_skills_2,mode);
  tag(s,p,labels.mecanismo_nativo_conteudo_hub_2,54,28,{color:C.databricks_native,size:24});
  // The folder under the dossier gives an unambiguous containment cue.
  p.path('M 66 120 H 310 L 340 148 H 820 V 803 H 66 Z').fill(C.dossier_back).stroke({color:C.line,width:2});
  p.rect(690,642).move(91,145).radius(13).fill(C.dossier_middle).stroke({color:C.line,width:2});
  p.path('M 123 131 H 664 L 736 203 V 755 H 123 Z').fill(C.panel).stroke({color:C.hub_custom,width:3});
  p.path('M 664 132 V 203 H 735').fill(C.dossier_fold).stroke({color:C.hub_custom,width:2});
  await icon(s,p,'file-code-2',152,160,52,C.hub_custom);
  txt(s,p,labels.skill_md,230,201,{size:48,weight:800});
  panel(p,153,244,551,197,{fill:C.background_elevated,stroke:C.databricks_native,radius:12});
  txt(s,p,labels.frontmatter_yaml,181,289,{size:33,weight:700,color:C.databricks_native});
  txt(s,p,labels.name_identidade_da_skill,181,335,{size:28,weight:600,maxWidth:495});
  txt(s,p,labels.description_quando_usar,181,374,{size:28,weight:600,maxWidth:495});
  txt(s,p,labels.description_continuation,181,413,{size:28,weight:600,maxWidth:495});
  txt(s,p,labels.instrucoes_em_markdown,153,493,{size:34,weight:700});
  const body=[labels.sequencia_de_trabalho,labels.exemplos_e_guardrails,labels.criterios_de_saida,labels.referencias_aos_recursos];
  for(let i=0;i<body.length;i++){
    p.circle(7).center(160,537+i*46).fill(C.hub_custom);
    txt(s,p,body[i],181,548+i*46,{size:29,color:C.muted});
  }
  txt(s,p,labels.cabecalho_corpo_no_mesmo_arquivo,155,720,{size:21,color:C.quiet,weight:700,essential:false});
  arrow(p,[[735,420],[866,420]],{color:C.supporting_method,dash:'10 9'});
  txt(s,p,labels.recursos_associados,866,207,{size:34,weight:700});
  lines(s,p,[labels.opcionais_e_referenciados,labels.conforme_a_necessidade],866,252,{size:28,color:C.muted,gap:39});
  const resources=[[labels.templates,'file-stack',labels.moldes_de_apoio],[labels.referencias,'library-big',labels.detalhes_e_padroes],[labels.scripts,'terminal-square',labels.acoes_reproduziveis]];
  for(let i=0;i<resources.length;i++){
    const [name,ico,desc]=resources[i],y=337+i*139;
    p.path(`M 882 ${y} H 1050 L 1075 ${y+21} H 1313 V ${y+105} H 882 Z`).fill(C.panel).stroke({color:C.supporting_method,width:2});
    await icon(s,p,ico,906,y+29,46,C.supporting_method);
    txt(s,p,name,979,y+50,{size:32,weight:700});
    txt(s,p,desc,979,y+90,{size:28,color:C.muted});
  }
  txt(s,p,labels.metadados_ajudam_a_selecionar_instrucoes_orientam_recursos_aprofundam,700,852,{size:28,align:'center',color:C.muted});
}

export async function briefing(s,c,mode) {
  const p=frame(s,c,labels.um_briefing_que_torna_a_entrega_verificavel,labels.hub_prompts_2,mode);
  tag(s,p,labels.briefing_tecnico,54,28,{color:C.hub_custom});
  txt(s,p,labels.preencher_contextualizar_conferir,1346,55,{size:23,weight:700,color:C.muted,align:'right',essential:false});
  // A single structured document with in-place annotations, not six independent cards.
  p.path('M 80 114 H 1223 L 1292 183 V 741 H 80 Z').fill(C.panel).stroke({color:C.line,width:2});
  p.path('M 1223 114 V 183 H 1292').fill(C.panel_high).stroke({color:C.line,width:2});
  line(p,667,170,667,694,{width:2});
  const positions=[[118,168],[715,168],[118,349],[715,349],[118,532],[715,532]];
  const blocks=[
    [labels.step_01,labels.objetivo_e_contexto,[labels.decisao_populacao_e_grao,labels.periodo_e_premissas],'target'],
    [labels.step_02,labels.recursos,[labels.tabela_notebook_ou_arquivo,labels.add_context],'paperclip'],
    [labels.step_03,labels.restricoes,[labels.custo_tempo_e_permissoes,labels.acoes_proibidas],'shield-alert'],
    [labels.step_04,labels.modo_de_trabalho,[labels.explicar_planejar_gerar,labels.codigo_ou_executar],'list-checks'],
    [labels.step_05,labels.contrato_de_saida,[labels.artefatos_e_evidencias,labels.limitacoes_declaradas],'package-check'],
    [labels.step_06,labels.validacao_final,[labels.criterios_de_aceite,labels.fatos_versus_hipoteses],'badge-check']
  ];
  for(let i=0;i<blocks.length;i++){
    const [num,title,copy,ico]=blocks[i],[x,y]=positions[i];
    txt(s,p,num,x,y+32,{size:32,weight:800,color:C.hub_custom});
    await icon(s,p,ico,x+448,y+3,39,C.muted);
    txt(s,p,title,x,y+79,{size:31,weight:700,maxWidth:500});
    lines(s,p,copy,x,y+123,{size:28,color:C.muted,gap:38,maxWidth:500});
    if(i<4)line(p,x,y+175,x+499,y+175,{width:1.5});
  }
  // Distinct sentinels teach what to write without inventing example schema.
  tag(s,p,labels.nao_informado,103,777,{color:C.human_decision,size:28,essential:true});
  txt(s,p,labels.ainda_desconhecido,407,806,{size:28,color:C.muted});
  tag(s,p,labels.nao_aplicavel,739,777,{color:C.supporting_method,size:28,essential:true});
  lines(s,p,[labels.fora_do_escopo],1030,806,{size:28,color:C.muted,maxWidth:352});
  if(mode==='readme') txt(s,p,labels.o_formulario_organiza_a_conversa_o_template_em_markdown_e_a_versao_cop,700,867,{size:27,align:'center',color:C.muted,essential:false});
}

export const renderers={
  'raiz.01_mapa_ecossistema':atlas,
  'assistant.02_arquitetura_de_uso':routes,
  'scripts.02_catalogo_diagnosticos':workbench,
  'skills.03_anatomia_skill':dossier,
  'prompts.03_anatomia_briefing':briefing
};
