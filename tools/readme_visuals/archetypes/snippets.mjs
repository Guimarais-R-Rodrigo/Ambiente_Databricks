import {
  C,
  txt,
  lines,
  icon,
  line,
  arrow,
  tag,
} from '../lib.mjs';

function chrome(s, label, title, subtitle, { standard = false, tagSize = 24 } = {}) {
  const p = s.draw.group();
  tag(s, p, label, 54, 28, { color: C.hub_custom, size: tagSize, essential: false });
  txt(s, p, title, 54, 106, {
    size: 40,
    weight: 700,
    maxWidth: standard ? 1290 : 1492,
  });
  txt(s, p, subtitle, 54, 150, {
    size: standard ? 28 : 32,
    color: C.muted,
    maxWidth: standard ? 1290 : 1492,
  });
  line(p, 54, 177, s.width - 54, 177, { width: 2 });
  return p;
}

function sheet(p, x, y, w, h, color) {
  const fold = 50;
  p.path(`M ${x} ${y} H ${x + w - fold} L ${x + w} ${y + fold} V ${y + h} H ${x} Z`)
    .fill(C.panel)
    .stroke({ color, width: 3, linejoin: 'round' });
  p.path(`M ${x + w - fold} ${y} V ${y + fold} H ${x + w}`)
    .fill(C.panel_high)
    .stroke({ color, width: 2, linejoin: 'round' });
}

async function anatomy(s, c, mode = 'readme') {
  const p = chrome(
    s,
    'HUB SNIPPETS · ESTRUTURA FÍSICA',
    'Uma pasta. Três responsabilidades.',
    'A estrutura separa contrato público, implementação e demonstração.',
    { standard: true },
  );

  // Folder silhouette makes containment explicit; the three artifacts are
  // deliberately exploded instead of being presented as sequential cards.
  p.path('M 58 246 H 284 L 326 211 H 810 L 850 251 V 828 H 58 Z')
    .fill(C.dossier_back)
    .stroke({ color: C.line, width: 3, linejoin: 'round' });
  p.path('M 80 276 H 824 V 808 H 80 Z')
    .fill(C.dossier_middle)
    .stroke({ color: C.hub_custom, width: 2 });
  txt(s, p, 'pasta do snippet', 105, 318, {
    size: 28,
    weight: 700,
    color: C.hub_custom,
    maxWidth: 260,
  });

  sheet(p, 112, 345, 620, 132, C.supporting_method);
  await icon(s, p, 'door-open', 141, 383, 46, C.supporting_method);
  txt(s, p, '__init__.py', 215, 397, { size: 36, weight: 800, maxWidth: 455 });
  txt(s, p, 'reexporta a API pública', 215, 442, {
    size: 28,
    color: C.muted,
    maxWidth: 455,
  });

  sheet(p, 151, 500, 620, 144, C.hub_custom);
  await icon(s, p, 'braces', 180, 542, 46, C.hub_custom);
  txt(s, p, 'nome_do_snippet.py', 254, 557, {
    size: 34,
    weight: 800,
    maxWidth: 452,
  });
  txt(s, p, 'lógica, validações e docstring', 254, 605, {
    size: 28,
    color: C.muted,
    maxWidth: 475,
  });

  // A tabbed canvas differentiates the executable notebook from source files.
  p.path('M 190 682 H 360 L 386 655 H 810 V 812 H 190 Z')
    .fill(C.panel)
    .stroke({ color: C.human_decision, width: 3, linejoin: 'round' });
  line(p, 190, 718, 810, 718, { color: C.human_decision, width: 2 });
  await icon(s, p, 'notebook-tabs', 219, 744, 44, C.human_decision);
  txt(s, p, 'exemplo_nome_do_snippet.py', 292, 757, {
    size: 30,
    weight: 800,
    maxWidth: 480,
  });
  txt(s, p, 'dados sintéticos, chamada e saída', 292, 796, {
    size: 28,
    color: C.muted,
    maxWidth: 500,
  });

  txt(s, p, 'RESPONSABILIDADES', 905, 235, {
    size: 24,
    weight: 700,
    color: C.quiet,
    essential: false,
    maxWidth: 390,
  });
  const roles = [
    {
      y: 338,
      color: C.supporting_method,
      number: '01',
      title: 'Fachada previsível',
      copy: ['import curto e estável', 'sem expor a organização interna'],
    },
    {
      y: 510,
      color: C.hub_custom,
      number: '02',
      title: 'Motor revisável',
      copy: ['assinatura real no código', 'lógica e limites verificáveis'],
    },
    {
      y: 688,
      color: C.human_decision,
      number: '03',
      title: 'Guia executável',
      copy: ['exemplo exercita o contrato', 'compatibilidade depende', 'do runtime e do volume'],
    },
  ];
  const sourceY = [411, 572, 744];
  roles.forEach((role, i) => {
    line(p, 812, sourceY[i], 876, sourceY[i], {
      color: role.color,
      width: 3,
      dash: '5 9',
    });
    p.circle(12).center(878, sourceY[i]).fill(role.color);
    txt(s, p, role.number, 905, role.y, {
      size: 30,
      weight: 800,
      color: role.color,
      maxWidth: 48,
    });
    txt(s, p, role.title, 969, role.y, {
      size: 30,
      weight: 700,
      maxWidth: 390,
    });
    lines(s, p, role.copy, 905, role.y + 46, {
      size: 28,
      color: C.muted,
      gap: 39,
      maxWidth: 440,
    });
  });
}

function territory(p, pathData, color) {
  p.path(pathData)
    .fill(C.panel)
    .stroke({ color, width: 3, linejoin: 'round' });
}

async function landscape(s, c, mode = 'readme') {
  const p = chrome(
    s,
    'HUB SNIPPETS · PAISAGEM DE CAPACIDADES',
    'Seis territórios de uma mesma biblioteca',
    'Escolha a categoria pela natureza do problema — não por uma ordem fixa.',
  );

  // Contour lines provide a landscape metaphor without creating routes,
  // quantities or an ordering between the six independent categories.
  p.path('M 84 391 C 252 317 379 380 522 319 S 815 254 1000 326 S 1303 393 1516 306')
    .fill('none').stroke({ color: C.line, width: 2, dasharray: '7 13', opacity: .65 });
  p.path('M 74 492 C 233 430 390 503 538 446 S 829 398 1012 455 S 1300 527 1526 449')
    .fill('none').stroke({ color: C.line, width: 2, dasharray: '7 13', opacity: .45 });

  const zones = [
    {
      path: 'M 55 263 C 78 222 119 202 169 207 L 426 202 C 469 209 498 239 493 278 L 500 347 C 493 380 468 400 425 397 L 111 401 C 76 391 55 364 59 330 Z',
      x: 91, y: 258, color: C.supporting_method, icon: 'brain-circuit', title: 'ml',
      copy: ['Machine Learning', 'e estatística aplicada'],
    },
    {
      path: 'M 548 257 C 567 220 598 199 646 203 L 959 201 C 1006 207 1035 234 1032 279 L 1036 342 C 1021 376 993 396 947 392 L 624 398 C 579 391 548 365 552 326 Z',
      x: 606, y: 250, color: C.databricks_native, icon: 'network', title: 'spark',
      copy: ['operações distribuídas', 'em escala'],
    },
    {
      path: 'M 1074 274 C 1088 231 1125 204 1173 202 L 1474 205 C 1519 211 1546 244 1541 286 L 1546 346 C 1536 379 1504 399 1462 395 L 1141 401 C 1098 393 1074 364 1078 326 Z',
      x: 1138, y: 258, color: C.result_evidence, icon: 'table-2', title: 'display',
      copy: ['exibição e tabelas', 'formatadas'],
    },
    {
      path: 'M 55 513 C 70 477 103 451 146 454 L 441 451 C 483 459 511 489 506 530 L 512 625 C 503 656 478 674 437 669 L 105 674 C 71 661 54 638 59 602 Z',
      x: 91, y: 516, color: C.hub_custom, icon: 'chart-no-axes-combined', title: 'visual',
      copy: ['identidade visual', 'e design em Plotly'],
    },
    {
      path: 'M 548 503 C 566 469 601 451 646 455 L 957 451 C 1003 458 1035 488 1030 527 L 1036 623 C 1025 653 996 674 953 670 L 622 674 C 580 666 548 639 553 598 Z',
      x: 586, y: 516, color: C.human_decision, icon: 'braces', title: 'constants',
      copy: ['formatos brasileiros', 'e estilos compartilhados'],
    },
    {
      path: 'M 1074 518 C 1088 479 1121 453 1167 455 L 1476 451 C 1519 458 1546 489 1541 531 L 1546 621 C 1537 653 1506 674 1464 669 L 1130 674 C 1097 663 1074 638 1079 598 Z',
      x: 1112, y: 516, color: C.supporting_method, icon: 'flask-conical', title: 'testing',
      copy: ['dados sintéticos', 'e fixtures'],
    },
  ];
  for (const zone of zones) {
    territory(p, zone.path, zone.color);
    await icon(s, p, zone.icon, zone.x, zone.y - 17, 52, zone.color);
    txt(s, p, zone.title, zone.x + 77, zone.y + 20, {
      size: 38,
      weight: 800,
      maxWidth: 285,
    });
    lines(s, p, zone.copy, zone.x, zone.y + 74, {
      size: 32,
      color: C.muted,
      gap: 42,
      maxWidth: 390,
    });
  }
}

async function journey(s, c, mode = 'readme') {
  const p = chrome(
    s,
    'HUB SNIPPETS · JORNADA NO NOTEBOOK',
    'Do exemplo à evidência reproduzível',
    'Quatro decisões explícitas mantêm o reuso sob controle.',
    { tagSize: 32 },
  );

  // One tabbed notebook surface replaces the former card-arrow-card sequence.
  p.path('M 54 247 H 344 L 379 215 H 1546 V 676 H 54 Z')
    .fill(C.panel)
    .stroke({ color: C.line, width: 3, linejoin: 'round' });
  p.path('M 54 247 H 1546 V 303 H 54 Z').fill(C.panel_high);
  p.circle(13).center(88, 275).fill(C.danger);
  p.circle(13).center(118, 275).fill(C.human_decision);
  p.circle(13).center(148, 275).fill(C.result_evidence);
  await icon(s, p, 'notebook-tabs', 194, 254, 42, C.databricks_native);
  txt(s, p, 'notebook de consumo', 254, 281, {
    size: 32,
    weight: 700,
    maxWidth: 380,
  });

  // The rail is a real sequence: one action/data path with a single direction.
  arrow(p, [[175, 385], [1405, 385]], { color: C.databricks_native, width: 6 });
  const steps = [
    {
      x: 215, number: '01', color: C.supporting_method, icon: 'book-open-check',
      title: 'Consultar', copy: ['abra exemplo_*.py', 'premissas e saída'],
    },
    {
      x: 585, number: '02', color: C.human_decision, icon: 'settings-2',
      title: 'Configurar', copy: ['torne a raiz visível', 'confirme dependências'],
    },
    {
      x: 970, number: '03', color: C.hub_custom, icon: 'play',
      title: 'Importar + executar', copy: ['execute a API pública', 'com parâmetros reais'],
    },
    {
      x: 1340, number: '04', color: C.result_evidence, icon: 'badge-check',
      title: 'Interpretar', copy: ['tipo, schema e unidade', 'limites e população'],
    },
  ];
  for (const step of steps) {
    p.circle(82).center(step.x, 385).fill(C.background_elevated).stroke({ color: step.color, width: 4 });
    await icon(s, p, step.icon, step.x - 24, 361, 48, step.color);
    txt(s, p, step.number, step.x, 460, {
      size: 24,
      weight: 800,
      color: step.color,
      align: 'center',
      essential: false,
    });
    txt(s, p, step.title, step.x, 510, {
      size: 34,
      weight: 800,
      align: 'center',
      maxWidth: 350,
    });
    lines(s, p, step.copy, step.x, 558, {
      size: 32,
      color: C.muted,
      align: 'center',
      anchor: 'middle',
      gap: 44,
      maxWidth: 360,
    });
  }
  txt(s, p, 'O código copiável permanece no README e no notebook modelo.', 800, 654, {
    size: 32,
    color: C.muted,
    align: 'center',
    maxWidth: 1040,
  });
}

async function bridge(s, c, mode = 'readme') {
  const p = chrome(
    s,
    'HUB SNIPPETS · CONTRATO DE REUSO',
    'Três apoios sustentam um reuso confiável',
    'Dependências, efeitos, parâmetros, limites e resultados permanecem observáveis.',
  );

  // Suspension lines and a single deck create a literal bridge. The API contract
  // is supported by three technical pillars; no person is drawn as infrastructure.
  p.path('M 92 336 C 360 215 565 215 800 336 C 1035 215 1240 215 1508 336')
    .fill('none').stroke({ color: C.databricks_native, width: 5, linecap: 'round' });
  for (const x of [118, 350, 575, 800, 1025, 1250, 1482]) {
    const top = x === 800 ? 336 : 336 - Math.abs(800 - x) * .16;
    line(p, x, top, x, 351, { color: C.databricks_native, width: 3 });
  }
  p.path('M 74 346 H 1526 L 1488 410 H 112 L 74 346 Z')
    .fill(C.panel_high).stroke({ color: C.hub_custom, width: 3, linejoin: 'round' });
  txt(s, p, 'REUSO CONFIÁVEL', 800, 389, {
    size: 36,
    weight: 800,
    color: C.text,
    align: 'center',
    maxWidth: 500,
  });

  const pillars = [
    {
      x: 110, w: 390, color: C.databricks_native, icon: 'scan-face',
      phase: 'ANTES DA CHAMADA', title: ['Interface', 'previsível'],
      copy: ['API pública', 'parâmetros explícitos', 'retorno e erros'],
    },
    {
      x: 605, w: 390, color: C.human_decision, icon: 'cpu',
      phase: 'DURANTE A CHAMADA', title: ['Execução', 'consciente'],
      copy: ['dependências', 'efeitos e mutações', 'custo e compute'],
    },
    {
      x: 1100, w: 390, color: C.result_evidence, icon: 'file-check-2',
      phase: 'DEPOIS DA CHAMADA', title: ['Evidência', 'reproduzível'],
      copy: ['resultado interpretado', 'limites declarados', 'teste reproduzível'],
    },
  ];
  for (const pillar of pillars) {
    p.path(`M ${pillar.x} 408 H ${pillar.x + pillar.w} L ${pillar.x + pillar.w - 34} 700 H ${pillar.x + 34} Z`)
      .fill(C.panel)
      .stroke({ color: pillar.color, width: 3, linejoin: 'round' });
    p.rect(pillar.w - 68, 10).move(pillar.x + 34, 690).fill(pillar.color);
    await icon(s, p, pillar.icon, pillar.x + 30, 446, 48, pillar.color);
    txt(s, p, pillar.phase, pillar.x + 98, 461, {
      size: 22,
      weight: 700,
      color: pillar.color,
      essential: false,
      maxWidth: pillar.w - 118,
    });
    lines(s, p, pillar.title, pillar.x + 30, 514, {
      size: 32,
      weight: 800,
      gap: 42,
      maxWidth: pillar.w - 60,
    });
    lines(s, p, pillar.copy, pillar.x + 30, 600, {
      size: 32,
      color: C.muted,
      gap: 42,
      maxWidth: pillar.w - 50,
    });
  }

  // The foundation is visual, not a fourth semantic pillar.
  p.path('M 52 726 C 208 704 356 740 514 720 S 825 704 984 724 S 1288 744 1548 716')
    .fill('none').stroke({ color: C.line, width: 3, dasharray: '9 14', opacity: .8 });
}

export const renderers = {
  'snippets.01_anatomia_pasta': anatomy,
  'snippets.02_mapa_categorias': landscape,
  'snippets.03_fluxo_operacional': journey,
  'snippets.04_contrato_de_reuso': bridge,
};
