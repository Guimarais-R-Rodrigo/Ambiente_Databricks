import {
  C,
  txt,
  lines,
  wrap,
  icon,
  line,
  arrow,
  tag,
} from '../lib.mjs';

const WIDE_MIN = 32;
const STANDARD_MIN = 28;

function frame(s, c, kicker, title, mode = 'readme') {
  const p = s.draw;
  const minimum = s.width >= 1600 ? WIDE_MIN : STANDARD_MIN;
  s.contentTransform = { scale: 1, dx: 0, dy: 0 };
  txt(s, p, kicker, 56, 49, {
    size: 24,
    weight: 800,
    color: C.hub_custom,
    essential: false,
  });
  txt(s, p, title, 56, 101, {
    size: s.width >= 1600 ? 42 : 44,
    weight: 800,
    maxWidth: s.width - 112,
  });
  const question = wrap(c.question, s.width - 112, minimum, 400);
  lines(s, p, question, 56, 144, {
    size: minimum,
    color: C.muted,
    maxWidth: s.width - 112,
  });
  const dividerY = question.length > 1 ? 194 : 169;
  line(p, 56, dividerY, s.width - 56, dividerY, { width: 2 });
  if (mode !== 'readme') {
    tag(s, p, 'APRESENTAÇÃO', s.width - 255, 24, {
      color: C.supporting_method,
      size: 20,
      essential: false,
    });
  }
  return { p, minimum, top: dividerY + 24 };
}

function notchedPanel(p, x, y, w, h, { stroke = C.line, fill = C.panel } = {}) {
  return p
    .path(
      `M ${x + 24} ${y} H ${x + w - 24} L ${x + w} ${y + 24} `
      + `V ${y + h} H ${x} V ${y + 24} Z`,
    )
    .fill(fill)
    .stroke({ color: stroke, width: 2, linejoin: 'round' });
}

function dividerLabel(s, p, value, x, y, color, width) {
  txt(s, p, value, x, y, {
    size: 24,
    weight: 800,
    color,
    maxWidth: width,
    essential: false,
  });
}

export async function anatomy(s, c, mode = 'readme') {
  const { p, minimum, top } = frame(
    s,
    c,
    'ANATOMIA · PASTA DE OBJETO',
    'Um Hub Script, por dentro',
    mode,
  );

  // A pasta funciona como estojo técnico. As três peças são removíveis e
  // semanticamente distintas; os trilhos pontilhados indicam pertencimento,
  // não uma sequência obrigatória de execução.
  const caseY = top + 40;
  p.path(
    `M 56 ${caseY + 48} H 242 L 282 ${caseY + 8} H 840 `
    + `Q 870 ${caseY + 8} 870 ${caseY + 38} V ${caseY + 512} `
    + `Q 870 ${caseY + 540} 842 ${caseY + 540} H 56 Z`,
  ).fill(C.dossier_back).stroke({ color: C.hub_custom, width: 3 });
  tag(s, p, 'HUB CUSTOMIZADO · 1 PASTA', 84, caseY + 26, {
    color: C.hub_custom,
    size: 22,
    essential: false,
  });
  p.path(
    `M 121 ${caseY + 128} V ${caseY + 449} `
    + `M 121 ${caseY + 178} H 171 M 121 ${caseY + 323} H 221 `
    + `M 121 ${caseY + 449} H 271`,
  ).fill('none').stroke({
    color: C.line,
    width: 4,
    dasharray: '5 11',
    linecap: 'round',
  });
  dividerLabel(s, p, 'CONTÉM', 84, caseY + 112, C.quiet, 112);

  const modules = [
    {
      x: 170,
      y: caseY + 116,
      w: 608,
      title: '__init__.py',
      role: 'interface pública · reexporta',
      ico: 'plug-zap',
      color: C.supporting_method,
    },
    {
      x: 220,
      y: caseY + 261,
      w: 608,
      title: '<nome>.py',
      role: 'implementação · contrato específico',
      ico: 'file-code-2',
      color: C.hub_custom,
    },
    {
      x: 270,
      y: caseY + 406,
      w: 538,
      title: 'exemplo_<nome>.py',
      role: 'demonstração em notebook',
      ico: 'notebook-tabs',
      color: C.supporting_method,
    },
  ];
  for (const item of modules) {
    notchedPanel(p, item.x, item.y, item.w, 108, {
      stroke: item.color,
      fill: C.panel,
    });
    await icon(s, p, item.ico, item.x + 25, item.y + 28, 48, item.color);
    txt(s, p, item.title, item.x + 94, item.y + 48, {
      size: minimum + 2,
      weight: 700,
      maxWidth: item.w - 120,
    });
    txt(s, p, item.role, item.x + 94, item.y + 88, {
      size: minimum,
      color: C.muted,
      maxWidth: item.w - 120,
    });
  }

  arrow(p, [[808, caseY + 315], [932, caseY + 315]], {
    color: C.result_evidence,
    width: 4,
  });
  dividerLabel(s, p, 'DEFINE', 832, caseY + 292, C.result_evidence, 90);

  const outX = 932;
  const outW = 412;
  notchedPanel(p, outX, caseY + 66, outW, 474, {
    stroke: C.result_evidence,
    fill: C.background_elevated,
  });
  await icon(s, p, 'file-output', outX + 28, caseY + 95, 50, C.result_evidence);
  txt(s, p, 'SAÍDA DO OBJETO', outX + 96, caseY + 126, {
    size: minimum,
    weight: 800,
    color: C.result_evidence,
    maxWidth: outW - 120,
  });
  lines(s, p, ['A ferramenta escolhida', 'define a forma da saída.'], outX + 30, caseY + 187, {
    size: minimum,
    color: C.muted,
    gap: 38,
    maxWidth: outW - 60,
  });
  line(p, outX + 30, caseY + 240, outX + outW - 30, caseY + 240, { width: 2 });

  const outputs = [
    'dict · contratos próprios',
    'Spark DataFrame · RFV',
    'texto · YAML ou JSON',
    'lista · violações',
  ];
  for (let index = 0; index < outputs.length; index += 1) {
    const yy = caseY + 290 + index * 49;
    p.circle(10).center(outX + 36, yy - 8).fill(C.result_evidence);
    txt(s, p, outputs[index], outX + 58, yy, {
      size: minimum,
      weight: 700,
      maxWidth: outW - 80,
    });
  }
  tag(s, p, 'SEM RETORNO UNIVERSAL', outX + 30, caseY + 486, {
    color: C.human_decision,
    size: 22,
    essential: false,
  });

  txt(
    s,
    p,
    'O exemplo demonstra; o consumidor interpreta o contrato da ferramenta escolhida.',
    700,
    866,
    {
      size: minimum,
      align: 'center',
      color: C.muted,
      maxWidth: 1288,
    },
  );
}

export async function returnsPanorama(s, c, mode = 'readme') {
  const { p, minimum, top } = frame(
    s,
    c,
    'PANORAMA · CONTRATOS DE RETORNO',
    'Sete ferramentas, quatro formas de saída',
    mode,
  );

  const flowY = top + 16;
  notchedPanel(p, 56, flowY, 390, 145, {
    stroke: C.hub_custom,
    fill: C.panel,
  });
  await icon(s, p, 'database', 82, flowY + 34, 52, C.hub_custom);
  txt(s, p, 'ENTRADA', 156, flowY + 49, {
    size: minimum,
    weight: 800,
    maxWidth: 260,
  });
  txt(s, p, 'tabela / arquivo', 156, flowY + 91, {
    size: minimum,
    color: C.muted,
    maxWidth: 260,
  });
  txt(s, p, '+ parâmetros', 156, flowY + 133, {
    size: minimum,
    color: C.muted,
    maxWidth: 290,
  });

  arrow(p, [[446, flowY + 66], [558, flowY + 66]], {
    color: C.hub_custom,
    width: 5,
  });
  p.path(
    `M 592 ${flowY} H 1010 L 1050 ${flowY + 40} V ${flowY + 92} `
    + `L 1010 ${flowY + 132} H 592 L 552 ${flowY + 92} V ${flowY + 40} Z`,
  ).fill(C.panel_high).stroke({ color: C.hub_custom, width: 3 });
  await icon(s, p, 'split', 588, flowY + 39, 48, C.hub_custom);
  txt(s, p, 'Hub Script escolhido', 660, flowY + 57, {
    size: minimum + 2,
    weight: 800,
    maxWidth: 365,
  });
  txt(s, p, 'execução sob demanda', 660, flowY + 103, {
    size: minimum,
    color: C.muted,
    maxWidth: 365,
  });
  arrow(p, [[1050, flowY + 66], [1100, flowY + 66]], {
    color: C.result_evidence,
    width: 5,
  });
  notchedPanel(p, 1100, flowY, 444, 132, {
    stroke: C.result_evidence,
    fill: C.background_elevated,
  });
  await icon(s, p, 'waypoints', 1128, flowY + 36, 50, C.result_evidence);
  lines(
    s,
    p,
    ['Cada função define', 'o contrato de saída.'],
    1200,
    flowY + 55,
    {
      size: minimum,
      weight: 600,
      color: C.muted,
      gap: 41,
      maxWidth: 316,
    },
  );

  const outputY = flowY + 171;
  const outputH = 356;
  const cards = [
    { x: 56, w: 600, stroke: C.result_evidence },
    { x: 672, w: 260, stroke: C.result_evidence },
    { x: 948, w: 290, stroke: C.supporting_method },
    { x: 1254, w: 290, stroke: C.human_decision },
  ];
  cards.forEach(card => notchedPanel(p, card.x, outputY, card.w, outputH, {
    stroke: card.stroke,
    fill: C.panel,
  }));

  await icon(s, p, 'braces', 82, outputY + 28, 46, C.result_evidence);
  txt(s, p, 'DICT · CONTRATOS PRÓPRIOS', 148, outputY + 61, {
    size: minimum,
    weight: 800,
    color: C.result_evidence,
    maxWidth: 480,
  });
  line(p, 78, outputY + 84, 634, outputY + 84, { width: 2 });
  const dictRows = [
    ['data_quality_check', 'qualidade'],
    ['quick_profile', 'perfil'],
    ['drift_detector', 'PSI + classe*'],
    ['doc_coverage', 'cobertura'],
  ];
  for (let index = 0; index < dictRows.length; index += 1) {
    const [name, value] = dictRows[index];
    const yy = outputY + 133 + index * 51;
    txt(s, p, name, 78, yy, {
      size: minimum,
      weight: 600,
      maxWidth: 304,
    });
    txt(s, p, value, 634, yy, {
      size: minimum,
      color: C.muted,
      align: 'right',
      maxWidth: 224,
    });
  }
  txt(s, p, '* classificação exige limiares', 78, outputY + 334, {
    size: minimum,
    color: C.muted,
    maxWidth: 540,
  });

  const singular = [
    {
      x: 672,
      w: 260,
      icon: 'table-2',
      color: C.result_evidence,
      kind: ['SPARK', 'DATAFRAME'],
      name: 'rfv_calculator',
      detail: ['features RFV', 'por entidade'],
    },
    {
      x: 948,
      w: 290,
      icon: 'file-json-2',
      color: C.supporting_method,
      kind: ['TEXTO'],
      name: 'schema_to_yaml',
      detail: ['YAML ou JSON', 'sem persistir'],
    },
    {
      x: 1254,
      w: 290,
      icon: 'list-checks',
      color: C.human_decision,
      kind: ['LISTA'],
      name: 'naming_checker',
      detail: ['violações', 'de nomenclatura'],
    },
  ];
  for (const item of singular) {
    await icon(s, p, item.icon, item.x + 24, outputY + 30, 48, item.color);
    txt(s, p, item.kind[0], item.x + 88, outputY + 60, {
      size: minimum,
      weight: 800,
      color: item.color,
      maxWidth: item.w - 112,
    });
    if (item.kind.length > 1) {
      txt(s, p, item.kind[1], item.x + item.w / 2, outputY + 111, {
        size: minimum,
        weight: 800,
        color: item.color,
        align: 'center',
        maxWidth: item.w - 44,
      });
    }
    line(p, item.x + 22, outputY + 132, item.x + item.w - 22, outputY + 132, { width: 2 });
    txt(s, p, item.name, item.x + item.w / 2, outputY + 194, {
      size: minimum,
      weight: 700,
      align: 'center',
      maxWidth: item.w - 24,
    });
    lines(s, p, item.detail, item.x + item.w / 2, outputY + 250, {
      size: minimum,
      color: C.muted,
      align: 'center',
      gap: 42,
      maxWidth: item.w - 24,
    });
  }
}

export async function operationalZones(s, c, mode = 'readme') {
  const { p, minimum, top } = frame(
    s,
    c,
    'RESPONSABILIDADES · LIMITES OPERACIONAIS',
    'Medir, decidir e orquestrar são camadas diferentes',
    mode,
  );

  const centerY = top + 236;
  // Instrumento circular: a metáfora é medição sob demanda, não dashboard vivo.
  p.circle(304).center(220, centerY).fill(C.panel).stroke({ color: C.hub_custom, width: 4 });
  p.circle(252).center(220, centerY).fill(C.background_elevated).stroke({ color: C.line, width: 2 });
  p.path(`M 112 ${centerY} A 108 108 0 0 1 328 ${centerY}`).fill('none').stroke({
    color: C.hub_custom,
    width: 6,
    linecap: 'round',
  });
  await icon(s, p, 'scan-search', 187, centerY - 112, 66, C.hub_custom);
  txt(s, p, '1 · MEDIR', 220, centerY + 2, {
    size: minimum + 4,
    weight: 800,
    align: 'center',
    color: C.hub_custom,
  });
  txt(s, p, 'Hub Script', 220, centerY + 45, {
    size: minimum,
    weight: 600,
    align: 'center',
    maxWidth: 270,
  });
  txt(s, p, 'de diagnóstico', 220, centerY + 87, {
    size: minimum,
    color: C.muted,
    align: 'center',
    maxWidth: 270,
  });
  txt(s, p, 'lê · calcula', 220, centerY + 129, {
    size: minimum,
    color: C.muted,
    align: 'center',
    maxWidth: 270,
  });
  dividerLabel(s, p, 'HUB CUSTOMIZADO', 139, centerY + 202, C.hub_custom, 250);

  arrow(p, [[372, centerY], [485, centerY]], { color: C.result_evidence, width: 5 });
  dividerLabel(s, p, 'SAÍDA', 397, centerY - 21, C.result_evidence, 90);

  // Recibo de evidência: forma documental distinta do instrumento e do gate.
  p.path(
    `M 485 ${centerY - 154} H 738 L 780 ${centerY - 112} `
    + `V ${centerY + 154} H 485 Z`,
  ).fill(C.panel).stroke({ color: C.result_evidence, width: 3 });
  p.path(`M 738 ${centerY - 154} V ${centerY - 112} H 780`).fill(C.panel_high).stroke({
    color: C.result_evidence,
    width: 2,
  });
  await icon(s, p, 'file-output', 517, centerY - 121, 48, C.result_evidence);
  txt(s, p, 'EVIDÊNCIA', 580, centerY - 88, {
    size: minimum,
    weight: 800,
    color: C.result_evidence,
    maxWidth: 180,
  });
  lines(s, p, ['métricas', 'alertas', 'classificações', 'ou estruturas'], 517, centerY - 23, {
    size: minimum,
    color: C.muted,
    gap: 45,
    maxWidth: 220,
  });

  arrow(p, [[780, centerY], [874, centerY]], { color: C.human_decision, width: 5 });
  dividerLabel(s, p, 'DECIDE', 780, centerY - 21, C.human_decision, 90);

  // Gate angular: a política é deliberadamente externa ao script.
  p.polygon(
    `${982},${centerY - 116} ${1098},${centerY} ${982},${centerY + 116} ${866},${centerY}`,
  ).fill(C.background_elevated).stroke({ color: C.human_decision, width: 4 });
  await icon(s, p, 'sliders-horizontal', 953, centerY - 78, 58, C.human_decision);
  txt(s, p, '2 · POLÍTICA', 982, centerY + 16, {
    size: minimum,
    weight: 800,
    align: 'center',
    color: C.human_decision,
    maxWidth: 205,
  });
  txt(s, p, 'código consumidor', 982, centerY + 166, {
    size: minimum,
    align: 'center',
    color: C.muted,
    maxWidth: 300,
  });

  arrow(p, [[1098, centerY], [1172, centerY]], {
    color: C.databricks_native,
    dash: '10 9',
    width: 5,
  });

  // Plano operacional Databricks em camadas, evitando aparência de um único
  // serviço obrigatório ou disponibilidade universal.
  p.path(
    `M 1172 ${centerY - 164} H 1512 L 1544 ${centerY - 132} `
    + `V ${centerY + 154} H 1172 Z`,
  ).fill(C.panel).stroke({ color: C.databricks_native, width: 3 });
  p.path(`M 1190 ${centerY - 180} H 1494 L 1512 ${centerY - 162} H 1172 Z`).fill(C.panel_high).stroke({
    color: C.databricks_native,
    width: 2,
  });
  await icon(s, p, 'server-cog', 1200, centerY - 133, 50, C.databricks_native);
  tag(s, p, 'QUANDO CONFIGURADO', 1272, centerY - 65, {
    color: C.databricks_native,
    size: 20,
    essential: false,
  });
  txt(s, p, '3 · ORQUESTRAR', 1258, centerY - 98, {
    size: minimum,
    weight: 800,
    color: C.databricks_native,
    maxWidth: 274,
  });
  const services = ['expectations', 'event log', 'Lakeflow Jobs'];
  for (let index = 0; index < services.length; index += 1) {
    const yy = centerY + 24 + index * 55;
    line(p, 1202, yy + 15, 1226, yy + 15, { color: C.databricks_native, width: 5 });
    txt(s, p, services[index], 1244, yy + 12, {
      size: minimum,
      weight: 700,
      maxWidth: 270,
    });
  }
  dividerLabel(
    s,
    p,
    'VERIFIQUE NO WORKSPACE',
    1198,
    centerY + 190,
    C.quiet,
    335,
  );

  const guardY = 685;
  line(p, 56, guardY - 42, 1544, guardY - 42, { color: C.danger, width: 2, dash: '8 10' });
  const guards = [
    [86, 'não agenda sozinho'],
    [568, 'não notifica sozinho'],
    [1050, 'não interrompe sozinho'],
  ];
  for (const [x, value] of guards) {
    p.circle(36).center(x, guardY).fill(C.background_elevated).stroke({ color: C.danger, width: 3 });
    line(p, x - 10, guardY - 10, x + 10, guardY + 10, { color: C.danger, width: 4 });
    line(p, x + 10, guardY - 10, x - 10, guardY + 10, { color: C.danger, width: 4 });
    txt(s, p, value, x + 34, guardY + 10, {
      size: minimum,
      weight: 700,
      color: C.muted,
      maxWidth: 380,
    });
  }
}

export async function dataQualityVerdict(s, c, mode = 'readme') {
  const { p, minimum, top } = frame(
    s,
    c,
    'DATA_QUALITY_CHECK · ESTADOS E POLÍTICA',
    'Três estados irmãos; um gate separado',
    mode,
  );

  const sourceY = top + 25;
  notchedPanel(p, 56, sourceY, 440, 438, {
    stroke: C.hub_custom,
    fill: C.panel,
  });
  tag(s, p, 'RETORNO ESPECÍFICO', 82, sourceY + 25, {
    color: C.hub_custom,
    size: 22,
    essential: false,
  });
  await icon(s, p, 'shield-check', 82, sourceY + 91, 54, C.hub_custom);
  txt(s, p, 'data_quality_check', 154, sourceY + 128, {
    size: minimum,
    weight: 800,
    maxWidth: 310,
  });
  txt(s, p, 'dict', 82, sourceY + 178, {
    size: minimum + 4,
    weight: 800,
    color: C.result_evidence,
  });
  const fields = ['status', 'score', 'thresholds', 'checks', 'alerts'];
  for (let index = 0; index < fields.length; index += 1) {
    const yy = sourceY + 222 + index * 42;
    p.circle(8).center(90, yy - 8).fill(C.result_evidence);
    txt(s, p, fields[index], 110, yy, {
      size: minimum,
      color: C.muted,
      maxWidth: 220,
    });
  }
  dividerLabel(s, p, 'ESTADOS · SÓ NESTE SCRIPT', 82, sourceY + 426, C.quiet, 360);

  const busX = 530;
  const stateX = 600;
  const stateTextX = 670;
  const stateYs = [sourceY + 55, sourceY + 219, sourceY + 383];
  line(p, 496, sourceY + 219, busX, sourceY + 219, { color: C.line, width: 5 });
  line(p, busX, stateYs[0], busX, stateYs[2], { color: C.line, width: 5 });
  stateYs.forEach(yy => arrow(p, [[busX, yy], [stateX - 38, yy]], { color: C.line, width: 4 }));

  const gateCenterX = 1088;
  const gateCenterY = sourceY + 219;
  const states = [
    {
      y: stateYs[0],
      name: 'PASS',
      color: C.result_evidence,
      shape: 'circle',
      icon: 'circle-check',
      copy: ['regras executadas', 'sem violação'],
      gate: [gateCenterX - 38, gateCenterY - 58],
    },
    {
      y: stateYs[1],
      name: 'WARN',
      color: C.human_decision,
      shape: 'triangle',
      icon: 'triangle-alert',
      copy: ['há uma condição', 'que exige atenção'],
      gate: [gateCenterX - 96, gateCenterY],
    },
    {
      y: stateYs[2],
      name: 'FAIL',
      color: C.danger,
      shape: 'diamond',
      icon: 'x',
      copy: ['uma regra de falha', 'foi violada'],
      gate: [gateCenterX - 38, gateCenterY + 58],
    },
  ];

  // Conectores chegam ao mesmo gate; nenhum estado conduz ao estado seguinte.
  for (const state of states) {
    arrow(p, [[962, state.y], state.gate], {
      color: state.color,
      width: 4,
    });
  }
  for (const state of states) {
    if (state.shape === 'circle') {
      p.circle(76).center(stateX, state.y).fill(C.background_elevated).stroke({ color: state.color, width: 4 });
    } else if (state.shape === 'triangle') {
      p.polygon(`${stateX},${state.y - 45} ${stateX + 43},${state.y + 37} ${stateX - 43},${state.y + 37}`)
        .fill(C.background_elevated).stroke({ color: state.color, width: 4, linejoin: 'round' });
    } else {
      p.polygon(`${stateX},${state.y - 43} ${stateX + 43},${state.y} ${stateX},${state.y + 43} ${stateX - 43},${state.y}`)
        .fill(C.background_elevated).stroke({ color: state.color, width: 4 });
    }
    await icon(s, p, state.icon, stateX - 23, state.y - 23, 46, state.color);
    txt(s, p, state.name, stateTextX, state.y - 7, {
      size: minimum + 4,
      weight: 800,
      color: state.color,
      maxWidth: 145,
    });
    lines(s, p, state.copy, stateTextX, state.y + 36, {
      size: minimum,
      color: C.muted,
      gap: 40,
      maxWidth: 310,
    });
  }

  p.polygon(
    `${gateCenterX},${gateCenterY - 92} ${gateCenterX + 96},${gateCenterY} `
    + `${gateCenterX},${gateCenterY + 92} ${gateCenterX - 96},${gateCenterY}`,
  ).fill(C.background_elevated).stroke({ color: C.human_decision, width: 4 });
  await icon(s, p, 'sliders-horizontal', gateCenterX - 25, gateCenterY - 60, 50, C.human_decision);
  lines(s, p, ['POLÍTICA', 'EXTERNA'], gateCenterX, gateCenterY + 13, {
    size: minimum,
    weight: 800,
    color: C.human_decision,
    align: 'center',
    gap: 42,
    maxWidth: 158,
  });

  arrow(p, [[gateCenterX + 96, gateCenterY], [1214, gateCenterY]], {
    color: C.human_decision,
    width: 5,
  });
  notchedPanel(p, 1214, sourceY + 65, 330, 308, {
    stroke: C.human_decision,
    fill: C.panel,
  });
  await icon(s, p, 'git-branch', 1240, sourceY + 95, 48, C.human_decision);
  lines(s, p, ['AÇÃO', 'CODIFICADA'], 1300, sourceY + 116, {
    size: minimum,
    weight: 800,
    color: C.human_decision,
    gap: 42,
    maxWidth: 220,
  });
  const actions = ['prosseguir', 'revisar alertas', 'falhar a tarefa'];
  for (let index = 0; index < actions.length; index += 1) {
    const yy = sourceY + 205 + index * 44;
    line(p, 1244, yy - 8, 1268, yy - 8, { color: C.human_decision, width: 5 });
    txt(s, p, actions[index], 1286, yy, {
      size: minimum,
      color: C.muted,
      maxWidth: 230,
    });
  }
  dividerLabel(s, p, 'DECISÃO EXTERNA', 1240, sourceY + 350, C.quiet, 270);

  tag(s, p, 'PASS NÃO HOMOLOGA', 250, 690, {
    color: C.result_evidence,
    size: minimum,
    essential: true,
  });
  tag(s, p, 'FAIL NÃO INTERROMPE SOZINHO', 842, 690, {
    color: C.danger,
    size: minimum,
    essential: true,
  });
}

export const renderers = {
  'scripts.01_anatomia_pasta': anatomy,
  'scripts.03_panorama_retornos': returnsPanorama,
  'scripts.04_diagnostico_vs_enforcement': operationalZones,
  'scripts.05_veredito_data_quality': dataQualityVerdict,
};
