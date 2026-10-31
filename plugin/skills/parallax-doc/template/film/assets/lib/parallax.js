// parallax-doc scene library. Every block loads it with
//   <script src="assets/lib/parallax.js"></script>
// before its own script. Plain functions on window; nothing here touches the clock.

const FPS = 30;
const L = Math.log;

// Type text on letter by letter. The element's data-text holds the line; "|" toggles the
// red emphasis on and off ("That is not in |question|" -> "question" in red).
// start: seconds on this scene's clock; step: frames per letter (2-3 reads as typed).
function typeOn(tl, el, start, step) {
  const parts = el.dataset.text.split("|");
  el.innerHTML = "";
  let i = 0;
  parts.forEach((part, k) => {
    [...part].forEach((ch) => {
      if (ch === "\n") {
        el.appendChild(document.createElement("br"));
        return;
      }
      const s = document.createElement("span");
      s.textContent = ch;
      if (k % 2 === 1) s.className = "red";
      el.appendChild(s);
      tl.fromTo(s, { opacity: 0 }, { opacity: 1, duration: 0.04, ease: "none" }, start + (i++ * step) / FPS);
    });
  });
}

// A camera on a plate: (cx, cy) is the plate point at the frame centre, ls = ln(scale),
// so a zoom eases evenly. Tween the returned rig's keys (GSAP calls them as setters on
// every render and seek, so the move is frame-exact).
function cameraRig(el, init, extra) {
  const cam = { ...init };
  const apply = () => {
    const s = Math.exp(cam.ls);
    gsap.set(el, { scale: s, x: 960 - cam.cx * s, y: 540 - cam.cy * s, transformOrigin: "0 0" });
    if (extra) extra(cam);
  };
  const rig = {};
  Object.keys(cam).forEach((k) => {
    rig[k] = function (v) {
      if (v === undefined) return cam[k];
      cam[k] = v;
      apply();
    };
  });
  apply();
  return rig;
}

// Any seek-safe custom value: a rig with one key whose setter does the work.
function driver(initial, onSet) {
  const state = { v: initial };
  const rig = {
    v: function (v) {
      if (v === undefined) return state.v;
      state.v = v;
      onSet(v);
    },
  };
  onSet(initial);
  return rig;
}

// Frame a plate point at the frame centre at a given scale (for elements whose
// transform-origin is 0 0). Use in GSAP tweens: tl.to(el, { ...frame(1.2, 900, 500) }).
function frame(scale, cx, cy) {
  return { scale: scale, x: 960 - cx * scale, y: 540 - cy * scale };
}

// A vertical seam at screen x: keep only what is left (or right) of it, feathered.
// Used to split two worlds behind a passing column.
function seamMask(el, x, side, feather) {
  const f = feather || 0;
  const m =
    side === "left"
      ? `linear-gradient(to right, #000 ${x - f}px, transparent ${x + f}px)`
      : `linear-gradient(to right, transparent ${x - f}px, #000 ${x + f}px)`;
  el.style.maskImage = m;
  el.style.webkitMaskImage = m;
}

// Hard clip: only the part right of screen x shows (object wipes).
function clipRightOf(el, x) {
  el.style.clipPath = `polygon(${x}px -200px, 2200px -200px, 2200px 1300px, ${x}px 1300px)`;
}

// Directional motion blur through an SVG filter the block declares:
//   <filter id="X"><feGaussianBlur id="X-g" stdDeviation="0 0"/></filter>
function motionBlur(el, filterId, sx, sy) {
  const g = document.getElementById(filterId + "-g");
  g.setAttribute("stdDeviation", `${sx} ${sy}`);
  el.style.filter = sx > 0.3 || sy > 0.3 ? `url(#${filterId})` : "none";
}
