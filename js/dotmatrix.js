/**
 * 点阵 + 水波纹背景动画
 * 所有页面通用，自动附着到 body
 */
(function () {
  'use strict';

  var canvas = document.createElement('canvas');
  canvas.id = 'dotMatrixCanvas';
  canvas.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;opacity:0.35;';
  document.body.insertBefore(canvas, document.body.firstChild);

  var ctx = canvas.getContext('2d');
  var W, H, dots = [], ripples = [], spacing = 28, cols, rows;
  var frame = 0;

  function resize() {
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = window.innerWidth;
    H = window.innerHeight;
    canvas.width = W * dpr;
    canvas.height = H * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    cols = Math.ceil(W / spacing) + 1;
    rows = Math.ceil(H / spacing) + 1;
    buildDots();
  }

  function buildDots() {
    dots = [];
    for (var r = 0; r < rows; r++) {
      for (var c = 0; c < cols; c++) {
        dots.push({ x: c * spacing, y: r * spacing, baseR: 1.0 });
      }
    }
  }

  // Auto-spawn ripples periodically
  function spawnRipple(x, y) {
    ripples.push({ x: x, y: y, radius: 0, maxRadius: 260 + Math.random() * 180, speed: 0.6 + Math.random() * 0.4, opacity: 1 });
    if (ripples.length > 6) ripples.shift();
  }

  // Natural auto-ripples
  var autoTimer = 0;
  function maybeAutoRipple() {
    autoTimer++;
    if (autoTimer > 120 + Math.random() * 180) {
      autoTimer = 0;
      spawnRipple(Math.random() * W, Math.random() * H);
    }
  }

  // Mouse interaction
  var mouseX = -999, mouseY = -999, mouseTimer = 0;
  document.addEventListener('mousemove', function (e) {
    mouseX = e.clientX;
    mouseY = e.clientY;
    mouseTimer++;
    if (mouseTimer > 60) {
      mouseTimer = 0;
      spawnRipple(mouseX, mouseY);
    }
  });

  function draw() {
    frame++;
    ctx.clearRect(0, 0, W, H);
    maybeAutoRipple();

    // Update ripples
    for (var ri = ripples.length - 1; ri >= 0; ri--) {
      var rp = ripples[ri];
      rp.radius += rp.speed;
      rp.opacity = 1 - (rp.radius / rp.maxRadius);
      if (rp.opacity <= 0) { ripples.splice(ri, 1); }
    }

    // Draw dots
    var time = frame * 0.008;
    for (var i = 0; i < dots.length; i++) {
      var d = dots[i];
      var dx = d.x, dy = d.y;

      // Base gentle breathing
      var breath = 0.15 * Math.sin(time + dx * 0.01 + dy * 0.012);

      // Ripple influence
      var rippleBoost = 0;
      for (var ri = 0; ri < ripples.length; ri++) {
        var rp = ripples[ri];
        var dist = Math.sqrt((dx - rp.x) * (dx - rp.x) + (dy - rp.y) * (dy - rp.y));
        var ringDist = Math.abs(dist - rp.radius);
        if (ringDist < 40) {
          var wave = (1 - ringDist / 40) * rp.opacity;
          rippleBoost += wave * 1.2;
        }
      }

      // Mouse proximity glow
      var mdist = Math.sqrt((dx - mouseX) * (dx - mouseX) + (dy - mouseY) * (dy - mouseY));
      var mouseGlow = mdist < 100 ? (1 - mdist / 100) * 0.5 : 0;

      var r = d.baseR + breath + rippleBoost * 0.8 + mouseGlow;
      var alpha = 0.18 + rippleBoost * 0.5 + mouseGlow * 0.4;

      if (r < 0.3) r = 0.3;
      if (alpha < 0.06) alpha = 0.06;
      if (alpha > 0.7) alpha = 0.7;

      ctx.beginPath();
      ctx.arc(dx, dy, r, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(22, 93, 255, ' + alpha + ')';
      ctx.fill();
    }

    requestAnimationFrame(draw);
  }

  window.addEventListener('resize', resize);
  resize();

  // Seed initial ripples
  setTimeout(function () { spawnRipple(W * 0.3, H * 0.4); }, 500);
  setTimeout(function () { spawnRipple(W * 0.7, H * 0.6); }, 1500);

  draw();
})();
