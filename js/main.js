// 严格模式
'use strict';

document.addEventListener('DOMContentLoaded', function () {

    // ===== Header 滚动效果 =====
    var header = document.getElementById('header');
    var backToTop = document.getElementById('backToTop');

    function onScroll() {
        var scrollY = window.scrollY || window.pageYOffset;
        if (scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
        if (scrollY > 400) {
            backToTop.classList.add('visible');
        } else {
            backToTop.classList.remove('visible');
        }
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    // ===== 回到顶部 =====
    backToTop.addEventListener('click', function () {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // ===== 移动端菜单 =====
    var mobileMenuBtn = document.getElementById('mobileMenuBtn');
    var nav = document.getElementById('nav');

    mobileMenuBtn.addEventListener('click', function () {
        nav.classList.toggle('active');
        var spans = mobileMenuBtn.querySelectorAll('span');
        if (nav.classList.contains('active')) {
            spans[0].style.transform = 'rotate(45deg) translateY(7px)';
            spans[1].style.opacity = '0';
            spans[2].style.transform = 'rotate(-45deg) translateY(-7px)';
        } else {
            spans[0].style.transform = '';
            spans[1].style.opacity = '';
            spans[2].style.transform = '';
        }
    });

    // 点击导航链接关闭菜单
    var navLinks = nav.querySelectorAll('.nav-link');
    navLinks.forEach(function (link) {
        link.addEventListener('click', function () {
            nav.classList.remove('active');
            var spans = mobileMenuBtn.querySelectorAll('span');
            spans[0].style.transform = '';
            spans[1].style.opacity = '';
            spans[2].style.transform = '';
        });
    });

    // ===== 平滑滚动 =====
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            var target = document.querySelector(this.getAttribute('href'));
            if (target) {
                var headerHeight = header.offsetHeight;
                var targetPosition = target.getBoundingClientRect().top + window.pageYOffset - headerHeight;
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // ===== 视频交互 =====
    var video = document.getElementById('promoVideo');
    var videoOverlay = document.getElementById('videoOverlay');
    var videoPlayBtn = document.getElementById('videoPlayBtn');

    if (video && videoOverlay) {
        videoPlayBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            if (video.muted) {
                video.muted = false;
                videoOverlay.style.opacity = '0';
                videoOverlay.style.pointerEvents = 'none';
            } else {
                video.muted = true;
                videoOverlay.style.opacity = '';
                videoOverlay.style.pointerEvents = '';
            }
        });
    }

    // ===== 滚动动画 (Intersection Observer) =====
    var observerOptions = {
        root: null,
        rootMargin: '0px 0px -60px 0px',
        threshold: 0.1
    };

    var animatedElements = document.querySelectorAll(
        '.product-card, .component-card, .advantage-card, .scenario-card, .section-header, .architecture-diagram, .about-content, .video-wrapper'
    );

    // 初始设置
    animatedElements.forEach(function (el) {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s cubic-bezier(0.4, 0, 0.2, 1), transform 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
    });

    var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry, index) {
            if (entry.isIntersecting) {
                // 为同级元素添加延迟
                var siblings = entry.target.parentElement.querySelectorAll(
                    '.product-card, .component-card, .advantage-card, .scenario-card'
                );
                var delay = 0;
                siblings.forEach(function (sib, i) {
                    if (sib === entry.target) {
                        delay = i * 80;
                    }
                });

                setTimeout(function () {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, delay);

                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    animatedElements.forEach(function (el) {
        observer.observe(el);
    });

    // ===== 导航高亮 =====
    var sections = document.querySelectorAll('section[id]');
    var navHighlightLinks = document.querySelectorAll('.nav-link');

    function highlightNav() {
        var scrollY = window.scrollY + header.offsetHeight + 100;
        sections.forEach(function (section) {
            var sectionTop = section.offsetTop;
            var sectionHeight = section.offsetHeight;
            var sectionId = section.getAttribute('id');

            if (scrollY >= sectionTop && scrollY < sectionTop + sectionHeight) {
                navHighlightLinks.forEach(function (link) {
                    link.style.color = '';
                    link.style.background = '';
                    if (link.getAttribute('href') === '#' + sectionId) {
                        link.style.color = 'var(--primary)';
                        link.style.background = 'var(--primary-bg)';
                    }
                });
            }
        });
    }

    window.addEventListener('scroll', highlightNav, { passive: true });
});
