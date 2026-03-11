/**
 * 行业研究页面 — 分页、推荐文章、Hero轮播、Three.js知识图谱
 */
(function () {
  'use strict';

  var ARTICLES_PER_PAGE = 6;
  var articles = [];
  var activeDomain = 'all';
  var searchQuery = '';
  var currentPage = 1;

  var grid = document.getElementById('articlesGrid');
  var emptyEl = document.getElementById('articlesEmpty');
  var paginationEl = document.getElementById('pagination');
  var featuredCard = document.getElementById('featuredCard');

  /* ============================================================
     Hero background image carousel — slow elegant crossfade
     ============================================================ */
  (function () {
    var slides = document.querySelectorAll('.hero-slide');
    if (!slides.length) return;
    var idx = 0;
    setInterval(function () {
      slides[idx].classList.remove('active');
      idx = (idx + 1) % slides.length;
      slides[idx].classList.add('active');
    }, 6000);
  })();

  /* ============================================================
     Load articles
     ============================================================ */
  async function loadArticles() {
    try {
      var resp = await fetch('research/index.json');
      articles = await resp.json();
      renderFeatured();
      renderPage();
    } catch (e) {
      console.error('Failed to load articles:', e);
    }
  }

  /* ============================================================
     Featured article — latest article, half-screen style
     ============================================================ */
  function renderFeatured() {
    var today = new Date().toISOString().slice(0, 10);
    var sorted = articles.filter(function (a) { return a.date <= today; }).sort(function (a, b) { return b.date.localeCompare(a.date); });
    var f = sorted[0];
    if (!f) return;
    var img = f.hero_image ? ('research/' + f.hero_image) : 'research/images/hero-data-01.jpg';
    featuredCard.innerHTML =
      '<div class="featured-image" style="background-image:url(\'' + img + '\')">'
      + '<span class="featured-badge">Latest</span>'
      + '</div>'
      + '<div class="featured-body">'
      + '<div class="featured-domain">' + escapeHtml(f.domain) + '</div>'
      + '<div class="featured-title">' + escapeHtml(f.title) + '</div>'
      + '<div class="featured-subtitle">' + escapeHtml(f.subtitle) + '</div>'
      + '<div class="featured-meta">'
      + '<span>' + f.date + '</span>'
      + '<span>' + f.keywords.slice(0, 3).join(' · ') + '</span>'
      + '<div class="featured-arrow"><svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div>'
      + '</div>'
      + '</div>';
    featuredCard.setAttribute('data-filename', f.filename);
    featuredCard.addEventListener('click', function () {
      window.location.href = 'research/' + f.filename;
    });
  }

  /* ============================================================
     Filtering & pagination
     ============================================================ */
  function getFiltered() {
    var today = new Date().toISOString().slice(0, 10);
    return articles.filter(function (a) {
      // 按系统时间过滤：只显示发布日期 <= 当天的文章
      if (a.date > today) return false;
      if (activeDomain !== 'all' && a.domain !== activeDomain) return false;
      if (searchQuery) {
        var q = searchQuery.toLowerCase();
        var h = (a.title + a.subtitle + a.keywords.join(' ') + a.domain).toLowerCase();
        if (h.indexOf(q) === -1) return false;
      }
      return true;
    });
  }

  function renderPage() {
    var filtered = getFiltered();
    filtered.sort(function (a, b) { return b.date.localeCompare(a.date); });

    if (filtered.length === 0) {
      grid.innerHTML = '';
      emptyEl.style.display = 'block';
      paginationEl.innerHTML = '';
      return;
    }
    emptyEl.style.display = 'none';

    var totalPages = Math.ceil(filtered.length / ARTICLES_PER_PAGE);
    if (currentPage > totalPages) currentPage = totalPages;
    var start = (currentPage - 1) * ARTICLES_PER_PAGE;
    var pageItems = filtered.slice(start, start + ARTICLES_PER_PAGE);

    grid.innerHTML = pageItems.map(function (a) {
      var img = a.hero_image ? ('research/' + a.hero_image) : '';
      return '<div class="article-card" data-filename="' + a.filename + '">'
        + (img ? '<div class="article-card-image" style="background-image:url(\'' + img + '\')"></div>' : '')
        + '<div class="article-card-body">'
        + '<div class="article-card-header">'
        + '<span class="article-domain">' + escapeHtml(a.domain) + '</span>'
        + '<span class="article-date">' + a.date + '</span>'
        + '</div>'
        + '<div class="article-title">' + escapeHtml(a.title) + '</div>'
        + '<div class="article-subtitle">' + escapeHtml(a.subtitle) + '</div>'
        + '<div class="article-keywords">'
        + a.keywords.slice(0, 3).map(function (k) { return '<span class="article-keyword">' + escapeHtml(k) + '</span>'; }).join('')
        + '</div>'
        + '</div>'
        + '</div>';
    }).join('');

    renderPagination(totalPages);
  }

  function renderPagination(totalPages) {
    if (totalPages <= 1) { paginationEl.innerHTML = ''; return; }

    var html = '';
    html += '<button class="page-btn" data-page="prev" ' + (currentPage === 1 ? 'disabled' : '') + '>&lsaquo;</button>';

    var pages = buildPageNumbers(currentPage, totalPages);
    pages.forEach(function (p) {
      if (p === '...') {
        html += '<span class="page-ellipsis">…</span>';
      } else {
        html += '<button class="page-btn' + (p === currentPage ? ' active' : '') + '" data-page="' + p + '">' + p + '</button>';
      }
    });

    html += '<button class="page-btn" data-page="next" ' + (currentPage === totalPages ? 'disabled' : '') + '>&rsaquo;</button>';
    paginationEl.innerHTML = html;
  }

  function buildPageNumbers(cur, total) {
    if (total <= 7) {
      var arr = [];
      for (var i = 1; i <= total; i++) arr.push(i);
      return arr;
    }
    var pages = [1];
    if (cur > 3) pages.push('...');
    for (var i = Math.max(2, cur - 1); i <= Math.min(total - 1, cur + 1); i++) pages.push(i);
    if (cur < total - 2) pages.push('...');
    pages.push(total);
    return pages;
  }

  /* ============================================================
     Event Listeners
     ============================================================ */
  grid.addEventListener('click', function (e) {
    var card = e.target.closest('.article-card');
    if (!card) return;
    window.location.href = 'research/' + card.getAttribute('data-filename');
  });

  paginationEl.addEventListener('click', function (e) {
    var btn = e.target.closest('.page-btn');
    if (!btn || btn.disabled) return;
    var p = btn.getAttribute('data-page');
    if (p === 'prev') currentPage--;
    else if (p === 'next') currentPage++;
    else currentPage = parseInt(p, 10);
    renderPage();
    document.getElementById('filtersBar').scrollIntoView({ behavior: 'smooth' });
  });

  document.getElementById('domainFilters').addEventListener('click', function (e) {
    if (!e.target.classList.contains('filter-tab')) return;
    this.querySelectorAll('.filter-tab').forEach(function (b) { b.classList.remove('active'); });
    e.target.classList.add('active');
    activeDomain = e.target.getAttribute('data-domain');
    currentPage = 1;
    renderPage();
  });

  document.getElementById('searchInput').addEventListener('input', function () {
    searchQuery = this.value.trim();
    currentPage = 1;
    renderPage();
  });

  function escapeHtml(s) {
    var d = document.createElement('div');
    d.textContent = s;
    return d.innerHTML;
  }

  /* ============================================================
     Header scroll & mobile menu
     ============================================================ */
  var header = document.getElementById('header');
  window.addEventListener('scroll', function () {
    header.classList.toggle('scrolled', window.scrollY > 20);
  });

  var mobileBtn = document.getElementById('mobileMenuBtn');
  var nav = document.getElementById('nav');
  if (mobileBtn) {
    mobileBtn.addEventListener('click', function () {
      nav.classList.toggle('active');
      mobileBtn.classList.toggle('active');
    });
  }

  /* ============================================================
     Three.js Knowledge Graph
     ============================================================ */
  function initViz() {
    var container = document.getElementById('vizContainer');
    if (!container || typeof THREE === 'undefined') return;

    var width = container.clientWidth;
    var height = container.clientHeight;

    var scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0A1628);

    var camera = new THREE.PerspectiveCamera(60, width / height, 0.1, 1000);
    camera.position.z = 28;

    var renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    // Keyword extraction
    var keywordMap = {};
    var domainColors = {
      '数据要素': 0x165DFF,
      '隐私计算': 0x3491FA,
      '数据安全': 0x86909C,
      '人工智能': 0xA0B0C8
    };

    var keywords = [];
    articles.forEach(function (a) {
      a.keywords.forEach(function (kw) {
        if (!keywordMap[kw]) {
          keywordMap[kw] = { count: 0, domain: a.domain };
          keywords.push(kw);
        }
        keywordMap[kw].count++;
      });
    });

    var nodes = [];
    var nodeGroup = new THREE.Group();
    scene.add(nodeGroup);

    // Domain centers
    var domainCenters = {};
    var domainNames = Object.keys(domainColors);
    domainNames.forEach(function (d, i) {
      var angle = (i / domainNames.length) * Math.PI * 2;
      var radius = 10;
      domainCenters[d] = { x: Math.cos(angle) * radius, y: Math.sin(angle) * radius, z: 0 };

      var geo = new THREE.SphereGeometry(1.2, 24, 24);
      var mat = new THREE.MeshPhongMaterial({
        color: domainColors[d], emissive: domainColors[d],
        emissiveIntensity: 0.3, transparent: true, opacity: 0.9
      });
      var mesh = new THREE.Mesh(geo, mat);
      mesh.position.set(domainCenters[d].x, domainCenters[d].y, 0);
      nodeGroup.add(mesh);
      nodes.push({ mesh: mesh, isDomain: true });
    });

    // Keyword nodes
    keywords.forEach(function (kw, i) {
      var info = keywordMap[kw];
      var center = domainCenters[info.domain] || { x: 0, y: 0, z: 0 };
      var angle = (i / keywords.length) * Math.PI * 2 + Math.random() * 0.5;
      var dist = 3 + Math.random() * 4;
      var z = (Math.random() - 0.5) * 6;
      var size = 0.2 + info.count * 0.15;
      var geo = new THREE.SphereGeometry(size, 16, 16);
      var color = domainColors[info.domain] || 0x165DFF;
      var mat = new THREE.MeshPhongMaterial({
        color: color, emissive: color, emissiveIntensity: 0.15,
        transparent: true, opacity: 0.7
      });
      var mesh = new THREE.Mesh(geo, mat);
      mesh.position.set(center.x + Math.cos(angle) * dist, center.y + Math.sin(angle) * dist, z);
      nodeGroup.add(mesh);
      nodes.push({ mesh: mesh, kw: kw, z: z });
    });

    // Lines
    var lineMat = new THREE.LineBasicMaterial({ color: 0x165DFF, transparent: true, opacity: 0.08 });
    articles.forEach(function (a) {
      for (var i = 0; i < a.keywords.length; i++) {
        for (var j = i + 1; j < a.keywords.length; j++) {
          var n1 = nodes.find(function (n) { return n.kw === a.keywords[i]; });
          var n2 = nodes.find(function (n) { return n.kw === a.keywords[j]; });
          if (n1 && n2) {
            var geo = new THREE.BufferGeometry().setFromPoints([n1.mesh.position, n2.mesh.position]);
            scene.add(new THREE.Line(geo, lineMat));
          }
        }
      }
    });

    // Particles
    var pGeo = new THREE.BufferGeometry();
    var pCount = 300;
    var pos = new Float32Array(pCount * 3);
    for (var i = 0; i < pCount; i++) {
      pos[i * 3] = (Math.random() - 0.5) * 50;
      pos[i * 3 + 1] = (Math.random() - 0.5) * 50;
      pos[i * 3 + 2] = (Math.random() - 0.5) * 30;
    }
    pGeo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    scene.add(new THREE.Points(pGeo, new THREE.PointsMaterial({ color: 0x165DFF, size: 0.08, transparent: true, opacity: 0.4 })));

    // Lights
    scene.add(new THREE.AmbientLight(0xffffff, 0.5));
    var dLight = new THREE.DirectionalLight(0xffffff, 0.8);
    dLight.position.set(10, 10, 10);
    scene.add(dLight);
    var pLight = new THREE.PointLight(0x165DFF, 1, 40);
    pLight.position.set(0, 0, 15);
    scene.add(pLight);

    // Mouse
    var mouse = { x: 0, y: 0 };
    container.addEventListener('mousemove', function (e) {
      var r = container.getBoundingClientRect();
      mouse.x = ((e.clientX - r.left) / r.width) * 2 - 1;
      mouse.y = -((e.clientY - r.top) / r.height) * 2 + 1;
    });

    // Animate
    var clock = new THREE.Clock();
    (function animate() {
      requestAnimationFrame(animate);
      var t = clock.getElapsedTime();
      nodeGroup.rotation.y = t * 0.05;
      nodeGroup.rotation.x = Math.sin(t * 0.03) * 0.1;
      camera.position.x += (mouse.x * 3 - camera.position.x) * 0.02;
      camera.position.y += (mouse.y * 2 - camera.position.y) * 0.02;
      camera.lookAt(scene.position);
      nodes.forEach(function (n, i) {
        if (!n.isDomain && n.mesh) n.mesh.position.z = n.z + Math.sin(t * 0.5 + i * 0.3) * 0.3;
      });
      renderer.render(scene, camera);
    })();

    window.addEventListener('resize', function () {
      var w = container.clientWidth, h = container.clientHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    });
  }

  /* ============================================================
     Init
     ============================================================ */
  loadArticles().then(function () {
    initViz();
  });

})();
