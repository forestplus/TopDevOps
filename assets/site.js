// ========== PARTICLES ==========
        const canvas = document.getElementById('particles-canvas');
        const ctx = canvas.getContext('2d');
        let particles = [];
        let mouseX = 0, mouseY = 0;

        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);

        class Particle {
            constructor() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.size = Math.random() * 2 + 0.5;
                this.speedX = (Math.random() - 0.5) * 0.5;
                this.speedY = (Math.random() - 0.5) * 0.5;
                this.opacity = Math.random() * 0.5 + 0.2;
            }
            update() {
                this.x += this.speedX;
                this.y += this.speedY;
                if (this.x < 0 || this.x > canvas.width) this.speedX *= -1;
                if (this.y < 0 || this.y > canvas.height) this.speedY *= -1;
                const dx = mouseX - this.x;
                const dy = mouseY - this.y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < 100) {
                    this.x -= dx * 0.01;
                    this.y -= dy * 0.01;
                }
            }
            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(0, 212, 255, ${this.opacity})`;
                ctx.fill();
            }
        }

        for (let i = 0; i < 60; i++) particles.push(new Particle());

        function drawConnections() {
            for (let i = 0; i < particles.length; i++) {
                for (let j = i + 1; j < particles.length; j++) {
                    const dx = particles[i].x - particles[j].x;
                    const dy = particles[i].y - particles[j].y;
                    const dist = Math.sqrt(dx * dx + dy * dy);
                    if (dist < 120) {
                        ctx.beginPath();
                        ctx.strokeStyle = `rgba(0, 212, 255, ${0.15 * (1 - dist / 120)})`;
                        ctx.lineWidth = 0.5;
                        ctx.moveTo(particles[i].x, particles[i].y);
                        ctx.lineTo(particles[j].x, particles[j].y);
                        ctx.stroke();
                    }
                }
            }
        }

        const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        let particlesRunning = false;
        let particlesRaf = null;

        function drawFrame() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            particles.forEach(p => { p.update(); p.draw(); });
            drawConnections();
        }

        function loopParticles() {
            drawFrame();
            particlesRaf = requestAnimationFrame(loopParticles);
        }

        function startParticles() {
            if (particlesRunning || reduceMotion || document.hidden) return;
            particlesRunning = true;
            loopParticles();
        }

        function stopParticles() {
            particlesRunning = false;
            if (particlesRaf) cancelAnimationFrame(particlesRaf);
            particlesRaf = null;
        }

        document.addEventListener('visibilitychange', () => {
            if (document.hidden) stopParticles();
            else startParticles();
        });

        if (reduceMotion) drawFrame();
        else startParticles();

        window.addEventListener('mousemove', e => { mouseX = e.clientX; mouseY = e.clientY; });

        // ========== NOTES SEARCH ==========
        (function initNotesSearch() {
            var input = document.getElementById('notes-search');
            var clearBtn = document.getElementById('notes-search-clear');
            var emptyEl = document.getElementById('notes-empty');
            var section = document.getElementById('notes');
            if (!input || !section) return;

            function applyLangPlaceholder() {
                var lang = (document.documentElement.lang || 'ru').slice(0,2);
                if (lang !== 'en') lang = 'ru';
                var ph = input.getAttribute('data-placeholder-' + lang) || 'Search…';
                input.setAttribute('placeholder', ph);
            }
            applyLangPlaceholder();
            document.addEventListener('langchange', applyLangPlaceholder);

            function filter() {
                var q = (input.value || '').trim().toLowerCase();
                clearBtn.classList.toggle('visible', q.length > 0);
                var groups = section.querySelectorAll('.notes-group');
                var anyVisible = false;
                groups.forEach(function(group) {
                    var links = group.querySelectorAll('.notes-list a');
                    var groupVisible = false;
                    links.forEach(function(a) {
                        var li = a.closest('li');
                        var text = ((a.textContent || '') + ' ' + (a.getAttribute('data-ru')||'') + ' ' + (a.getAttribute('data-en')||'')).toLowerCase();
                        var titleEl = group.querySelector('.notes-toggle-label') || group.querySelector('.notes-group-title');
                        var title = (titleEl && titleEl.textContent) || '';
                        text += ' ' + title.toLowerCase();
                        var match = !q || text.indexOf(q) !== -1;
                        if (li) li.classList.toggle('hidden-by-search', !match);
                        if (match) groupVisible = true;
                    });
                    group.classList.toggle('hidden-by-search', !groupVisible);
                    if (groupVisible) {
                        anyVisible = true;
                        if (q && !group.classList.contains('open')) {
                            var btn = group.querySelector('.notes-toggle');
                            if (btn && btn.getAttribute('aria-expanded') === 'false') btn.click();
                        }
                    }
                });
                if (emptyEl) emptyEl.classList.toggle('visible', q && !anyVisible);
            }

            input.addEventListener('input', filter);
            input.addEventListener('search', filter);
            if (clearBtn) clearBtn.addEventListener('click', function() {
                input.value = '';
                filter();
                input.focus();
            });
        })();
