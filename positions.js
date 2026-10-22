// Positions are observed ranks from the export, not impression-weighted API metrics.
function positionValue(raw) {
  const match = String(raw ?? '').trim().match(/^(?:№\s*)?([1-9]\d*)(?=\s|$|[—–-])/);
  return match ? Number(match[1]) : null;
}
function positionStats(rows) {
  const values = rows.map(r => r.position).filter(n => Number.isInteger(n) && n > 0);
  const n = values.length;
  return {
    n, missing: rows.length - n,
    mean: n ? values.reduce((a, b) => a + b, 0) / n : null,
    first: n ? values.filter(x => x === 1).length / n * 100 : null,
    top3: n ? values.filter(x => x <= 3).length / n * 100 : null,
  };
}
function positionNumber(n) { return n === null ? '—' : n.toLocaleString('ru-RU', {maximumFractionDigits: 2}); }
function positionCells(rows) {
  const s = positionStats(rows);
  return `<td>${positionNumber(s.mean)}</td><td>${s.n}</td><td>${s.missing}</td><td>${positionNumber(s.first)}${s.n ? '%' : ''}</td><td>${positionNumber(s.top3)}${s.n ? '%' : ''}</td>`;
}
function positionTable(headers, body) {
  return `<div class="position-scroll"><table class="position-table"><thead><tr>${headers.map(h => `<th>${h}</th>`).join('')}<th>Средняя позиция ↓</th><th>Замеров</th><th>Без позиции</th><th>Место №1</th><th>Топ-3</th></tr></thead><tbody>${body || `<tr><td colspan="${headers.length + 5}">Нет наблюдений для выбранных условий</td></tr>`}</tbody></table></div>`;
}
