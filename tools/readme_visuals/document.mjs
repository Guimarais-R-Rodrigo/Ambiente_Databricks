import fs from 'node:fs/promises';
import path from 'node:path';
import {ASSET,OUT,readYaml,write} from './lib.mjs';
const contracts=(await readYaml(path.join(ASSET,'specs/visual_contracts.yaml'))).contracts;
const manifest=JSON.parse(await fs.readFile(path.join(OUT,'manifest.json'),'utf8'));
let md='# Contratos das 21 figuras\n\nEstas fichas delimitam as sprints futuras. Somente cinco figuras assinatura foram desenhadas na Sprint 0; as demais são contratos semânticos, não entregas gráficas concluídas. Os 22 ativos atuais permanecem congelados no baseline. A proposta futura tem 21 ativos únicos: retirar o fluxo redundante da raiz e substituir a repetição do mapa dentro do guia operacional não autoriza apagar figuras agora.\n\nO nome do ativo é uma chave de manutenção, não um código de decisão arquitetural. Cada figura precisa responder à sua própria pergunta e conservar o conteúdo textual copiável no README. Os seis consumidores físicos pertencem a cinco sprints: os dois READMEs de topo formam a primeira sprint.\n\n## Inventário de produção planejada\n\n| Família | Quantidade | Protótipos nesta sprint |\n|---|---:|---:|\n';
for(const group of ['raiz','assistant','snippets','scripts','skills','prompts'])md+=`| ${group} | ${contracts.filter(c=>c.id.startsWith(group+'.')).length} | ${contracts.filter(c=>c.id.startsWith(group+'.')&&c.prototype).length} |\n`;
md+='\n## Como usar as fichas\n\nAntes de desenhar: conferir fontes, pergunta, mensagem e não objetivos. Durante o desenho: preservar topologia, procedência e limites semânticos. Depois: comparar os rótulos renderizados com a fonte e executar QA. As âncoras atuais foram verificadas literalmente nos READMEs; quando apontam à seção-pai, isso é declarado. Os IDs ASCII propostos ainda não foram inseridos nos documentos.\n\n';
for(const c of contracts){
  md+=`## ${c.id}\n\n**Situação:** ${c.prototype?'protótipo assinatura disponível':'produção reservada à sprint documental'}.\n\n| Contrato | Definição |\n|---|---|\n| Documento responsável | \`${c.owner_readme}\` |\n| Seção preservada | ${c.section} |\n| Pergunta central | ${c.question} |\n| Mensagem obrigatória | ${c.message} |\n| Arquétipo | \`${c.archetype}\` |\n| Escopo semântico | ${c.semantic_scope} |\n| Formatos | ${c.render_targets.join(', ')} |\n| Âncora atual | \`${c.text_equivalent_anchor}\` (${c.anchor_scope==='existing_parent_section'?'seção-pai existente':'seção existente'}) |\n| Âncora ASCII proposta | \`${c.planned_ascii_anchor}\` — migração futura, não aplicada |\n\n### O que esta figura não pode sugerir\n\n${c.non_goals.map(n=>'- '+n).join('\n')}\n\n### Evidência e equivalente textual\n\n${c.fact_sources.map(f=>'- Fonte do projeto: `'+f+'`.').join('\n')}\n\n**Texto alternativo:** ${c.alt}\n\n**Legenda:** ${c.caption}\n\n**Leitura essencial, independente da imagem:** ${c.message}\n\n`;
  const a=manifest.assets.find(a=>a.id===c.id);
  if(a){
    md+='### Rótulos da versão de leitura\n\nEsta transcrição é extraída da renderização e permite conferir conteúdo sem OCR. A ordem é a de construção gráfica, não uma nova sequência operacional.\n\n';
    md+=a.variants[0].texts.map(t=>`- ${t.text}`).join('\n')+'\n\n';
    md+=`[Abrir protótipo](${a.variants[0].png}) · [Abrir apresentação](${a.variants[1].png})\n\n`;
  }
  md+='### Gate da sprint documental\n\nPreservar os tópicos e subtópicos existentes; inserir legenda e equivalente textual próximos; verificar nomes e comportamento na fonte; testar PNG no notebook e links no Markdown; aplicar os limites do sistema visual; registrar aprovação explícita antes de substituir o baseline.\n\n';
}
await write(path.join(OUT,'CONTRATOS_21_FIGURAS.md'),md);
console.log('21 semantic contract sheets generated.');
