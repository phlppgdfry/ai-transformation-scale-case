// Small shared helpers for the charts: SVG creation, a tooltip that only
// uses textContent (labels are data, not markup), and number formatting.
export const NS = "http://www.w3.org/2000/svg";

export function el(tag, attrs = {}, parent) {
  const e = document.createElementNS(NS, tag);
  for (const [k, v] of Object.entries(attrs)) {
    // CSS custom properties are not reliable in SVG presentation attributes,
    // so colour tokens go through the style property instead.
    if ((k === "fill" || k === "stroke") && String(v).includes("var(")) e.style[k] = v;
    else e.setAttribute(k, v);
  }
  if (parent) parent.appendChild(e);
  return e;
}

export function text(parent, x, y, str, attrs = {}) {
  const t = el("text", { x, y, ...attrs }, parent);
  t.textContent = str;
  return t;
}

const tip = document.createElement("div");
tip.className = "tip";
tip.setAttribute("role", "status");
document.body.appendChild(tip);

// rows: [{value, label, color?}] ; title: string
export function showTip(evt, title, rows) {
  tip.replaceChildren();
  const h = document.createElement("div");
  h.textContent = title;
  h.style.fontWeight = "600";
  h.style.marginBottom = "4px";
  tip.appendChild(h);
  for (const r of rows) {
    const line = document.createElement("div");
    if (r.color) {
      const k = document.createElement("span");
      k.className = "key";
      k.style.background = r.color;
      line.appendChild(k);
    }
    const v = document.createElement("strong");
    v.textContent = r.value;
    line.appendChild(v);
    const l = document.createElement("span");
    l.textContent = " " + r.label;
    l.style.color = "var(--muted)";
    line.appendChild(l);
    tip.appendChild(line);
  }
  tip.style.display = "block";
  const x = evt.clientX ?? evt.target.getBoundingClientRect().right;
  const y = evt.clientY ?? evt.target.getBoundingClientRect().top;
  const w = tip.offsetWidth, hgt = tip.offsetHeight;
  tip.style.left = Math.min(window.innerWidth - w - 8, x + 14) + "px";
  tip.style.top = Math.max(8, Math.min(window.innerHeight - hgt - 8, y + 14)) + "px";
}

export function hideTip() { tip.style.display = "none"; }

export const css = (name) => getComputedStyle(document.documentElement).getPropertyValue(name).trim();
export const eur = (x) => x >= 1e6 ? `€${(x / 1e6).toFixed(1)}m` : `€${Math.round(x / 1e3)}k`;
