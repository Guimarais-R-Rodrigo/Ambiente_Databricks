import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';
import {
  ROOT,
  ASSET,
  C,
  readYaml,
  sha,
  write,
  newCanvas,
  measure,
  txt,
  icon,
  panel,
  line,
  arrow,
} from '../lib.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUTPUT = path.join(ROOT, '.artifacts/visual-v2/methods');

function addAudit(s, text, color, against) {
  s.contrastAudit ??= [];
  s.contrastAudit.push({ text: String(text), color, against });
}

function t(s, p, value, x, y, options = {}) {
  if (!Number.isFinite(options.maxWidth)) {
    throw new Error(`maxWidth real é obrigatório: ${value}`);
  }
  const color = options.color ?? C.text;
  const against = options.against ?? C.background;
  const clean = { ...options };
  delete clean.against;
  const width = txt(s, p, value, x, y, clean);
  addAudit(s, value, color, against);
  return width;
}

function multiline(s, p, values, x, y, options = {}) {
  const size = options.size ?? 32;
  const gap = options.gap ?? Math.ceil(size * 1.36);
  values.forEach((value, index) => t(s, p, value, x, y + index * gap, options));
}

function chip(s, p, value, x, y, color, { size = 24, maxWidth = 420 } = {}) {
  const w = measure(value, size, 700) + 30;
  if (w > maxWidth) throw new Error(`Chip overflow: ${value}`);
  p.rect(w, 40).move(x, y).radius(8).fill(C.background_elevated).stroke({ color, width: 2 });
  t(s, p, value, x + 15, y + 29, {
    size,
    weight: 700,
    color,
    maxWidth: w - 30,
    essential: false,
    against: C.background_elevated,
  });
  return w;
}

function documentShape(p, x, y, w, h, color = C.hub_custom) {
  const fold = 54;
  p.path(`M ${x} ${y} H ${x + w - fold} L ${x + w} ${y + fold} V ${y + h} H ${x} Z`)
    .fill(C.panel)
    .stroke({ color, width: 3, linejoin: 'round' });
  p.path(`M ${x + w - fold} ${y} V ${y + fold} H ${x + w}`)
    .fill(C.panel_high)
    .stroke({ color, width: 2, linejoin: 'round' });
}

function notebookShape(p, x, y, w, h, color = C.databricks_native) {
  p.path(`M ${x + 34} ${y} H ${x + w} V ${y + h} H ${x} V ${y + 34} Z`)
    .fill(C.panel)
    .stroke({ color, width: 3, linejoin: 'round' });
  p.rect(124, 34).move(x + 34, y).radius(8).fill(C.panel_high).stroke({ color, width: 2 });
}

function packageShape(p, x, y, w, h, color = C.hub_custom) {
  p.path(`M ${x + 20} ${y} H ${x + w} V ${y + h - 20} L ${x + w - 20} ${y + h} H ${x} V ${y + 20} Z`)
    .fill(C.panel)
    .stroke({ color, width: 3, linejoin: 'round' });
}

function curvedArrow(p, d, endX, endY, color, direction = 'right') {
  p.path(d).fill('none').stroke({ color, width: 5, linecap: 'round', linejoin: 'round' });
  const baseX = direction === 'left' ? endX + 15 : endX - 15;
  p.polygon(`${baseX},${endY - 9} ${endX},${endY} ${baseX},${endY + 9}`).fill(color);
}

function frame(s) {
  s.contentTransform = { scale: 1, dx: 0, dy: 0 };
  return s.draw.group();
}

export async function skillSelection(s, c, mode = 'readme') {
  const p = frame(s);
  chip(s, p, 'AGENT SKILLS · DUAS ROTAS SUPORTADAS', 56, 34, C.databricks_native, { maxWidth: 600 });
  t(s, p, 'Como uma skill entra no contexto', 56, 108, {
    size: 38, weight: 800, maxWidth: 720, against: C.background,
  });
  t(s, p, 'Relevância e @ são caminhos independentes que chegam ao mesmo pacote.', 56, 153, {
    size: 32, color: C.muted, maxWidth: 1400, against: C.background,
  });

  // Rota A: uma corrente contextual, sem limiar inventado.
  p.path('M 86 286 C 260 218 424 214 602 284 C 770 350 900 350 1013 412')
    .fill('none').stroke({ color: C.databricks_native, width: 14, linecap: 'round' });
  p.circle(72).center(118, 275).fill(C.background_elevated).stroke({ color: C.databricks_native, width: 3 });
  await icon(s, p, 'message-square-text', 91, 248, 54, C.databricks_native);
  p.circle(96).center(520, 260).fill(C.panel_high).stroke({ color: C.databricks_native, width: 3 });
  await icon(s, p, 'scan-search', 488, 228, 64, C.databricks_native);
  t(s, p, 'ROTA A · RELEVÂNCIA', 88, 386, {
    size: 32, weight: 800, color: C.databricks_native, maxWidth: 420, against: C.background,
  });
  t(s, p, 'Pedido em linguagem natural', 88, 431, {
    size: 32, weight: 700, maxWidth: 460, against: C.background,
  });
  multiline(s, p, ['A description ajuda a Genie Code', 'a avaliar se a skill é aplicável.'], 88, 475, {
    size: 32, color: C.muted, maxWidth: 600, against: C.background,
  });

  // Rota B: escolha humana explícita. O desenho não adiciona confirmação obrigatória.
  p.path('M 86 618 C 290 676 477 653 633 579 C 790 505 900 474 1013 412')
    .fill('none').stroke({ color: C.human_decision, width: 14, linecap: 'round' });
  p.circle(72).center(118, 625).fill(C.background_elevated).stroke({ color: C.human_decision, width: 3 });
  await icon(s, p, 'at-sign', 91, 598, 54, C.human_decision);
  p.circle(96).center(540, 622).fill(C.panel_high).stroke({ color: C.human_decision, width: 3 });
  await icon(s, p, 'mouse-pointer-click', 508, 590, 64, C.human_decision);
  t(s, p, 'ROTA B · MENÇÃO @', 650, 637, {
    size: 32, weight: 800, color: C.human_decision, maxWidth: 520, against: C.background,
  });
  t(s, p, '@nome-da-skill', 650, 683, {
    size: 34, weight: 700, maxWidth: 360, against: C.background,
  });

  // Convergência: o arquivo canônico e as instruções permanecem um único pacote.
  documentShape(p, 1050, 230, 470, 380, C.hub_custom);
  chip(s, p, 'CONTEÚDO DO HUB', 1090, 265, C.hub_custom, { maxWidth: 330 });
  await icon(s, p, 'route', 1090, 340, 66, C.hub_custom);
  multiline(s, p, ['Agent Skill', 'carregada'], 1180, 371, {
    size: 34, weight: 800, maxWidth: 298, gap: 42, against: C.panel,
  });
  line(p, 1090, 434, 1478, 434, { color: C.line, width: 2 });
  multiline(s, p, ['SKILL.md', 'metodologia · guardrails', 'recursos sob demanda'], 1090, 482, {
    size: 32, color: C.muted, maxWidth: 390, gap: 48, against: C.panel,
  });
  p.circle(34).center(1030, 412).fill(C.background_elevated).stroke({ color: C.result_evidence, width: 4 });
  await icon(s, p, 'merge', 1014, 396, 32, C.result_evidence);
  line(p, 1047, 412, 1050, 412, { color: C.result_evidence, width: 5 });
  t(s, p, 'CONVERGÊNCIA', 1170, 664, {
    size: 24, weight: 800, color: C.result_evidence, maxWidth: 260, essential: false, against: C.background,
  });
  t(s, p, 'A rota muda; a responsabilidade de revisar a entrega permanece.', 56, 732, {
    size: 32, color: C.muted, maxWidth: 1040, against: C.background,
  });
}

export async function skillRuntimeCutaway(s, c, mode = 'readme') {
  const p = frame(s);
  chip(s, p, 'CORTE ARQUITETURAL', 56, 30, C.supporting_method, { maxWidth: 420 });
  t(s, p, 'Método acima; execução no runtime', 56, 105, {
    size: 38, weight: 800, maxWidth: 840, against: C.background,
  });

  // Plano superior: contexto. A skill é um documento de método, não um módulo Python.
  p.path('M 56 156 H 1544 V 352 H 56 Z').fill(C.panel_high).stroke({ color: C.databricks_native, width: 3 });
  chip(s, p, 'PLANO DE CONTEXTO', 86, 180, C.databricks_native, { maxWidth: 360 });
  documentShape(p, 104, 244, 300, 82, C.hub_custom);
  await icon(s, p, 'file-text', 126, 260, 42, C.hub_custom);
  t(s, p, 'Agent Skill', 188, 294, {
    size: 32, weight: 800, maxWidth: 184, against: C.panel,
  });
  t(s, p, 'metodologia + guardrails', 500, 285, {
    size: 34, weight: 700, maxWidth: 420, against: C.panel_high,
  });
  arrow(p, [[416, 286], [480, 286]], { color: C.supporting_method, dash: '10 9', width: 5 });
  t(s, p, 'orienta', 424, 242, {
    size: 24, weight: 700, color: C.supporting_method, maxWidth: 120, essential: false, against: C.panel_high,
  });
  p.path('M 923 286 C 1070 286 1110 237 1260 237').fill('none')
    .stroke({ color: C.supporting_method, width: 4, dasharray: '10 9', linecap: 'round' });
  p.rect(270, 83).move(962, 184).radius(8).fill(C.panel_high);
  t(s, p, 'pode recomendar', 984, 218, {
    size: 24, weight: 700, color: C.supporting_method, maxWidth: 240, essential: false, against: C.panel_high,
  });
  t(s, p, 'quando adequado', 984, 249, {
    size: 24, weight: 700, color: C.supporting_method, maxWidth: 240, essential: false, against: C.panel_high,
  });
  packageShape(p, 1270, 200, 230, 112, C.hub_custom);
  await icon(s, p, 'package-open', 1294, 222, 42, C.hub_custom);
  t(s, p, 'helpers', 1354, 254, {
    size: 32, weight: 800, maxWidth: 125, against: C.panel,
  });
  t(s, p, 'não é importação', 1280, 343, {
    size: 24, weight: 700, color: C.muted, maxWidth: 220, essential: false, against: C.panel_high,
  });

  // Laje de separação: a mensagem central do corte arquitetural.
  p.rect(1488, 58).move(56, 358).fill(C.background_elevated).stroke({ color: C.human_decision, width: 3 });
  await icon(s, p, 'split', 82, 371, 34, C.human_decision);
  t(s, p, 'FRONTEIRA · RECOMENDAÇÃO NÃO É IMPORTAÇÃO NEM EXECUÇÃO', 138, 397, {
    size: 32, weight: 800, color: C.human_decision, maxWidth: 1200, against: C.background_elevated,
  });

  // Plano inferior: ações explícitas dentro do notebook e do compute.
  p.path('M 56 422 H 1544 V 704 H 56 Z').fill(C.background_elevated).stroke({ color: C.line, width: 3 });
  chip(s, p, 'PLANO DE RUNTIME', 86, 448, C.hub_custom, { maxWidth: 340 });
  notebookShape(p, 112, 520, 340, 132, C.databricks_native);
  await icon(s, p, 'notebook-tabs', 144, 558, 50, C.databricks_native);
  t(s, p, 'Notebook', 218, 590, {
    size: 34, weight: 800, maxWidth: 190, against: C.panel,
  });
  t(s, p, 'ação explícita', 145, 636, {
    size: 32, color: C.muted, maxWidth: 280, against: C.panel,
  });
  arrow(p, [[476, 586], [618, 586]], { color: C.hub_custom, width: 6 });
  t(s, p, 'importa', 495, 548, {
    size: 24, weight: 800, color: C.hub_custom, maxWidth: 110, essential: false, against: C.background_elevated,
  });
  packageShape(p, 640, 512, 330, 150, C.hub_custom);
  await icon(s, p, 'blocks', 671, 550, 50, C.hub_custom);
  multiline(s, p, ['Hub Snippets', 'Hub Scripts'], 734, 570, {
    size: 32, weight: 800, maxWidth: 220, gap: 41, against: C.panel,
  });
  t(s, p, 'código reutilizável', 671, 652, {
    size: 32, color: C.muted, maxWidth: 280, against: C.panel,
  });
  arrow(p, [[998, 586], [1124, 586]], { color: C.databricks_native, width: 6 });
  t(s, p, 'chama', 1022, 548, {
    size: 24, weight: 800, color: C.databricks_native, maxWidth: 90, essential: false, against: C.background_elevated,
  });
  p.path('M 1150 508 H 1498 V 680 H 1150 L 1182 594 Z').fill(C.panel).stroke({ color: C.databricks_native, width: 3 });
  await icon(s, p, 'cpu', 1202, 550, 54, C.databricks_native);
  t(s, p, 'Runtime', 1286, 580, {
    size: 34, weight: 800, maxWidth: 160, against: C.panel,
  });
  multiline(s, p, ['executa', 'produz evidência'], 1200, 622, {
    size: 32, color: C.muted, maxWidth: 270, gap: 42, against: C.panel,
  });
  t(s, p, 'A skill orienta o trabalho; o notebook controla importação, chamada e execução.', 56, 740, {
    size: 32, color: C.muted, maxWidth: 1250, against: C.background,
  });
}

export async function promptFamilyRouter(s, c, mode = 'readme') {
  const p = frame(s);
  chip(s, p, 'ROTEADOR DE BRIEFINGS', 56, 34, C.hub_custom, { maxWidth: 430 });
  t(s, p, 'Comece pelo resultado esperado', 56, 112, {
    size: 38, weight: 800, maxWidth: 760, against: C.background,
  });
  t(s, p, 'O catálogo textual continua canônico; a figura orienta a primeira escolha.', 56, 158, {
    size: 28, color: C.muted, maxWidth: 1060, against: C.background,
  });

  // Quatro destinos em torno de uma bússola decisória, sem reproduzir o catálogo mutável.
  const cx = 700, cy = 468;
  curvedArrow(p, `M ${cx - 118} ${cy - 78} C 510 330 455 310 400 310`, 400, 310, C.databricks_native, 'left');
  curvedArrow(p, `M ${cx + 118} ${cy - 78} C 890 330 945 310 1000 310`, 1000, 310, C.supporting_method);
  curvedArrow(p, `M ${cx - 118} ${cy + 78} C 510 610 455 645 400 645`, 400, 645, C.human_decision, 'left');
  curvedArrow(p, `M ${cx + 118} ${cy + 78} C 890 610 945 645 1000 645`, 1000, 645, C.result_evidence);

  p.circle(262).center(cx, cy).fill(C.panel_high).stroke({ color: C.hub_custom, width: 4 });
  p.circle(216).center(cx, cy).fill(C.background_elevated).stroke({ color: C.line, width: 2 });
  await icon(s, p, 'compass', 664, 345, 72, C.hub_custom);
  multiline(s, p, ['QUAL', 'RESULTADO', 'VOCÊ', 'PRECISA?'], cx, 457, {
    size: 28, weight: 800, align: 'center', maxWidth: 200, gap: 36, against: C.background_elevated,
  });

  const destinations = [
    {
      x: 40, y: 180, w: 360, h: 270, color: C.databricks_native, icon: 'scan-search',
      number: '01', outcome: ['Entender uma base', 'e seu perfil'], family: ['Exploração &', 'Perfilamento'],
    },
    {
      x: 1000, y: 180, w: 360, h: 270, color: C.supporting_method, icon: 'chart-no-axes-combined',
      number: '02', outcome: ['Modelar, medir', 'ou acompanhar'], family: ['Modelagem, Safras', '& Estatística'],
    },
    {
      x: 40, y: 550, w: 360, h: 270, color: C.human_decision, icon: 'shield-check',
      number: '03', outcome: ['Conferir dados,', 'código ou bases'], family: ['Qualidade,', 'Reconciliação', '& Auditoria'],
    },
    {
      x: 1000, y: 550, w: 360, h: 270, color: C.result_evidence, icon: 'book-open-check',
      number: '04', outcome: ['Explicar, documentar', 'ou iniciar'], family: ['Documentação,', 'Tutoria &', 'Onboarding'],
    },
  ];
  for (const d of destinations) {
    p.path(`M ${d.x + 22} ${d.y} H ${d.x + d.w} V ${d.y + d.h - 22} L ${d.x + d.w - 22} ${d.y + d.h} H ${d.x} V ${d.y + 22} Z`)
      .fill(C.panel).stroke({ color: d.color, width: 3, linejoin: 'round' });
    p.circle(58).center(d.x + 48, d.y + 48).fill(C.background_elevated).stroke({ color: d.color, width: 2 });
    await icon(s, p, d.icon, d.x + 30, d.y + 30, 36, d.color);
    t(s, p, d.number, d.x + d.w - 24, d.y + 56, {
      size: 30, weight: 800, color: d.color, align: 'right', maxWidth: 60, against: C.panel,
    });
    multiline(s, p, d.outcome, d.x + 24, d.y + 103, {
      size: 28, weight: 800, maxWidth: d.w - 48, gap: 36, against: C.panel,
    });
    line(p, d.x + 24, d.y + 151, d.x + d.w - 24, d.y + 151, { color: C.line, width: 2 });
    multiline(s, p, d.family, d.x + 24, d.y + (d.family.length === 3 ? 185 : 203), {
      size: 28, weight: 700, color: d.color, maxWidth: d.w - 48, gap: 36, essential: true, against: C.panel,
    });
  }

  t(s, p, 'DECISÃO', 594, 832, {
    size: 24, weight: 800, color: C.hub_custom, maxWidth: 140, essential: false, against: C.background,
  });
  arrow(p, [[738, 823], [778, 823]], { color: C.muted, width: 3 });
  t(s, p, 'FAMÍLIA', 795, 832, {
    size: 24, weight: 800, color: C.result_evidence, maxWidth: 140, essential: false, against: C.background,
  });
  t(s, p, 'Depois, use a matriz e o catálogo para escolher o briefing específico.', 700, 878, {
    size: 28, color: C.muted, align: 'center', maxWidth: 940, against: C.background,
  });
}

export async function promptFiveStages(s, c, mode = 'readme') {
  const p = frame(s);
  chip(s, p, 'STORYBOARD · 5 MACROESTÁGIOS', 56, 30, C.hub_custom, { maxWidth: 520 });
  t(s, p, 'Do briefing à entrega verificável', 56, 105, {
    size: 38, weight: 800, maxWidth: 780, against: C.background,
  });
  t(s, p, 'Cada cena acrescenta informação ao mesmo trabalho — não é um novo fluxo paralelo.', 56, 150, {
    size: 32, color: C.muted, maxWidth: 1450, against: C.background,
  });

  // Uma película contínua evita a aparência de cinco caixas independentes.
  p.path('M 54 218 H 1546 V 645 H 54 Z').fill(C.panel).stroke({ color: C.line, width: 3 });
  for (let x = 80; x < 1520; x += 72) {
    p.rect(36, 18).move(x, 232).radius(4).fill(C.background);
    p.rect(36, 18).move(x, 613).radius(4).fill(C.background);
  }
  const stages = [
    { n: '01', x: 74, color: C.databricks_native, icon: 'list-filter', title: ['SELECIONAR', 'O BRIEFING'], copy: ['Resultado-alvo', 'família'] },
    { n: '02', x: 372, color: C.supporting_method, icon: 'square-pen', title: ['PREENCHER', 'METADADOS'], copy: ['Contexto + grão', 'tempo explícito'] },
    { n: '03', x: 670, color: C.hub_custom, icon: 'paperclip', title: ['ANEXAR', 'RECURSOS'], copy: ['Contexto', 'limites + modo'] },
    { n: '04', x: 968, color: C.human_decision, icon: 'clipboard-check', title: ['REVISAR', 'O PLANO'], copy: ['Escopo definido', 'política vigente'] },
    { n: '05', x: 1266, color: C.result_evidence, icon: 'badge-check', title: ['VALIDAR', 'A ENTREGA'], copy: ['Evidências', 'limites + aceite'] },
  ];

  // A faixa inferior é uma única progressão; a etapa 4 incorpora a execução no escopo revisado.
  p.path('M 108 556 C 310 508 440 568 630 536 C 820 504 940 564 1120 532 C 1270 505 1380 518 1492 493')
    .fill('none').stroke({ color: C.muted, width: 7, linecap: 'round' });
  p.polygon('1475,482 1504,490 1481,509').fill(C.result_evidence);

  for (let index = 0; index < stages.length; index += 1) {
    const d = stages[index];
    const y = index % 2 === 0 ? 275 : 305;
    p.path(`M ${d.x} ${y + 24} L ${d.x + 24} ${y} H ${d.x + 252} L ${d.x + 276} ${y + 24} V ${y + 275} H ${d.x} Z`)
      .fill(index === 3 ? C.panel_high : C.background_elevated)
      .stroke({ color: d.color, width: 3, linejoin: 'round' });
    p.circle(64).center(d.x + 42, y + 45).fill(C.panel_high).stroke({ color: d.color, width: 3 });
    await icon(s, p, d.icon, d.x + 20, y + 23, 44, d.color);
    t(s, p, d.n, d.x + 250, y + 54, {
      size: 32, weight: 800, color: d.color, align: 'right', maxWidth: 54,
      against: index === 3 ? C.panel_high : C.background_elevated,
    });
    multiline(s, p, d.title, d.x + 22, y + 111, {
      size: 32, weight: 800, maxWidth: 232, gap: 41,
      against: index === 3 ? C.panel_high : C.background_elevated,
    });
    line(p, d.x + 22, y + 160, d.x + 252, y + 160, { color: C.line, width: 2 });
    multiline(s, p, d.copy, d.x + 22, y + 202, {
      size: 32, color: C.muted, maxWidth: 250, gap: 42,
      against: index === 3 ? C.panel_high : C.background_elevated,
    });
  }

  chip(s, p, 'A EXECUÇÃO CABE NO ESTÁGIO 04', 1010, 665, C.human_decision, { maxWidth: 500 });
  t(s, p, 'O quinto estágio confronta a entrega com o contrato de saída.', 56, 740, {
    size: 32, color: C.muted, maxWidth: 1050, against: C.background,
  });
}

export const renderers = {
  'skills.01_descoberta_e_selecao': skillSelection,
  'skills.02_skill_helpers_runtime': skillRuntimeCutaway,
  'prompts.01_mapa_familias': promptFamilyRouter,
  'prompts.02_fluxo_operacional': promptFiveStages,
};

function hexToRgb(value) {
  const h = value.replace('#', '');
  return [0, 2, 4].map(i => Number.parseInt(h.slice(i, i + 2), 16) / 255);
}

function relativeLuminance(value) {
  return hexToRgb(value)
    .map(v => (v <= 0.04045 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4))
    .reduce((sum, v, i) => sum + v * [0.2126, 0.7152, 0.0722][i], 0);
}

function contrastRatio(a, b) {
  const [hi, lo] = [relativeLuminance(a), relativeLuminance(b)].sort((x, y) => y - x);
  return (hi + 0.05) / (lo + 0.05);
}

function validateState(s, preset) {
  const minimum = preset === 'readme_standard' ? 28 : 32;
  for (const item of s.texts) {
    if (item.essential && item.size < minimum) {
      throw new Error(`Texto essencial abaixo do mínimo (${item.size} < ${minimum}): ${item.text}`);
    }
  }
  for (const item of s.contrastAudit ?? []) {
    const ratio = contrastRatio(item.color, item.against);
    if (ratio < 4.5) throw new Error(`Contraste ${ratio.toFixed(2)} em: ${item.text}`);
  }
  const essential = s.texts.filter(item => item.essential);
  const overlaps = [];
  for (let i = 0; i < essential.length; i += 1) {
    for (let j = i + 1; j < essential.length; j += 1) {
      const a = essential[i], b = essential[j];
      const overlapX = Math.min(a.x + a.width, b.x + b.width) - Math.max(a.x, b.x);
      const overlapY = Math.min(a.y + a.height, b.y + b.height) - Math.max(a.y, b.y);
      if (overlapX > 1 && overlapY > 1) overlaps.push([a.text, b.text]);
    }
  }
  if (overlaps.length) throw new Error(`Sobreposição de texto: ${JSON.stringify(overlaps)}`);
}

async function renderMethods() {
  const contracts = (await readYaml(path.join(ASSET, 'specs/visual_contracts.yaml'))).contracts;
  const records = [];
  for (const [id, renderer] of Object.entries(renderers)) {
    const contract = contracts.find(item => item.id === id);
    if (!contract) throw new Error(`Contrato ausente: ${id}`);
    const presetName = contract.render_targets[0];
    const preset = (await readYaml(path.join(ASSET, 'visual_system/tokens.yaml'))).presets[presetName];
    const state = newCanvas(preset.width, preset.height, contract.alt);
    await renderer(state, contract, 'readme');
    validateState(state, presetName);
    const svg = `${state.draw.svg()}\n`;
    const stem = id.replace('.', '_');
    const svgRel = `readme/${stem}.svg`;
    const pngRel = `readme/${stem}.png`;
    const sampleRel = `qa/${stem}_720.png`;
    await write(path.join(OUTPUT, svgRel), svg);
    const png = await sharp(Buffer.from(svg)).png({ compressionLevel: 9 }).toBuffer();
    await write(path.join(OUTPUT, pngRel), png);
    const sample = await sharp(png).resize({ width: 720 }).png({ compressionLevel: 9 }).toBuffer();
    await write(path.join(OUTPUT, sampleRel), sample);
    records.push({
      id,
      contract: contract.id,
      preset: presetName,
      width: preset.width,
      height: preset.height,
      alt: contract.alt,
      caption: contract.caption,
      svg: svgRel,
      png: pngRel,
      sample_720: sampleRel,
      svg_sha256: sha(Buffer.from(svg)),
      png_sha256: sha(png),
      text: state.texts,
      contrast: state.contrastAudit.map(item => ({
        ...item,
        ratio: Number(contrastRatio(item.color, item.against).toFixed(2)),
      })),
      icons: [...new Set(state.icons)],
    });
  }
  await write(path.join(OUTPUT, 'manifest.json'), `${JSON.stringify({
    schema_version: 1,
    status: 'staging_for_independent_audit',
    generated_by: path.relative(ROOT, fileURLToPath(import.meta.url)).replaceAll('\\', '/'),
    assets: records,
  }, null, 2)}\n`);
  process.stdout.write(`Rendered ${records.length} method figures in ${path.relative(ROOT, OUTPUT)}\n`);
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  await renderMethods();
}
