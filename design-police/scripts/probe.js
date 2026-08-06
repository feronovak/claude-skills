/*
 * design-police computed-style probe.
 *
 * Pass the entire contents of this file as the `function` argument to
 * Playwright's browser_evaluate. It returns one JSON object describing every
 * measurable defect on the current page at the current viewport.
 *
 * Why this is a file and not instructions: every audit needs the same numbers,
 * and a formula retyped from memory each run produces a different answer each
 * run. APCA in particular has two polarity branches and a soft-clamp that are
 * easy to drop — dropping them silently mis-scores every light-on-dark button
 * on the page. Measure with this; spend your own effort on judgement instead.
 */
() => {
  // ---------- APCA (W3C 0.1.9) — both polarities, clamp, offset ----------
  const Yof = (c) => {
    const m = (c.match(/[\d.]+/g) || []).map(Number);
    if (m.length < 3) return null;
    if (m.length > 3 && m[3] === 0) return null; // fully transparent
    const f = (v) => Math.pow(v / 255, 2.4);
    return 0.2126729 * f(m[0]) + 0.7151522 * f(m[1]) + 0.0721750 * f(m[2]);
  };
  const clamp = (y) => (y > 0.022 ? y : y + Math.pow(0.022 - y, 1.414));

  function apca(textColor, bgColor) {
    let Yt = Yof(textColor), Yb = Yof(bgColor);
    if (Yt === null || Yb === null) return null;
    Yt = clamp(Yt); Yb = clamp(Yb);
    let S, Lc;
    if (Yb > Yt) {                                   // dark text on light bg
      S = (Math.pow(Yb, 0.56) - Math.pow(Yt, 0.57)) * 1.14;
      Lc = S < 0.1 ? 0 : S - 0.027;
    } else {                                         // light text on dark bg
      S = (Math.pow(Yb, 0.65) - Math.pow(Yt, 0.62)) * 1.14;
      Lc = S > -0.1 ? 0 : S + 0.027;
    }
    return Math.round(Lc * 1000) / 10;
  }

  // Two numbers, deliberately kept apart, because conflating them is how a
  // perfectly legible white-on-blue button gets reported as a defect:
  //
  //   floor  — below this the text is genuinely hard to read. This FAILS.
  //   target — the quality bar you'd hit given a free hand. Never a failure,
  //            reported separately so nobody has to argue about it.
  //
  // Anchored on APCA's published levels (Lc 90 preferred body, 75 minimum
  // body, 60 spot/headline, 45 large-and-bold). Polarity does not change the
  // threshold — compare |Lc|, since APCA already encodes the asymmetry in
  // its two branches.
  function floorLc(px, weight) {
    let f;
    if (px >= 36 || (px >= 24 && weight >= 600)) f = 45;
    else if (px >= 24 || (px >= 18 && weight >= 600)) f = 55;
    else if (px >= 18) f = 60;
    else if (px >= 16) f = 68;
    else f = 75;
    if (weight >= 700) f -= 5;      // heavier strokes read at lower contrast
    else if (weight >= 600) f -= 3;
    return f;
  }

  const SPACING = new Set([0, 2, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 56, 64, 72, 80, 96, 112, 128, 160, 192]);

  const sel = (el) => {
    let s = el.tagName.toLowerCase();
    if (el.id) return s + '#' + el.id;
    const c = (el.getAttribute && el.getAttribute('class')) || '';
    if (c.trim()) s += '.' + c.trim().split(/\s+/)[0];
    return s;
  };
  const vis = (el) => {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || cs.opacity === '0') return false;
    const r = el.getBoundingClientRect();
    return r.width > 0 || r.height > 0;
  };
  function bgOf(el) {
    let n = el;
    while (n && n.nodeType === 1) {
      const c = getComputedStyle(n).backgroundColor;
      const y = Yof(c);
      if (y !== null) return c;
      n = n.parentElement;
    }
    return 'rgb(255, 255, 255)';
  }
  const ownText = (el) =>
    [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim().length > 1);

  const out = {
    url: location.href,
    viewport: { w: innerWidth, h: innerHeight },
    contrast: [], contrastBelowTarget: [],
    spacing: { offScaleValues: [], offScale: [], compliance: null },
    typeScale: { sizes: [], belowFloor: [] },
    touchTargets: [], lineLength: [], clipped: [], occluded: [],
    brokenImages: [], imgMissingDims: [], placeholders: [],
    uppercaseNoTracking: [], horizontalScroll: null, counts: {},
  };

  const all = [...document.querySelectorAll('body *')].filter(vis);
  let spaceTotal = 0, spaceOk = 0;
  const sizes = new Map();

  for (const el of all) {
    const cs = getComputedStyle(el);
    const rect = el.getBoundingClientRect();
    const id = sel(el);

    // ---- spacing scale ----
    for (const p of ['marginTop','marginBottom','marginLeft','marginRight',
                     'paddingTop','paddingBottom','paddingLeft','paddingRight',
                     'rowGap','columnGap']) {
      const raw = cs[p];
      if (!raw || raw === 'normal' || raw.includes('%')) continue;
      const v = parseFloat(raw);
      if (isNaN(v) || v === 0) continue;
      // skip margins that are just auto-centring artefacts
      if ((p === 'marginLeft' || p === 'marginRight') && cs.marginLeft === cs.marginRight && parseFloat(cs.maxWidth) > 0) continue;
      spaceTotal++;
      if (SPACING.has(Math.round(v))) spaceOk++;
      else out.spacing.offScale.push(`${id} ${p}=${raw}`);
    }

    // ---- type ----
    const fs = parseFloat(cs.fontSize);
    const fw = parseInt(cs.fontWeight) || 400;
    if (ownText(el)) {
      sizes.set(fs, (sizes.get(fs) || 0) + 1);
      if (fs < 14) out.typeScale.belowFloor.push(`${id} ${cs.fontSize}`);

      if (cs.textTransform === 'uppercase' && parseFloat(cs.letterSpacing || '0') <= 0)
        out.uppercaseNoTracking.push(`${id} ${cs.fontSize}`);

      // ---- contrast ----
      const bg = bgOf(el);
      const Lc = apca(cs.color, bg);
      if (Lc !== null) {
        const floor = floorLc(fs, fw), target = floor + 15;
        const rec = { el: id, color: cs.color, bg, px: fs, weight: fw, Lc,
                      floor, target,
                      polarity: Lc < 0 ? 'light-on-dark' : 'dark-on-light' };
        if (Math.abs(Lc) < floor) out.contrast.push(rec);
        else if (Math.abs(Lc) < target) out.contrastBelowTarget.push(rec);
      }

      // ---- real rendered line length ----
      try {
        const rng = document.createRange();
        rng.selectNodeContents(el);
        const rects = [...rng.getClientRects()].filter((r) => r.width > 1);
        if (rects.length && el.textContent.trim().length > 100) {
          const widest = Math.max(...rects.map((r) => r.width));
          // measure a real average glyph advance rather than guessing 0.5em
          const probe = document.createElement('span');
          probe.textContent = 'abcdefghijklmnopqrstuvwxyz';
          probe.style.cssText = `position:absolute;visibility:hidden;white-space:pre;font:${cs.font}`;
          document.body.appendChild(probe);
          const adv = probe.getBoundingClientRect().width / 26;
          probe.remove();
          const ch = Math.round(widest / adv);
          if (ch > 80) out.lineLength.push({ el: id, ch, px: Math.round(widest), fontSize: fs });
        }
      } catch (e) { /* range failed on this node */ }

      // ---- placeholder copy ----
      if (/lorem ipsum|dolor sit amet|\bTODO\b|\bFIXME\b|\bTBD\b|placeholder text|coming soon/i.test(el.textContent))
        out.placeholders.push(`${id}: ${el.textContent.trim().slice(0, 70)}`);

      // ---- clipped text ----
      if (el.scrollWidth > el.clientWidth + 1 && el.clientWidth > 0 &&
          !/auto|scroll/.test(cs.overflowX) && cs.textOverflow !== 'ellipsis')
        out.clipped.push({ el: id, textWidth: el.scrollWidth, boxWidth: el.clientWidth,
                           text: el.textContent.trim().slice(0, 50) });
    }

    // ---- touch targets ----
    // Only meaningful where a finger is the pointer. Reported at any width so
    // you can see them, but `enforced` tells you whether it counts as a defect.
    if (el.matches('a[href],button,input:not([type=hidden]),select,textarea,[role=button],[role=link],[onclick]')) {
      const w = Math.round(rect.width), h = Math.round(rect.height);
      if (w > 0 && h > 0 && (w < 44 || h < 44))
        out.touchTargets.push({ el: id, w, h, enforced: innerWidth < 768,
                                text: (el.textContent || '').trim().slice(0, 30) });
    }
  }

  // ---- occlusion: is anything sitting on top of text? ----
  // This is what catches a badge covering a button label — no style value
  // reveals it, only hit-testing does.
  for (const el of all) {
    if (!ownText(el)) continue;
    const r = el.getBoundingClientRect();
    if (r.width < 4 || r.height < 4) continue;
    let hits = 0, blocker = null, samples = 0;
    for (let fx = 0.15; fx <= 0.85; fx += 0.175) {
      for (let fy = 0.3; fy <= 0.7; fy += 0.2) {
        const x = r.left + r.width * fx, y = r.top + r.height * fy;
        if (x < 0 || y < 0 || x > innerWidth || y > innerHeight) continue;
        samples++;
        const top = document.elementFromPoint(x, y);
        if (!top) continue;
        if (top !== el && !el.contains(top) && !top.contains(el)) { hits++; blocker = top; }
      }
    }
    if (samples > 0 && hits / samples >= 0.25 && blocker)
      out.occluded.push({ el: sel(el), coveredBy: sel(blocker),
                          coverage: Math.round((hits / samples) * 100) + '%',
                          text: el.textContent.trim().slice(0, 40) });
  }

  // ---- images ----
  for (const img of document.querySelectorAll('img')) {
    const src = img.getAttribute('src');
    if (!img.complete || img.naturalWidth === 0) out.brokenImages.push(src);
    if (!img.hasAttribute('width') || !img.hasAttribute('height')) {
      const cs = getComputedStyle(img);
      if (!(cs.aspectRatio && cs.aspectRatio !== 'auto')) out.imgMissingDims.push(src);
    }
  }

  out.spacing.compliance = spaceTotal ? Math.round((spaceOk / spaceTotal) * 100) : null;
  out.spacing.offScale = [...new Set(out.spacing.offScale)];
  // The actionable unit is the distinct value, not the 27 places it appears.
  out.spacing.offScaleValues = [...new Set(
    out.spacing.offScale.map((s) => parseFloat(s.split('=')[1]))
  )].sort((a, b) => a - b);
  out.typeScale.sizes = [...sizes.entries()].sort((a, b) => a[0] - b[0])
    .map(([px, n]) => `${px}px x${n}`);
  out.horizontalScroll = document.documentElement.scrollWidth > innerWidth + 1;
  out.counts = {
    contrastFailures: out.contrast.length,
    contrastBelowTargetOnly: out.contrastBelowTarget.length,
    offScaleSpacingValues: out.spacing.offScaleValues.length,
    touchTargetFailures: out.touchTargets.filter((t) => t.enforced).length,
    lineLengthFailures: out.lineLength.length,
    clippedText: out.clipped.length,
    occludedText: out.occluded.length,
    brokenImages: out.brokenImages.length,
    placeholders: out.placeholders.length,
  };
  return out;
}
