/**
 * 行业研究页面 - 列表、筛选、文章加载与Three.js可视化
 */
(function () {
  'use strict';

  /* ============================================================
     State
     ============================================================ */
  let articles = [];
  let activeDomain = 'all';
  let activeYear = 'all';
  let searchQuery = '';
  let isListView = false;

  const grid = document.getElementById('articlesGrid');
  const emptyEl = document.getElementById('articlesEmpty');
  const resultCount = document.getElementById('resultCount');

  /* ============================================================
     Load article index
     ============================================================ */
  async function loadArticles() {
    try {
      const resp = await fetch('research/index.json');
      articles = await resp.json();
      renderArticles();
    } catch (e) {
      console.error('Failed to load articles:', e);
      resultCount.textContent = '加载失败';
    }
  }

  /* ============================================================
     Render article cards
     ============================================================ */
  function getFiltered() {
    return articles.filter(function (a) {
      if (activeDomain !== 'all' && a.domain !== activeDomain) return false;
      if (activeYear !== 'all' && !a.date.startsWith(activeYear)) return false;
      if (searchQuery) {
        var q = searchQuery.toLowerCase();
        var haystack = (a.title + a.subtitle + a.keywords.join(' ') + a.domain).toLowerCase();
        if (haystack.indexOf(q) === -1) return false;
      }
      return true;
    });
  }

  function renderArticles() {
    var filtered = getFiltered();
    resultCount.textContent = '共 ' + filtered.length + ' 篇报告';

    if (filtered.length === 0) {
      grid.innerHTML = '';
      emptyEl.style.display = 'block';
      return;
    }
    emptyEl.style.display = 'none';

    // Sort by date desc
    filtered.sort(function (a, b) { return b.date.localeCompare(a.date); });

    grid.innerHTML = filtered.map(function (a) {
      return '<div class="article-card" data-slug="' + a.slug + '" data-filename="' + a.filename + '">'
        + '<div class="article-card-header">'
        + '<span class="article-domain" data-domain="' + a.domain + '">' + a.domain + '</span>'
        + '<span class="article-date">' + a.date + '</span>'
        + '</div>'
        + '<div class="article-title">' + escapeHtml(a.title) + '</div>'
        + '<div class="article-subtitle">' + escapeHtml(a.subtitle) + '</div>'
        + '<div class="article-keywords">'
        + a.keywords.map(function (k) { return '<span class="article-keyword">' + escapeHtml(k) + '</span>'; }).join('')
        + '</div>'
        + '</div>';
    }).join('');
  }

  function escapeHtml(s) {
    var d = document.createElement('div');
    d.textContent = s;
    return d.innerHTML;
  }

  /* ============================================================
     Filters
     ============================================================ */
  document.getElementById('domainFilters').addEventListener('click', function (e) {
    if (!e.target.classList.contains('filter-tag')) return;
    this.querySelectorAll('.filter-tag').forEach(function (b) { b.classList.remove('active'); });
    e.target.classList.add('active');
    activeDomain = e.target.getAttribute('data-domain');
    renderArticles();
  });

  document.getElementById('yearFilters').addEventListener('click', function (e) {
    if (!e.target.classList.contains('filter-tag')) return;
    this.querySelectorAll('.filter-tag').forEach(function (b) { b.classList.remove('active'); });
    e.target.classList.add('active');
    activeYear = e.target.getAttribute('data-year');
    renderArticles();
  });

  document.getElementById('searchInput').addEventListener('input', function () {
    searchQuery = this.value.trim();
    renderArticles();
  });

  /* View toggle */
  document.getElementById('gridViewBtn').addEventListener('click', function () {
    isListView = false;
    grid.classList.remove('list-view');
    this.classList.add('active');
    document.getElementById('listViewBtn').classList.remove('active');
  });

  document.getElementById('listViewBtn').addEventListener('click', function () {
    isListView = true;
    grid.classList.add('list-view');
    this.classList.add('active');
    document.getElementById('gridViewBtn').classList.remove('active');
  });

  /* ============================================================
     Article Modal
     ============================================================ */
  var modal = document.getElementById('articleModal');
  var modalBody = document.getElementById('modalBody');

  grid.addEventListener('click', function (e) {
    var card = e.target.closest('.article-card');
    if (!card) return;
    openArticle(card.getAttribute('data-filename'));
  });

  document.getElementById('modalClose').addEventListener('click', closeModal);
  document.getElementById('modalOverlay').addEventListener('click', closeModal);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeModal();
  });

  async function openArticle(filename) {
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
    modalBody.innerHTML = '<p style="text-align:center;padding:40px;color:#86909C;">加载中...</p>';

    try {
      var resp = await fetch('research/' + filename);
      var text = await resp.text();

      // Strip YAML frontmatter
      var content = text;
      if (content.startsWith('---')) {
        var endIdx = content.indexOf('---', 3);
        if (endIdx > 0) {
          content = content.substring(endIdx + 3).trim();
        }
      }

      // Render markdown
      if (typeof marked !== 'undefined') {
        modalBody.innerHTML = marked.parse(content);
      } else {
        modalBody.innerHTML = '<pre style="white-space:pre-wrap;">' + escapeHtml(content) + '</pre>';
      }
    } catch (e) {
      modalBody.innerHTML = '<p style="text-align:center;padding:40px;color:#F53F3F;">加载失败</p>';
    }
  }

  function closeModal() {
    modal.classList.remove('active');
    document.body.style.overflow = '';
    modalBody.innerHTML = '';
  }

  /* ============================================================
     Header scroll effect & mobile menu (same as main page)
     ============================================================ */
  var header = document.getElementById('header');
  window.addEventListener('scroll', function () {
    if (window.scrollY > 20) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
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
     Three.js Knowledge Graph Visualization
     ============================================================ */
  function initViz() {
    var container = document.getElementById('vizContainer');
    if (!container || typeof THREE === 'undefined') return;

    var width = container.clientWidth;
    var height = container.clientHeight;

    // Scene
    var scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0A1628);

    // Camera
    var camera = new THREE.PerspectiveCamera(60, width / height, 0.1, 1000);
    camera.position.z = 28;

    // Renderer
    var renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    // Build keyword graph from articles data
    var keywordMap = {};
    var domainColors = {
      '数据要素': 0x165DFF,
      '隐私计算': 0x0FC6C2,
      '数据安全': 0xF7BA1E,
      '人工智能': 0x722ED1
    };

    // Collect unique keywords and their domains
    var keywords = [];
    var keywordDomainMap = {};
    articles.forEach(function (a) {
      a.keywords.forEach(function (kw) {
        if (!keywordMap[kw]) {
          keywordMap[kw] = { count: 0, domain: a.domain };
          keywords.push(kw);
          keywordDomainMap[kw] = a.domain;
        }
        keywordMap[kw].count++;
      });
    });

    // Create nodes (spheres)
    var nodes = [];
    var nodeGroup = new THREE.Group();
    scene.add(nodeGroup);

    // Domain center nodes
    var domainCenters = {};
    var domainNames = Object.keys(domainColors);
    domainNames.forEach(function (d, i) {
      var angle = (i / domainNames.length) * Math.PI * 2;
      var radius = 10;
      domainCenters[d] = {
        x: Math.cos(angle) * radius,
        y: Math.sin(angle) * radius,
        z: 0
      };

      var geo = new THREE.SphereGeometry(1.2, 24, 24);
      var mat = new THREE.MeshPhongMaterial({
        color: domainColors[d],
        emissive: domainColors[d],
        emissiveIntensity: 0.3,
        transparent: true,
        opacity: 0.9
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
        color: color,
        emissive: color,
        emissiveIntensity: 0.15,
        transparent: true,
        opacity: 0.7
      });
      var mesh = new THREE.Mesh(geo, mat);
      mesh.position.set(
        center.x + Math.cos(angle) * dist,
        center.y + Math.sin(angle) * dist,
        z
      );
      nodeGroup.add(mesh);
      nodes.push({ mesh: mesh, kw: kw, center: center, angle: angle, dist: dist, z: z });
    });

    // Connecting lines between co-occurring keywords
    var lineMat = new THREE.LineBasicMaterial({
      color: 0x165DFF,
      transparent: true,
      opacity: 0.08
    });

    articles.forEach(function (a) {
      for (var i = 0; i < a.keywords.length; i++) {
        for (var j = i + 1; j < a.keywords.length; j++) {
          var n1 = nodes.find(function (n) { return n.kw === a.keywords[i]; });
          var n2 = nodes.find(function (n) { return n.kw === a.keywords[j]; });
          if (n1 && n2) {
            var geo = new THREE.BufferGeometry().setFromPoints([
              n1.mesh.position, n2.mesh.position
            ]);
            var line = new THREE.Line(geo, lineMat);
            scene.add(line);
          }
        }
      }
    });

    // Lines from domain centers to keywords
    var domainLineMat = new THREE.LineBasicMaterial({
      color: 0xffffff,
      transparent: true,
      opacity: 0.04
    });

    keywords.forEach(function (kw) {
      var domain = keywordDomainMap[kw];
      var domainNode = nodes.find(function (n) { return n.isDomain; });
      var kwNode = nodes.find(function (n) { return n.kw === kw; });
      if (kwNode) {
        var center = domainCenters[domain];
        var centerPos = new THREE.Vector3(center.x, center.y, 0);
        var geo = new THREE.BufferGeometry().setFromPoints([
          centerPos, kwNode.mesh.position
        ]);
        var line = new THREE.Line(geo, domainLineMat);
        scene.add(line);
      }
    });

    // Ambient particles
    var particlesGeo = new THREE.BufferGeometry();
    var particleCount = 300;
    var positions = new Float32Array(particleCount * 3);
    for (var i = 0; i < particleCount; i++) {
      positions[i * 3] = (Math.random() - 0.5) * 50;
      positions[i * 3 + 1] = (Math.random() - 0.5) * 50;
      positions[i * 3 + 2] = (Math.random() - 0.5) * 30;
    }
    particlesGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    var particleMat = new THREE.PointsMaterial({
      color: 0x165DFF,
      size: 0.08,
      transparent: true,
      opacity: 0.4
    });
    scene.add(new THREE.Points(particlesGeo, particleMat));

    // Lights
    scene.add(new THREE.AmbientLight(0xffffff, 0.5));
    var dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
    dirLight.position.set(10, 10, 10);
    scene.add(dirLight);
    var pointLight = new THREE.PointLight(0x165DFF, 1, 40);
    pointLight.position.set(0, 0, 15);
    scene.add(pointLight);

    // Mouse interaction
    var mouse = { x: 0, y: 0 };
    container.addEventListener('mousemove', function (e) {
      var rect = container.getBoundingClientRect();
      mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
    });

    // Animate
    var clock = new THREE.Clock();
    function animate() {
      requestAnimationFrame(animate);
      var elapsed = clock.getElapsedTime();

      // Slow rotation
      nodeGroup.rotation.y = elapsed * 0.05;
      nodeGroup.rotation.x = Math.sin(elapsed * 0.03) * 0.1;

      // Mouse influence on camera
      camera.position.x += (mouse.x * 3 - camera.position.x) * 0.02;
      camera.position.y += (mouse.y * 2 - camera.position.y) * 0.02;
      camera.lookAt(scene.position);

      // Pulse keyword nodes
      nodes.forEach(function (n, i) {
        if (!n.isDomain && n.mesh) {
          n.mesh.position.z = n.z + Math.sin(elapsed * 0.5 + i * 0.3) * 0.3;
        }
      });

      renderer.render(scene, camera);
    }
    animate();

    // Resize handler
    window.addEventListener('resize', function () {
      var w = container.clientWidth;
      var h = container.clientHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    });
  }

  /* ============================================================
     Init
     ============================================================ */
  loadArticles().then(function () {
    // Init Three.js after articles are loaded (needs keyword data)
    initViz();
  });

})();
