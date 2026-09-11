/**
 * Gera as fontes SVG e os PNGs usados pelos READMEs do ecossistema.
 *
 * O SVG e a fonte editável; o PNG e o artefato publicado no Databricks.
 * Requer `sharp`, disponibilizado pelo runtime de dependencias do Codex.
 */

import fs from "node:fs/promises";
import path from "node:path";
import crypto from "node:crypto";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";

const require = createRequire(import.meta.url);
const sharp = require("sharp");

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");
const currentManifest = await fs.readFile(path.join(ROOT, "ambiente_fonte/.assistant/hub_readmes_visual_assets/manifest.yaml"), "utf8");
if (/^version:\s*2\s*$/m.test(currentManifest)) {
  throw new Error("Renderer v1 retired. Use node tools/readme_visuals/production.mjs --family all.");
}
const BASE = path.join(
  ROOT,
  "ambiente_fonte",
  ".assistant",
  "hub_readmes_visual_assets",
  "readmes",
);

const W = 1600;
const H = 900;

const C = {
  bg: "#07111F",
  panel: "#101D2F",
  panel2: "#16263B",
  line: "#2C4059",
  text: "#F7FAFC",
  muted: "#AFC0D4",
  hub: "#FF4F87",
  native: "#5DD6FF",
  human: "#FFC966",
  result: "#66E3C4",
  violet: "#A992FF",
  danger: "#FF7A7A",
};

function esc(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function textLines(x, y, lines, options = {}) {
  const {
    size = 24,
    fill = C.text,
    weight = 500,
    anchor = "start",
    gap = Math.round(size * 1.35),
    opacity = 1,
  } = options;
  const spans = lines
    .map((line, index) => `<tspan x="${x}" dy="${index === 0 ? 0 : gap}">${esc(line)}</tspan>`)
    .join("");
  return `<text x="${x}" y="${y}" text-anchor="${anchor}" font-family="Segoe UI, Arial, sans-serif" font-size="${size}" font-weight="${weight}" fill="${fill}" opacity="${opacity}">${spans}</text>`;
}

function shell(title, subtitle, body, options = {}) {
  const { section = "GUIA VISUAL", note = "Leitura técnica + impacto visual" } = options;
  return `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#07111F"/>
      <stop offset="0.56" stop-color="#0B1728"/>
      <stop offset="1" stop-color="#101B30"/>
    </linearGradient>
    <radialGradient id="glow" cx="0.82" cy="0.08" r="0.85">
      <stop offset="0" stop-color="#FF4F87" stop-opacity="0.18"/>
      <stop offset="0.52" stop-color="#5DD6FF" stop-opacity="0.05"/>
      <stop offset="1" stop-color="#07111F" stop-opacity="0"/>
    </radialGradient>
    <pattern id="grid" width="48" height="48" patternUnits="userSpaceOnUse">
      <path d="M 48 0 L 0 0 0 48" fill="none" stroke="#2C4059" stroke-width="1" opacity="0.16"/>
    </pattern>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="160%">
      <feDropShadow dx="0" dy="12" stdDeviation="14" flood-color="#000814" flood-opacity="0.42"/>
    </filter>
    <marker id="arrow" markerWidth="12" markerHeight="12" refX="9" refY="5" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,5 L0,10 z" fill="#7890AA"/>
    </marker>
  </defs>
  <rect width="${W}" height="${H}" fill="url(#bg)"/>
  <rect width="${W}" height="${H}" fill="url(#glow)"/>
  <rect width="${W}" height="${H}" fill="url(#grid)"/>
  <rect x="68" y="50" width="188" height="34" rx="17" fill="#FF4F87" opacity="0.16"/>
  ${textLines(162, 74, [section], { size: 15, fill: C.hub, weight: 700, anchor: "middle" })}
  ${textLines(68, 122, [title], { size: 40, weight: 750 })}
  ${textLines(68, 158, [subtitle], { size: 20, fill: C.muted, weight: 450 })}
  <line x1="68" y1="186" x2="1532" y2="186" stroke="#2C4059" stroke-width="1"/>
  ${body}
  <line x1="68" y1="838" x2="1532" y2="838" stroke="#2C4059" stroke-width="1"/>
  <circle cx="80" cy="865" r="5" fill="#FF4F87"/>
  ${textLines(96, 871, ["HUB .ASSISTANT"], { size: 14, fill: C.muted, weight: 700 })}
  ${textLines(1532, 871, [note], { size: 14, fill: C.muted, weight: 500, anchor: "end" })}
</svg>`;
}

function card(node) {
  const {
    x, y, w, h, title, lines = [], color = C.native, tag = "", number = "",
    center = false, dim = false,
  } = node;
  const tx = center ? x + w / 2 : x + 28;
  const anchor = center ? "middle" : "start";
  const opacity = dim ? 0.72 : 1;
  const tagMarkup = tag
    ? `<rect x="${x + 24}" y="${y + 20}" width="${Math.max(92, tag.length * 9 + 28)}" height="28" rx="14" fill="${color}" opacity="0.14"/>
       ${textLines(x + 38, y + 40, [tag.toUpperCase()], { size: 12, fill: color, weight: 750 })}`
    : "";
  const numberMarkup = number
    ? `<circle cx="${x + w - 34}" cy="${y + 34}" r="20" fill="${color}" opacity="0.18"/>
       ${textLines(x + w - 34, y + 41, [number], { size: 16, fill: color, weight: 750, anchor: "middle" })}`
    : "";
  const titleY = y + (tag ? 84 : 50);
  return `<g opacity="${opacity}" filter="url(#shadow)">
    <rect x="${x}" y="${y}" width="${w}" height="${h}" rx="24" fill="#101D2F" stroke="#2C4059" stroke-width="1.5"/>
    <rect x="${x}" y="${y}" width="6" height="${h}" rx="3" fill="${color}"/>
    ${tagMarkup}${numberMarkup}
    ${textLines(tx, titleY, Array.isArray(title) ? title : [title], { size: 24, weight: 700, anchor })}
    ${textLines(tx, titleY + (Array.isArray(title) ? title.length * 32 + 12 : 42), lines, { size: 17, fill: C.muted, weight: 450, gap: 25, anchor })}
  </g>`;
}

function connector(a, b, options = {}) {
  const { label = "", dashed = false, color = "#7890AA", vertical = false } = options;
  let x1; let y1; let x2; let y2; let d;
  if (vertical) {
    x1 = a.x + a.w / 2;
    x2 = b.x + b.w / 2;
    if (a.y <= b.y) {
      y1 = a.y + a.h;
      y2 = b.y;
    } else {
      y1 = a.y;
      y2 = b.y + b.h;
    }
    const mid = (y1 + y2) / 2;
    d = `M${x1},${y1} C${x1},${mid} ${x2},${mid} ${x2},${y2}`;
  } else {
    x1 = a.x + a.w; y1 = a.y + a.h / 2;
    x2 = b.x; y2 = b.y + b.h / 2;
    const mid = (x1 + x2) / 2;
    d = `M${x1},${y1} C${mid},${y1} ${mid},${y2} ${x2},${y2}`;
  }
  const lx = (x1 + x2) / 2;
  const ly = (y1 + y2) / 2 - 10;
  return `<path d="${d}" fill="none" stroke="${color}" stroke-width="3" ${dashed ? 'stroke-dasharray="10 9"' : ""} marker-end="url(#arrow)"/>
  ${label ? `<rect x="${lx - Math.max(52, label.length * 4.8)}" y="${ly - 19}" width="${Math.max(104, label.length * 9.6)}" height="28" rx="14" fill="#07111F" stroke="#2C4059"/><text x="${lx}" y="${ly + 1}" text-anchor="middle" font-family="Segoe UI, Arial" font-size="13" font-weight="650" fill="${C.muted}">${esc(label)}</text>` : ""}`;
}

function pills(items, y = 785) {
  let x = 68;
  return items.map(({ label, color }) => {
    const width = label.length * 9 + 52;
    const value = `<g><circle cx="${x + 12}" cy="${y}" r="6" fill="${color}"/><text x="${x + 28}" y="${y + 6}" font-family="Segoe UI, Arial" font-size="15" font-weight="600" fill="${C.muted}">${esc(label)}</text></g>`;
    x += width;
    return value;
  }).join("");
}

function standard(title, subtitle, nodes, edges = [], options = {}) {
  const groups = (options.groups || []).map((g) => `<g>
    <rect x="${g.x}" y="${g.y}" width="${g.w}" height="${g.h}" rx="30" fill="${g.fill || C.panel2}" opacity="${g.opacity || 0.45}" stroke="${g.color || C.line}" stroke-width="1.5" stroke-dasharray="8 8"/>
    ${g.label ? textLines(g.x + 24, g.y + 34, [g.label.toUpperCase()], { size: 13, fill: g.color || C.muted, weight: 750 }) : ""}
  </g>`).join("");
  const links = edges.map((e) => connector(nodes[e.from], nodes[e.to], e)).join("");
  const blocks = nodes.map(card).join("");
  const legend = pills(options.legend || [
    { label: "Mecanismo nativo", color: C.native },
    { label: "Conteúdo do Hub", color: C.hub },
    { label: "Decisão humana", color: C.human },
  ]);
  return shell(title, subtitle, `${groups}${links}${blocks}${legend}`, options);
}

function radial(title, subtitle, centerNode, satellites, options = {}) {
  const cx = centerNode.x + centerNode.w / 2;
  const cy = centerNode.y + centerNode.h / 2;
  const links = satellites.map((n) => {
    const nx = n.x + n.w / 2;
    const ny = n.y + n.h / 2;
    return `<path d="M${cx},${cy} L${nx},${ny}" stroke="${n.color}" stroke-width="3" opacity="0.58" fill="none"/>
      <circle cx="${(cx + nx) / 2}" cy="${(cy + ny) / 2}" r="4" fill="${n.color}"/>`;
  }).join("");
  return shell(title, subtitle, `${links}${satellites.map(card).join("")}${card(centerNode)}${pills(options.legend || [
    { label: "Nativo da plataforma", color: C.native },
    { label: "Extensão customizada", color: C.hub },
  ])}`, options);
}

const specs = [];

function add(area, name, svg) {
  specs.push({ area, name, svg });
}

// Sprint 1 — Hub Snippets
{
  const nodes = [
    { x: 120, y: 300, w: 360, h: 240, title: "__init__.py", tag: "API pública", color: C.native, lines: ["Ponto estável de importação", "Reexporta o contrato"] },
    { x: 620, y: 300, w: 360, h: 240, title: "nome_do_snippet.py", tag: "Implementação", color: C.hub, lines: ["Lógica reutilizável", "Validações e retornos"] },
    { x: 1120, y: 300, w: 360, h: 240, title: "exemplo_*.py", tag: "Notebook", color: C.human, lines: ["Chamada real e copiável", "Interpretação do resultado"] },
  ];
  add("snippets", "01_anatomia_pasta", standard("Anatomia de um snippet", "Três arquivos, três responsabilidades e uma API previsível", nodes, [
    { from: 0, to: 1, label: "reexporta" }, { from: 1, to: 2, label: "é demonstrado em" },
  ], { legend: [{ label: "Contrato público", color: C.native }, { label: "Código do Hub", color: C.hub }, { label: "Uso didático", color: C.human }] }));

  const center = { x: 585, y: 350, w: 430, h: 180, title: "Hub Snippets", tag: "Biblioteca", color: C.hub, center: true, lines: ["Funções importáveis", "para tarefas recorrentes"] };
  const sats = [
    { x: 80, y: 230, w: 330, h: 150, title: "ml", color: C.violet, tag: "Modelagem", lines: ["temporal · métricas · explicabilidade"] },
    { x: 80, y: 540, w: 330, h: 150, title: "spark", color: C.native, tag: "Escala", lines: ["joins · qualidade · amostragem"] },
    { x: 1190, y: 210, w: 330, h: 150, title: "display + visual", color: C.result, tag: "Apresentação", lines: ["tabelas · temas · componentes"] },
    { x: 1190, y: 530, w: 330, h: 150, title: "constants + testing", color: C.human, tag: "Consistência", lines: ["formatos · cores · fixtures"] },
  ];
  add("snippets", "02_mapa_categorias", radial("Mapa funcional da biblioteca", "Categorias organizadas pelo tipo de problema que resolvem", center, sats, { legend: [{ label: "Código customizado do Hub", color: C.hub }, { label: "Famílias especializadas", color: C.violet }] }));

  const steps = [
    { x: 80, y: 300, w: 310, h: 230, title: "Consultar", number: "1", color: C.violet, lines: ["Abra exemplo_*.py", "Entenda entradas e saída"] },
    { x: 455, y: 300, w: 310, h: 230, title: "Configurar", number: "2", color: C.human, lines: ["Torne a raiz visível", "Confirme dependências"] },
    { x: 830, y: 300, w: 310, h: 230, title: "Importar", number: "3", color: C.hub, lines: ["Use a API pública", "Passe parâmetros reais"] },
    { x: 1205, y: 300, w: 310, h: 230, title: "Validar", number: "4", color: C.result, lines: ["Interprete retorno", "Confira limites e custo"] },
  ];
  add("snippets", "03_fluxo_operacional", standard("Do exemplo ao resultado confiável", "O snippet acelera o trabalho; a validação continua humana", steps, [
    { from: 0, to: 1 }, { from: 1, to: 2 }, { from: 2, to: 3 },
  ], { legend: [{ label: "Preparação", color: C.violet }, { label: "Execução explícita", color: C.hub }, { label: "Validação", color: C.result }] }));

  const reuse = [
    { x: 140, y: 255, w: 390, h: 330, title: "Contrato", tag: "Antes", color: C.native, lines: ["Entradas nomeadas", "Retorno documentado", "Erros previsíveis", "Sem mutação silenciosa"] },
    { x: 605, y: 255, w: 390, h: 330, title: "Reuso", tag: "Durante", color: C.hub, lines: ["Import explícito", "Parâmetros do caso", "Compute consciente", "Evidência observável"] },
    { x: 1070, y: 255, w: 390, h: 330, title: "Confiança", tag: "Depois", color: C.result, lines: ["Resultado interpretado", "Limites declarados", "Teste reproduzível", "Decisão rastreável"] },
  ];
  add("snippets", "04_contrato_de_reuso", standard("O contrato de reuso", "Velocidade só vira ganho quando a interface permanece verificável", reuse, [
    { from: 0, to: 1, label: "habilita" }, { from: 1, to: 2, label: "sustenta" },
  ], { legend: [{ label: "Interface", color: C.native }, { label: "Biblioteca do Hub", color: C.hub }, { label: "Evidência", color: C.result }] }));
}

// Sprint 2 — Hub Scripts
{
  const nodes = [
    { x: 120, y: 300, w: 360, h: 240, title: "__init__.py", tag: "API pública", color: C.native, lines: ["Exportação estável", "Ponto único de import"] },
    { x: 620, y: 300, w: 360, h: 240, title: "nome_do_script.py", tag: "Diagnóstico", color: C.hub, lines: ["Leituras e agregações", "Status, métricas e alertas"] },
    { x: 1120, y: 300, w: 360, h: 240, title: "exemplo_*.py", tag: "Notebook", color: C.human, lines: ["Configuração real", "Tratamento do veredito"] },
  ];
  add("scripts", "01_anatomia_pasta", standard("Anatomia de um Hub Script", "Separação clara entre interface, diagnóstico e demonstração", nodes, [
    { from: 0, to: 1, label: "expõe" }, { from: 1, to: 2, label: "é aplicado em" },
  ]));

  const center = { x: 585, y: 355, w: 430, h: 170, title: "Hub Scripts", tag: "Diagnóstico", color: C.hub, center: true, lines: ["Inspeções explícitas", "sem enforcement implícito"] };
  const sats = [
    { x: 100, y: 220, w: 350, h: 170, title: "Saúde dos dados", color: C.native, tag: "Perfil", lines: ["quality · profile · RFV"] },
    { x: 100, y: 540, w: 350, h: 170, title: "Estabilidade", color: C.violet, tag: "Mudança", lines: ["drift de distribuição"] },
    { x: 1150, y: 300, w: 350, h: 220, title: "Governança técnica", color: C.human, tag: "Contratos", lines: ["schema em YAML", "naming checker", "cobertura documental"] },
  ];
  add("scripts", "02_catalogo_diagnosticos", radial("Catálogo por pergunta de diagnóstico", "Escolha o script pelo risco que precisa tornar visível", center, sats));

  const nodes3 = [
    { x: 70, y: 310, w: 260, h: 220, title: "Notebook", tag: "Configura", color: C.human, lines: ["recurso · chaves", "limiares · escopo"] },
    { x: 390, y: 310, w: 260, h: 220, title: "Hub Script", tag: "Inspeciona", color: C.hub, lines: ["leituras", "agregações"] },
    { x: 710, y: 310, w: 260, h: 220, title: "Dados", tag: "Responde", color: C.native, lines: ["schema", "estatísticas"] },
    { x: 1030, y: 230, w: 260, h: 180, title: "PASS", tag: "Resultado", color: C.result, lines: ["prosseguir conforme", "a política"] },
    { x: 1030, y: 455, w: 260, h: 180, title: "WARN", tag: "Resultado", color: C.human, lines: ["analisar alerta", "antes de decidir"] },
    { x: 1340, y: 345, w: 190, h: 180, title: "FAIL", tag: "Resultado", color: C.danger, lines: ["bloquear só se", "foi codificado"] },
  ];
  add("scripts", "03_fluxo_execucao", standard("Como o diagnóstico produz um veredito", "O script mede; o consumidor decide como reagir", nodes3, [
    { from: 0, to: 1 }, { from: 1, to: 2 }, { from: 2, to: 3 }, { from: 2, to: 4 }, { from: 4, to: 5, dashed: true },
  ], { legend: [{ label: "Decisão humana", color: C.human }, { label: "Código do Hub", color: C.hub }, { label: "Leitura nativa", color: C.native }] }));

  const nodes4 = [
    { x: 120, y: 300, w: 370, h: 260, title: "Hub Script", tag: "Mede", color: C.hub, lines: ["Retorna métricas", "Sinaliza alertas", "Não agenda nem bloqueia"] },
    { x: 615, y: 300, w: 370, h: 260, title: "Política consumidora", tag: "Decide", color: C.human, lines: ["Prosseguir", "Alertar", "Falhar"] },
    { x: 1110, y: 220, w: 370, h: 220, title: "Lakeflow Jobs", tag: "Orquestra", color: C.native, lines: ["Execução", "notificações"] },
    { x: 1110, y: 500, w: 370, h: 220, title: "Pipelines", tag: "Aplica", color: C.native, lines: ["Expectations", "event log"] },
  ];
  add("scripts", "04_diagnostico_vs_enforcement", standard("Diagnóstico não é enforcement", "Medição, política e orquestração são camadas diferentes", nodes4, [
    { from: 0, to: 1, label: "entrega evidência" }, { from: 1, to: 2, label: "aciona" }, { from: 1, to: 3, label: "aciona" },
  ], { legend: [{ label: "Extensão do Hub", color: C.hub }, { label: "Política da equipe", color: C.human }, { label: "Serviço Databricks", color: C.native }] }));

  const nodes5 = [
    { x: 120, y: 270, w: 390, h: 350, title: "PASS", tag: "Evidência suficiente", color: C.result, lines: ["Critérios atendidos", "Registrar a execução", "Prosseguir conforme o fluxo"] },
    { x: 605, y: 270, w: 390, h: 350, title: "WARN", tag: "Atenção necessária", color: C.human, lines: ["Investigar a causa", "Avaliar materialidade", "Documentar a decisão"] },
    { x: 1090, y: 270, w: 390, h: 350, title: "FAIL", tag: "Critério violado", color: C.danger, lines: ["Interromper se previsto", "Corrigir ou justificar", "Reexecutar o diagnóstico"] },
  ];
  add("scripts", "05_leitura_do_veredito", standard("Como ler o veredito", "Status é evidência operacional — nunca uma decisão de negócio automática", nodes5, [], { legend: [{ label: "Aprovado", color: C.result }, { label: "Requer análise", color: C.human }, { label: "Violação", color: C.danger }] }));
}

// Sprint 3 — Agent Skills
{
  const nodes = [
    { x: 80, y: 310, w: 260, h: 230, title: "Necessidade", tag: "Usuário", color: C.human, lines: ["Descreve o objetivo", "ou usa @hub-ml-*"] },
    { x: 405, y: 310, w: 280, h: 230, title: "Relevância", tag: "Genie Code", color: C.native, lines: ["Avalia description", "ou respeita seleção"] },
    { x: 750, y: 310, w: 280, h: 230, title: "SKILL.md", tag: "Método", color: C.hub, lines: ["Carrega instruções", "e recursos necessários"] },
    { x: 1095, y: 225, w: 280, h: 200, title: "Plano", tag: "Revisão", color: C.violet, lines: ["Premissas", "operações propostas"] },
    { x: 1095, y: 500, w: 280, h: 200, title: "Execução", tag: "Após aprovação", color: C.result, lines: ["Código ou ação", "evidência verificável"] },
    { x: 1425, y: 345, w: 120, h: 170, title: "QA", tag: "Humano", color: C.human, lines: ["revisa"] },
  ];
  add("skills", "01_descoberta_e_selecao", standard("Da necessidade à skill adequada", "Seleção por relevância ou ativação explícita com @", nodes, [
    { from: 0, to: 1 }, { from: 1, to: 2 }, { from: 2, to: 3 }, { from: 3, to: 4, vertical: true }, { from: 4, to: 5 },
  ]));

  const nodes2 = [
    { x: 70, y: 310, w: 255, h: 230, title: "Pergunta", tag: "Usuário", color: C.human, lines: ["Objetivo", "dados e limites"] },
    { x: 380, y: 310, w: 255, h: 230, title: "Genie Code", tag: "Nativo", color: C.native, lines: ["Orquestra contexto", "e propõe plano"] },
    { x: 690, y: 310, w: 255, h: 230, title: "Agent Skill", tag: "Método", color: C.hub, lines: ["Guardrails", "critérios de saída"] },
    { x: 1000, y: 310, w: 255, h: 230, title: "Helpers", tag: "Implementação", color: C.hub, lines: ["Import explícito", "execução revisada"] },
    { x: 1310, y: 310, w: 225, h: 230, title: "Evidência", tag: "Resultado", color: C.result, lines: ["Métricas", "limites"] },
  ];
  add("skills", "02_skill_helpers_runtime", standard("Método, implementação e execução", "A skill orienta; snippets e scripts só executam quando importados", nodes2, [
    { from: 0, to: 1 }, { from: 1, to: 2 }, { from: 2, to: 3, label: "recomenda" }, { from: 3, to: 4 },
  ]));

  const layers = [
    { x: 140, y: 260, w: 390, h: 360, title: "Descoberta", tag: "Frontmatter", color: C.native, lines: ["name", "description", "quando a skill é relevante", "identidade hub-ml-*"] },
    { x: 605, y: 260, w: 390, h: 360, title: "Método", tag: "SKILL.md", color: C.hub, lines: ["sequência de trabalho", "guardrails", "critérios de aceite", "rotas para recursos"] },
    { x: 1070, y: 260, w: 390, h: 360, title: "Recursos", tag: "Sob demanda", color: C.violet, lines: ["templates", "referências", "exemplos", "scripts auxiliares"] },
  ];
  add("skills", "03_camadas_de_uma_skill", standard("As três camadas de uma Agent Skill", "Metadados roteiam, instruções orientam e recursos aprofundam", layers, [
    { from: 0, to: 1, label: "seleciona" }, { from: 1, to: 2, label: "carrega quando necessário" },
  ], { legend: [{ label: "Mecanismo de descoberta", color: C.native }, { label: "Conteúdo do Hub", color: C.hub }, { label: "Apoio sob demanda", color: C.violet }] }));
}

// Sprint 4 — Hub Prompts
{
  const nodes = [
    { x: 80, y: 310, w: 280, h: 230, title: "Briefing", tag: "Problema", color: C.hub, lines: ["Contexto", "restrições e aceite"] },
    { x: 420, y: 310, w: 280, h: 230, title: "Agent Skill", tag: "Método", color: C.violet, lines: ["Processo", "guardrails"] },
    { x: 760, y: 310, w: 280, h: 230, title: "Genie Code", tag: "Nativo", color: C.native, lines: ["Integra contexto", "propõe plano e código"] },
    { x: 1100, y: 310, w: 280, h: 230, title: "Helpers", tag: "Implementação", color: C.hub, lines: ["Snippets", "scripts explícitos"] },
    { x: 1420, y: 335, w: 130, h: 180, title: "Entrega", tag: "QA", color: C.result, lines: ["evidência"] },
  ];
  add("prompts", "01_sinergia_contexto", standard("A sinergia entre contexto, método e código", "Cada componente responde a uma pergunta diferente", nodes, [
    { from: 0, to: 2 }, { from: 1, to: 2, dashed: true }, { from: 2, to: 3 }, { from: 3, to: 4 },
  ]));

  const steps = [
    { x: 65, y: 300, w: 230, h: 240, title: "Selecionar", number: "1", color: C.violet, lines: ["Escolha a família", "certa de briefing"] },
    { x: 320, y: 300, w: 230, h: 240, title: "Preencher", number: "2", color: C.hub, lines: ["Declare contexto", "limites e aceite"] },
    { x: 575, y: 300, w: 230, h: 240, title: "Anexar", number: "3", color: C.native, lines: ["Use @ e recursos", "explicitamente"] },
    { x: 830, y: 300, w: 230, h: 240, title: "Revisar", number: "4", color: C.human, lines: ["Corrija premissas", "antes de executar"] },
    { x: 1085, y: 300, w: 230, h: 240, title: "Executar", number: "5", color: C.native, lines: ["Somente o escopo", "autorizado"] },
    { x: 1340, y: 300, w: 230, h: 240, title: "Validar", number: "6", color: C.result, lines: ["Compare a entrega", "ao contrato"] },
  ];
  add("prompts", "02_fluxo_operacional", standard("Do briefing à entrega verificável", "Um bom prompt reduz ambiguidade sem substituir a revisão", steps, [
    { from: 0, to: 1 }, { from: 1, to: 2 }, { from: 2, to: 3 }, { from: 3, to: 4 }, { from: 4, to: 5 },
  ]));

  const anatomy = [
    { x: 100, y: 245, w: 420, h: 410, title: "Objetivo e contexto", tag: "Por quê", color: C.violet, lines: ["Problema de negócio", "grão e população", "fontes anexadas", "o que já é conhecido"] },
    { x: 590, y: 245, w: 420, h: 410, title: "Restrições e operação", tag: "Como", color: C.hub, lines: ["colunas e chaves", "período e filtros", "custo e permissões", "ações proibidas"] },
    { x: 1080, y: 245, w: 420, h: 410, title: "Entrega e aceite", tag: "Pronto quando", color: C.result, lines: ["artefatos esperados", "evidências mínimas", "limitações declaradas", "critérios verificáveis"] },
  ];
  add("prompts", "03_anatomia_do_briefing", standard("Anatomia de um briefing forte", "O contexto útil conecta intenção, execução e critério de conclusão", anatomy, [
    { from: 0, to: 1, label: "delimita" }, { from: 1, to: 2, label: "produz" },
  ], { legend: [{ label: "Intenção", color: C.violet }, { label: "Controle", color: C.hub }, { label: "Critério de aceite", color: C.result }] }));
}

// Sprint 5 — README raiz + README do ecossistema
{
  const center = { x: 585, y: 350, w: 430, h: 185, title: "Ecossistema .assistant", tag: "Contexto ampliado", color: C.hub, center: true, lines: ["Método + briefing", "código + padrões"] };
  const sats = [
    { x: 70, y: 205, w: 345, h: 160, title: "Agent Skills", color: C.native, tag: "Nativo + Hub", lines: ["metodologia · guardrails"] },
    { x: 70, y: 525, w: 345, h: 160, title: "Hub Prompts", color: C.hub, tag: "Customizado", lines: ["briefing · critérios de aceite"] },
    { x: 1185, y: 180, w: 345, h: 160, title: "Hub Snippets", color: C.hub, tag: "Customizado", lines: ["funções importáveis"] },
    { x: 1185, y: 380, w: 345, h: 160, title: "Hub Scripts", color: C.hub, tag: "Customizado", lines: ["diagnósticos explícitos"] },
    { x: 1185, y: 580, w: 345, h: 160, title: "Hub Padrões", color: C.hub, tag: "Customizado", lines: ["moldes e consistência"] },
  ];
  add("raiz", "01_mapa_ecossistema", radial("O ecossistema em uma visão", "Cinco componentes complementares, uma experiência coerente", center, sats));

  const nodes2 = [
    { x: 70, y: 310, w: 260, h: 230, title: "Repositório", tag: "Canônico", color: C.violet, lines: ["fonte", "ferramentas e testes"] },
    { x: 390, y: 310, w: 260, h: 230, title: "Workspace", tag: "Databricks", color: C.native, lines: [".assistant", "instruções"] },
    { x: 710, y: 310, w: 260, h: 230, title: "Genie Code", tag: "Contexto", color: C.native, lines: ["instruções", "skills e briefing"] },
    { x: 1030, y: 310, w: 260, h: 230, title: "Notebook", tag: "Revisão", color: C.human, lines: ["Python", "PySpark ou SQL"] },
    { x: 1350, y: 310, w: 190, h: 230, title: "Runtime", tag: "Execução", color: C.result, lines: ["dados", "evidência"] },
  ];
  add("raiz", "02_arquitetura_ecossistema", standard("Arquitetura de ponta a ponta", "Da fonte versionada à evidência executada no Databricks", nodes2, [
    { from: 0, to: 1, label: "publica" }, { from: 1, to: 2, label: "contextualiza" }, { from: 2, to: 3, label: "propõe" }, { from: 3, to: 4, label: "executa" },
  ]));

  const steps = [
    { x: 65, y: 300, w: 230, h: 235, title: "Editar", number: "1", color: C.violet, lines: ["fonte canônica"] },
    { x: 320, y: 300, w: 230, h: 235, title: "Validar", number: "2", color: C.result, lines: ["contratos e links"] },
    { x: 575, y: 300, w: 230, h: 235, title: "Renderizar", number: "3", color: C.hub, lines: ["espelho derivado"] },
    { x: 830, y: 300, w: 230, h: 235, title: "Publicar", number: "4", color: C.native, lines: ["manifesto e hashes"] },
    { x: 1085, y: 300, w: 230, h: 235, title: "Verificar", number: "5", color: C.human, lines: ["conteúdo no destino"] },
    { x: 1340, y: 300, w: 230, h: 235, title: "Testar", number: "6", color: C.result, lines: ["runtime e Genie Code"] },
  ];
  add("raiz", "03_ciclo_de_vida", standard("Ciclo de vida do projeto", "Cada mudança percorre os mesmos gates antes de chegar à equipe", steps, [
    { from: 0, to: 1 }, { from: 1, to: 2 }, { from: 2, to: 3 }, { from: 3, to: 4 }, { from: 4, to: 5 },
  ]));

  const nodes4 = [
    { x: 70, y: 310, w: 255, h: 230, title: "Objetivo", tag: "Pessoa", color: C.human, lines: ["dados", "limites e recursos"] },
    { x: 380, y: 310, w: 255, h: 230, title: "Genie Code", tag: "Nativo", color: C.native, lines: ["aplica instruções", "e skill relevante"] },
    { x: 690, y: 310, w: 255, h: 230, title: "Plano", tag: "Proposta", color: C.violet, lines: ["premissas", "código e ações"] },
    { x: 1000, y: 310, w: 255, h: 230, title: "Revisão", tag: "Pessoa", color: C.human, lines: ["corrige", "aprova o escopo"] },
    { x: 1310, y: 310, w: 225, h: 230, title: "Resultado", tag: "Runtime", color: C.result, lines: ["evidências", "limitações"] },
  ];
  add("raiz", "04_fluxo_de_contexto", standard("Como o contexto chega ao resultado", "A plataforma propõe; a pessoa mantém o controle da execução", nodes4, [
    { from: 0, to: 1 }, { from: 1, to: 2 }, { from: 2, to: 3 }, { from: 3, to: 4 },
  ]));

  const useFlow = [
    { x: 65, y: 265, w: 240, h: 220, title: "Objetivo", tag: "Pessoa", color: C.human, lines: ["dados", "restrições"] },
    { x: 355, y: 265, w: 260, h: 220, title: "Genie Code", tag: "Contexto", color: C.native, lines: ["instruções", "skills + briefing"] },
    { x: 665, y: 265, w: 240, h: 220, title: "Revisão", tag: "Pessoa", color: C.human, lines: ["plano", "código proposto"] },
    { x: 955, y: 265, w: 240, h: 220, title: "Notebook", tag: "Execução", color: C.violet, lines: ["Python", "PySpark ou SQL"] },
    { x: 955, y: 575, w: 240, h: 150, title: "Helpers", tag: "Import explícito", color: C.hub, lines: ["snippets + scripts"] },
    { x: 1285, y: 265, w: 250, h: 220, title: "Evidências", tag: "Resultado", color: C.result, lines: ["métricas", "limitações"] },
  ];
  add("assistant", "02_arquitetura_de_uso", standard("As duas rotas da experiência", "Contexto orienta a conversa; helpers entram explicitamente no notebook", useFlow, [
    { from: 0, to: 1 }, { from: 1, to: 2 }, { from: 2, to: 3 }, { from: 4, to: 3, vertical: true, label: "importa" }, { from: 3, to: 5 },
  ]));

  const contextFlow = [
    { x: 65, y: 305, w: 230, h: 235, title: "Informar", number: "1", color: C.human, lines: ["objetivo, limites", "e recursos"] },
    { x: 320, y: 305, w: 230, h: 235, title: "Contextualizar", number: "2", color: C.native, lines: ["instruções", "e Agent Skill"] },
    { x: 575, y: 305, w: 230, h: 235, title: "Planejar", number: "3", color: C.violet, lines: ["premissas", "e operações"] },
    { x: 830, y: 305, w: 230, h: 235, title: "Revisar", number: "4", color: C.human, lines: ["corrigir", "e aprovar"] },
    { x: 1085, y: 305, w: 230, h: 235, title: "Executar", number: "5", color: C.hub, lines: ["imports", "e código"] },
    { x: 1340, y: 305, w: 230, h: 235, title: "Conferir", number: "6", color: C.result, lines: ["evidências", "e limitações"] },
  ];
  add("assistant", "03_contexto_e_execucao", standard("Do contexto à execução revisada", "A Genie Code organiza a proposta; a aprovação e a conferência continuam humanas", contextFlow, [
    { from: 0, to: 1 }, { from: 1, to: 2 }, { from: 2, to: 3 }, { from: 3, to: 4 }, { from: 4, to: 5 },
  ]));

  const decision = [
    { x: 585, y: 215, w: 430, h: 150, title: "O que você precisa agora?", tag: "Ponto de partida", color: C.human, center: true, lines: ["Escolha pelo objetivo, não pelo nome da pasta"] },
    { x: 60, y: 510, w: 270, h: 210, title: "Tarefa completa", color: C.native, tag: "Skill", lines: ["método e guardrails"] },
    { x: 365, y: 510, w: 270, h: 210, title: "Pedido estruturado", color: C.hub, tag: "Prompt", lines: ["briefing preenchível"] },
    { x: 670, y: 510, w: 270, h: 210, title: "Função reutilizável", color: C.hub, tag: "Snippet", lines: ["import no notebook"] },
    { x: 975, y: 510, w: 270, h: 210, title: "Diagnóstico", color: C.hub, tag: "Script", lines: ["status e métricas"] },
    { x: 1280, y: 510, w: 270, h: 210, title: "Novo componente", color: C.violet, tag: "Padrões", lines: ["molde consistente"] },
  ];
  add("assistant", "01_escolha_ponto_de_partida", standard("Escolha o ponto de partida", "Uma pergunta simples direciona para o componente mais útil", decision, [
    { from: 0, to: 1, vertical: true }, { from: 0, to: 2, vertical: true }, { from: 0, to: 3, vertical: true }, { from: 0, to: 4, vertical: true }, { from: 0, to: 5, vertical: true },
  ]));
}

async function writeAsset({ area, name, svg }) {
  const sourceDir = path.join(BASE, area, "sources");
  const pngDir = path.join(BASE, area, "png");
  await fs.mkdir(sourceDir, { recursive: true });
  await fs.mkdir(pngDir, { recursive: true });
  const svgPath = path.join(sourceDir, `${name}.svg`);
  const pngPath = path.join(pngDir, `${name}.png`);
  await fs.writeFile(svgPath, svg, "utf8");
  await sharp(Buffer.from(svg)).png({ compressionLevel: 9, adaptiveFiltering: true }).toFile(pngPath);
  const pngBytes = await fs.readFile(pngPath);
  return {
    area,
    name,
    svgPath,
    pngPath,
    sha256: crypto.createHash("sha256").update(pngBytes).digest("hex"),
  };
}

const written = [];
for (const spec of specs) written.push(await writeAsset(spec));

const manifest = [
  "version: 1",
  "generated_by: tools/render_readme_visuals.mjs",
  "format:",
  "  source: svg",
  "  published: png",
  "  width: 1600",
  "  height: 900",
  "assets:",
  ...written.flatMap((item) => [
    `  - id: ${item.area}.${item.name}`,
    `    source: readmes/${item.area}/sources/${item.name}.svg`,
    `    published: readmes/${item.area}/png/${item.name}.png`,
    `    sha256: ${item.sha256}`,
  ]),
  "",
].join("\n");
await fs.writeFile(path.resolve(BASE, "..", "manifest.yaml"), manifest, "utf8");

console.log(`Gerados ${written.length} pares SVG/PNG em ${BASE}`);
for (const item of written) console.log(`${item.area}/${item.name}`);
