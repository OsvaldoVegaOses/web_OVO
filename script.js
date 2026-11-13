// Configuración del Header al hacer scroll
const header = document.getElementById('header');
const navToggle = document.getElementById('nav-toggle');
const navLinks = document.getElementById('nav-links');
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

// El enlace original conserva su comportamiento y su medición; el aviso no
// dispara eventos ni incluye los atributos utilizados por los rastreadores.
document.querySelectorAll('a[href]').forEach(link => {
    if (!/^mailto:contacto@osvaldovega\.cl(?:\?|$)/i.test(link.getAttribute('href'))) return;
    const notice = document.createElement('span');
    notice.className = 'contact-notice';
    notice.setAttribute('role', 'status');
    notice.setAttribute('aria-live', 'polite');
    if (navLinks && navLinks.contains(link) && header) {
        notice.classList.add('contact-notice-header');
        header.appendChild(notice);
    } else {
        link.insertAdjacentElement('afterend', notice);
    }
    link.addEventListener('click', event => {
        if (event.defaultPrevented || event.button !== 0) return;
        notice.replaceChildren(document.createTextNode('Se abrirá tu aplicación de correo. También puedes escribir a '));
        const email = document.createElement('a');
        email.href = 'mailto:contacto@osvaldovega.cl';
        email.textContent = 'contacto@osvaldovega.cl';
        notice.append(email, document.createTextNode('.'));
    });
});

window.addEventListener('scroll', () => {
    if (window.scrollY > 40) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});

// Menú móvil (Hamburger Toggle)
if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => {
        const isExpanded = navToggle.getAttribute('aria-expanded') === 'true';
        navToggle.setAttribute('aria-expanded', !isExpanded);
        navLinks.classList.toggle('active');
        
        // Cambiar icono
        const icon = navToggle.querySelector('i');
        if (icon) {
            if (navLinks.classList.contains('active')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-xmark');
            } else {
                icon.classList.remove('fa-xmark');
                icon.classList.add('fa-bars');
            }
        }
    });

    // Cerrar menú al hacer clic en un enlace
    navLinks.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            if (navLinks.classList.contains('active')) {
                navLinks.classList.remove('active');
                navToggle.setAttribute('aria-expanded', 'false');
                const icon = navToggle.querySelector('i');
                if (icon) {
                    icon.classList.remove('fa-xmark');
                    icon.classList.add('fa-bars');
                }
            }
        });
    });
}

// Navegación suave con offset para header fijo
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;

        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            e.preventDefault();
            const headerHeight = header ? header.offsetHeight : 0;
            const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - headerHeight - 16;
            
            window.scrollTo({
                top: targetPosition,
                behavior: prefersReducedMotion ? 'auto' : 'smooth'
            });
        }
    });
});

// Animaciones de revelado progresivo (IntersectionObserver)
const animatableElements = document.querySelectorAll(
    '.glass-card, .project-card, .method-step, .theogen-box, .value-prop-card'
);

const observerOptions = {
    threshold: 0.12,
    rootMargin: "0px 0px -40px 0px"
};

const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
            revealObserver.unobserve(entry.target);
        }
    });
}, observerOptions);

if (!prefersReducedMotion) {
    animatableElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(22px)';
        el.style.transition = 'opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1), transform 0.6s cubic-bezier(0.16, 1, 0.3, 1)';
        revealObserver.observe(el);
    });
}

// Control de acordeones en casos de estudio (.case-accordion)
document.addEventListener('DOMContentLoaded', () => {
    const btnExpandAll = document.getElementById('btn-expand-all');
    const btnCollapseAll = document.getElementById('btn-collapse-all');
    
    if (btnExpandAll || btnCollapseAll) {
        const getAccordions = () => document.querySelectorAll('.case-accordion');
        
        if (btnExpandAll) {
            btnExpandAll.addEventListener('click', () => {
                getAccordions().forEach(accordion => {
                    accordion.open = true;
                });
            });
        }
        
        if (btnCollapseAll) {
            btnCollapseAll.addEventListener('click', () => {
                getAccordions().forEach(accordion => {
                    accordion.open = false;
                });
            });
        }
    }
});
