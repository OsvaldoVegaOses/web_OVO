import re

css_content = """    <style>
        /* ============================================================
           INDEX_2.HTML — EDITORIAL LIGHT PORTFOLIO & TECH TRANSITION
           ============================================================ */

        /* --- Global Reset Scope & Color Tokens --- */
        .index-editorial-prototype {
            --bg-main: #F4F6F8;
            --bg-surface: #FFFFFF;
            --bg-alt: #EEF2F6;
            --text-primary: #07111F;
            --text-secondary: #334155;
            --text-muted: #64748B;
            --accent-cyan: #0e7490;
            --accent-hover: #0369a1;
            --border-light: rgba(7, 17, 31, 0.1);
            --border-subtle: rgba(7, 17, 31, 0.06);

            background-color: var(--bg-main) !important;
            background-image: none !important;
            color: var(--text-primary) !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }

        /* Override global dark text & headers */
        .index-editorial-prototype h1,
        .index-editorial-prototype h2,
        .index-editorial-prototype h3,
        .index-editorial-prototype h4 {
            color: var(--text-primary);
        }

        .index-editorial-prototype p {
            color: var(--text-secondary);
        }

        /* --- Serif Editorial Headings --- */
        .index-editorial-prototype .editorial-section-title,
        .index-editorial-prototype .featured-card-title,
        .index-editorial-prototype #metodologia .editorial-section-title,
        .index-editorial-prototype .method-step-title,
        .index-editorial-prototype #sobre-mi .section-title {
            font-family: Georgia, 'Times New Roman', serif;
        }

        /* --- Header Sticky & Legibilidad --- */
        .index-editorial-prototype #header {
            background: rgba(255, 255, 255, 0.95);
            border-bottom: 1px solid var(--border-light);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }

        .index-editorial-prototype #header.scrolled {
            background: rgba(255, 255, 255, 0.98);
            box-shadow: 0 4px 12px rgba(7, 17, 31, 0.05);
        }

        .index-editorial-prototype .logo {
            color: var(--text-primary);
            font-weight: 700;
        }

        .index-editorial-prototype .logo .text-gradient {
            color: var(--accent-cyan);
            background: none;
            -webkit-text-fill-color: initial;
        }

        .index-editorial-prototype .nav-links a {
            color: var(--text-secondary);
            font-weight: 500;
        }

        .index-editorial-prototype .nav-links a:hover,
        .index-editorial-prototype .nav-links a.active {
            color: var(--accent-cyan);
        }

        .index-editorial-prototype .nav-toggle {
            color: var(--text-primary);
        }

        /* --- Hero Editorial --- */
        .index-editorial-prototype .hero {
            background: var(--bg-main);
            padding-top: calc(80px + 3rem);
            padding-bottom: 4.5rem;
        }

        .index-editorial-prototype .hero-eyebrow {
            color: var(--accent-cyan);
            font-size: 0.82rem;
            font-weight: 700;
            letter-spacing: 0.16em;
            text-transform: uppercase;
        }

        .index-editorial-prototype .hero h1 {
            color: var(--text-primary);
            font-family: Georgia, 'Times New Roman', serif;
            font-size: clamp(2.4rem, 4.8vw, 3.8rem);
            line-height: 1.15;
            letter-spacing: -0.03em;
        }

        .index-editorial-prototype .hero .text-gradient {
            color: var(--accent-cyan);
            background: none;
            -webkit-text-fill-color: initial;
            font-style: normal;
        }

        .index-editorial-prototype .hero p {
            color: var(--text-secondary);
            font-size: 1.12rem;
            line-height: 1.7;
            max-width: 44rem;
        }

        .index-editorial-prototype .btn-primary {
            background: var(--accent-cyan);
            color: #ffffff;
            border: 1px solid var(--accent-cyan);
            font-weight: 600;
            box-shadow: none;
        }

        .index-editorial-prototype .btn-primary:hover {
            background: var(--accent-hover);
            border-color: var(--accent-hover);
            box-shadow: 0 4px 12px rgba(14, 116, 144, 0.25);
        }

        .index-editorial-prototype .btn-outline {
            color: var(--accent-cyan);
            border: 1px solid var(--accent-cyan);
            background: transparent;
            font-weight: 600;
        }

        .index-editorial-prototype .btn-outline:hover {
            background: rgba(14, 116, 144, 0.06);
            color: var(--accent-hover);
            border-color: var(--accent-hover);
        }

        /* --- Layout de Secciones de Alternancia Clara --- */
        .index-editorial-prototype .section-alt {
            background: var(--bg-alt);
            border-top: 1px solid var(--border-subtle);
            border-bottom: 1px solid var(--border-subtle);
        }

        .index-editorial-prototype .section-title {
            color: var(--text-primary);
            font-size: clamp(2rem, 3.5vw, 2.8rem);
            letter-spacing: -0.02em;
        }

        .index-editorial-prototype .section-title .text-gradient {
            color: var(--accent-cyan);
            background: none;
            -webkit-text-fill-color: initial;
        }

        .index-editorial-prototype .section-subtitle {
            color: var(--text-secondary);
        }

        /* --- 02 CASOS SELECCIONADOS (Colección Editorial Continua) --- */
        .index-editorial-prototype .editorial-section-intro {
            display: grid;
            grid-template-columns: minmax(0, 1.2fr) minmax(260px, 0.8fr);
            gap: 3rem;
            align-items: end;
            margin-bottom: 3rem;
        }

        .index-editorial-prototype .editorial-kicker {
            display: block;
            margin-bottom: 0.75rem;
            color: var(--accent-cyan);
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.16em;
            text-transform: uppercase;
        }

        .index-editorial-prototype .editorial-section-title {
            margin: 0;
            color: var(--text-primary);
            font-size: clamp(2.2rem, 4.5vw, 3.6rem);
            font-weight: 400;
            line-height: 1.02;
            letter-spacing: -0.03em;
        }

        .index-editorial-prototype .editorial-section-description {
            max-width: 34rem;
            margin: 0;
            color: var(--text-secondary);
            font-size: 1.05rem;
            line-height: 1.65;
        }

        .index-editorial-prototype .editorial-cases-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            border-top: 1px solid var(--border-light);
            border-bottom: 1px solid var(--border-light);
            background: var(--bg-surface);
        }

        .index-editorial-prototype .editorial-cases-grid .featured-card {
            min-width: 0;
            border: 0;
            border-left: 1px solid var(--border-light);
            border-radius: 0;
            background: transparent;
            box-shadow: none;
            backdrop-filter: none;
            -webkit-backdrop-filter: none;
            transform: none;
            transition: none;
            display: flex;
            flex-direction: column;
        }

        .index-editorial-prototype .editorial-cases-grid .featured-card:first-child {
            border-left: 0;
        }

        .index-editorial-prototype .editorial-cases-grid .featured-card-media {
            height: auto;
            aspect-ratio: 16 / 9;
            background: #e2e8f0;
            overflow: hidden;
        }

        .index-editorial-prototype .editorial-cases-grid .featured-card-img {
            display: block;
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s ease;
        }

        .index-editorial-prototype .editorial-cases-grid .featured-card:hover .featured-card-img {
            transform: scale(1.025);
        }

        .index-editorial-prototype .editorial-cases-grid .featured-card-content {
            min-width: 0;
            padding: 1.6rem 1.4rem 1.8rem;
            display: flex;
            flex-direction: column;
            flex-grow: 1;
        }

        .index-editorial-prototype .editorial-cases-grid .featured-card-location {
            color: var(--text-muted);
            font-size: 0.76rem;
            font-weight: 600;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            margin-bottom: 0.6rem;
            display: block;
        }

        .index-editorial-prototype .editorial-cases-grid .featured-card-location i {
            color: var(--accent-cyan);
            margin-right: 0.3rem;
        }

        .index-editorial-prototype .editorial-cases-grid .featured-card-title {
            color: var(--text-primary);
            font-size: 1.35rem;
            font-weight: 400;
            line-height: 1.25;
            margin-top: 0;
            margin-bottom: 0.5rem;
        }

        .index-editorial-prototype .editorial-cases-grid .featured-card-role {
            color: var(--accent-cyan);
            font-size: 0.84rem;
            font-weight: 600;
            margin-bottom: 0.9rem;
            display: block;
        }

        .index-editorial-prototype .editorial-cases-grid .featured-card-summary {
            color: var(--text-secondary);
            font-size: 0.96rem;
            line-height: 1.6;
            margin-bottom: 1.2rem;
            flex-grow: 1;
        }

        .index-editorial-prototype .featured-card-link {
            color: var(--accent-cyan);
            font-weight: 600;
            font-size: 0.92rem;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            margin-top: auto;
        }

        .index-editorial-prototype .featured-card-link:hover {
            color: var(--accent-hover);
        }

        /* --- Discretes Tags Control (No check icons, subtle rectangular) --- */
        .index-editorial-prototype .project-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 0.4rem;
        }

        .index-editorial-prototype .tag-item {
            font-size: 0.72rem;
            font-weight: 600;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            padding: 0.25rem 0.55rem;
            border-radius: 2px;
            background: rgba(7, 17, 31, 0.04);
            border: 1px solid var(--border-light);
            color: var(--text-secondary);
        }

        .index-editorial-prototype .tag-item i {
            display: none !important; /* Oculta íconos check según especificación */
        }

        /* --- 03 EN QUÉ PUEDO APORTAR (Especialidades) --- */
        .index-editorial-prototype .experience-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1.8rem;
        }

        .index-editorial-prototype .glass-card {
            background: var(--bg-surface);
            border: 1px solid var(--border-light);
            border-radius: 4px;
            padding: 2rem 1.75rem;
            box-shadow: 0 2px 6px rgba(7, 17, 31, 0.02);
            backdrop-filter: none;
            -webkit-backdrop-filter: none;
            transition: border-color 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease;
        }

        .index-editorial-prototype .glass-card:hover {
            border-color: rgba(14, 116, 144, 0.4);
            box-shadow: 0 6px 20px rgba(7, 17, 31, 0.06);
            transform: translateY(-2px);
        }

        .index-editorial-prototype .glass-card h3 {
            color: var(--text-primary);
            font-size: 1.25rem;
            font-weight: 600;
            margin-top: 1rem;
            margin-bottom: 0.8rem;
        }

        .index-editorial-prototype .glass-card p {
            color: var(--text-secondary);
            font-size: 0.98rem;
            line-height: 1.65;
        }

        .index-editorial-prototype .card-icon i {
            color: var(--accent-cyan);
            font-size: 2rem;
        }

        /* --- 04 MÁS CASOS Y OTROS PROYECTOS --- */
        .index-editorial-prototype .more-cases-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1.8rem;
            margin-bottom: 3.5rem;
        }

        .index-editorial-prototype .secondary-card {
            background: var(--bg-surface);
            border: 1px solid var(--border-light);
            border-radius: 4px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }

        .index-editorial-prototype .secondary-card:hover {
            border-color: rgba(14, 116, 144, 0.4);
            box-shadow: 0 6px 18px rgba(7, 17, 31, 0.06);
        }

        .index-editorial-prototype .secondary-card-media {
            aspect-ratio: 16 / 9;
            overflow: hidden;
            background: #e2e8f0;
        }

        .index-editorial-prototype .secondary-card-img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s ease;
        }

        .index-editorial-prototype .secondary-card:hover .secondary-card-img {
            transform: scale(1.03);
        }

        .index-editorial-prototype .secondary-card-content {
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            flex-grow: 1;
        }

        .index-editorial-prototype .secondary-card-location {
            color: var(--text-muted);
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-bottom: 0.5rem;
        }

        .index-editorial-prototype .secondary-card-location i {
            color: var(--accent-cyan);
            margin-right: 0.25rem;
        }

        .index-editorial-prototype .secondary-card-title {
            color: var(--text-primary);
            font-size: 1.18rem;
            font-weight: 600;
            line-height: 1.3;
            margin-top: 0;
            margin-bottom: 0.6rem;
        }

        .index-editorial-prototype .secondary-card-summary {
            color: var(--text-secondary);
            font-size: 0.94rem;
            line-height: 1.6;
            margin-bottom: 1.2rem;
            flex-grow: 1;
        }

        /* Otros Proyectos Compactos */
        .index-editorial-prototype .other-projects-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1.5rem;
        }

        .index-editorial-prototype .other-project-card {
            background: var(--bg-surface);
            border: 1px solid var(--border-light);
            border-radius: 4px;
            padding: 1.4rem;
        }

        .index-editorial-prototype .other-project-card h4 {
            color: var(--accent-cyan);
            font-size: 1.1rem;
            font-weight: 700;
            margin-top: 0;
            margin-bottom: 0.3rem;
        }

        .index-editorial-prototype .other-project-subtitle {
            color: var(--text-primary);
            font-size: 0.88rem;
            font-weight: 600;
            display: block;
            margin-bottom: 0.9rem;
        }

        /* --- 05 MI FORMA DE TRABAJAR (Proceso Editorial) --- */
        .index-editorial-prototype .editorial-process-summary {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            padding: 1rem 1.6rem;
            background: var(--bg-surface);
            border: 1px solid var(--border-light);
            border-radius: 4px;
            margin-bottom: 3rem;
            color: var(--text-secondary);
            font-size: 0.92rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .index-editorial-prototype .editorial-process-summary span {
            color: var(--text-primary);
        }

        .index-editorial-prototype .editorial-process-summary i {
            color: var(--accent-cyan);
        }

        .index-editorial-prototype .editorial-method-grid {
            position: relative;
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 2rem;
        }

        .index-editorial-prototype .editorial-method-grid::before {
            content: '';
            position: absolute;
            top: 22px;
            left: 2rem;
            right: 2rem;
            height: 2px;
            background: rgba(14, 116, 144, 0.25);
            z-index: 1;
        }

        .index-editorial-prototype .editorial-method-grid .method-step {
            position: relative;
            z-index: 2;
            background: transparent;
        }

        .index-editorial-prototype .editorial-method-grid .method-step-num {
            width: 44px;
            height: 44px;
            background: var(--accent-cyan);
            color: #ffffff;
            font-size: 1rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 4px;
            margin-bottom: 1.2rem;
        }

        .index-editorial-prototype .editorial-method-grid .method-step-title {
            color: var(--text-primary);
            font-size: 1.3rem;
            font-weight: 400;
            margin-top: 0;
            margin-bottom: 0.4rem;
        }

        .index-editorial-prototype .editorial-method-concept {
            color: var(--accent-cyan);
            font-style: italic;
            font-size: 0.95rem;
            font-weight: 500;
            margin-bottom: 0.8rem;
        }

        .index-editorial-prototype .editorial-method-grid .method-step p:not(.editorial-method-concept) {
            color: var(--text-secondary);
            font-size: 0.95rem;
            line-height: 1.6;
        }

        /* --- 06 SOBRE MÍ Y TRAYECTORIA --- */
        .index-editorial-prototype .about-milestones {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1.5rem;
        }

        .index-editorial-prototype .about-milestone-card {
            background: var(--bg-surface);
            border: 1px solid var(--border-light);
            border-radius: 4px;
            padding: 1.6rem 1.4rem;
        }

        .index-editorial-prototype .about-milestone-card h4 {
            color: var(--text-primary);
            font-size: 1.1rem;
            font-weight: 600;
            margin-top: 0.8rem;
            margin-bottom: 0.5rem;
        }

        .index-editorial-prototype .about-milestone-card p {
            color: var(--text-secondary);
            font-size: 0.92rem;
            line-height: 1.6;
        }

        .index-editorial-prototype .about-milestone-card .milestone-icon i {
            color: var(--accent-cyan);
            font-size: 1.5rem;
        }

        /* ============================================================
           TRANSICIÓN DELIBERADA A FONDO OSCURO TECNOLÓGICO
           Punto de Quiebre: #innovacion + footer#contacto
           ============================================================ */
        .index-editorial-prototype #innovacion {
            background-color: #07111F !important;
            color: #F8FAFC !important;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            padding-top: 5rem;
            padding-bottom: 5rem;
        }

        .index-editorial-prototype #innovacion .section-title {
            color: #F8FAFC !important;
        }

        .index-editorial-prototype #innovacion .section-title .text-gradient {
            color: #38BDF8 !important;
            background: none !important;
            -webkit-text-fill-color: initial !important;
        }

        .index-editorial-prototype #innovacion p {
            color: #94A3B8 !important;
        }

        .index-editorial-prototype .innovation-highlight {
            background: rgba(56, 189, 248, 0.05);
            border: 1px solid rgba(56, 189, 248, 0.25);
            border-radius: 6px;
            padding: 1.8rem;
        }

        .index-editorial-prototype .innovation-highlight h3 {
            color: #38BDF8 !important;
            font-size: 1.5rem;
            margin-top: 0;
            margin-bottom: 0.5rem;
        }

        .index-editorial-prototype .innovation-highlight strong {
            color: #F8FAFC !important;
        }

        .index-editorial-prototype .platform-note {
            color: #64748B !important;
            font-size: 0.85rem;
        }

        .index-editorial-prototype .theogen-box {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 2.5rem 2rem;
            text-align: center;
        }

        .index-editorial-prototype .theogen-box h3 {
            color: #F8FAFC !important;
            font-size: 1.35rem;
            margin-bottom: 1.5rem;
        }

        .index-editorial-prototype .pipeline-flow {
            background: rgba(56, 189, 248, 0.1);
            border: 1px solid rgba(56, 189, 248, 0.2);
            border-radius: 30px;
            padding: 0.6rem 1.4rem;
            color: #38BDF8 !important;
            font-weight: 600;
            display: inline-flex;
            gap: 0.6rem;
            align-items: center;
        }

        .index-editorial-prototype .pipeline-flow span {
            color: #38BDF8 !important;
        }

        /* --- Footer Oscuro Coherente (#contacto) --- */
        .index-editorial-prototype footer#contacto {
            background-color: #050B14 !important;
            border-top: 1px solid rgba(255, 255, 255, 0.08);
            color: #F8FAFC !important;
            padding-top: 5rem;
            padding-bottom: 3.5rem;
        }

        .index-editorial-prototype footer#contacto .footer-heading {
            color: #F8FAFC !important;
            font-family: Georgia, 'Times New Roman', serif;
            font-size: clamp(2rem, 3.5vw, 3rem);
        }

        .index-editorial-prototype footer#contacto .footer-audience,
        .index-editorial-prototype footer#contacto .footer-cta-text {
            color: #94A3B8 !important;
        }

        .index-editorial-prototype footer#contacto .btn-primary {
            background: #0284c7;
            border-color: #0284c7;
            color: #ffffff;
        }

        .index-editorial-prototype footer#contacto .btn-primary:hover {
            background: #0369a1;
            border-color: #0369a1;
        }

        .index-editorial-prototype footer#contacto .btn-outline {
            color: #38bdf8;
            border-color: #38bdf8;
            background: transparent;
        }

        .index-editorial-prototype footer#contacto .btn-outline:hover {
            background: rgba(56, 189, 248, 0.1);
            color: #7dd3fc;
            border-color: #7dd3fc;
        }

        .index-editorial-prototype footer#contacto .footer-copy {
            color: #64748B !important;
            border-top: 1px solid rgba(255, 255, 255, 0.06);
            padding-top: 2rem;
            margin-top: 3.5rem;
        }

        /* ============================================================
           BREAKPOINTS RESPONSIVE STRICT RULES (QA 320 - 1440px)
           Reglas de Grilla:
           - Casos seleccionados: 3 cols -> 1 col (o 2+1 deliberado)
           - Especialidades: 3 cols -> 1 col (evita 2+1 desequilibrado)
           - Más casos: 3 cols -> 1 col
           - Otros proyectos: 3 cols -> 1 col
           - Proceso: 4 cols -> 2x2 tablet -> 1 col móvil (APROBADO)
           - Trayectoria: 4 cols -> 2x2 tablet -> 1 col móvil (NO 3+1)
           ============================================================ */

        @media (max-width: 1024px) {
            .index-editorial-prototype .editorial-section-intro {
                grid-template-columns: 1fr;
                gap: 1.2rem;
                align-items: start;
            }

            .index-editorial-prototype .editorial-section-description {
                max-width: 100%;
            }

            .index-editorial-prototype .editorial-method-grid {
                grid-template-columns: repeat(2, 1fr);
                gap: 2.5rem 2rem;
            }

            .index-editorial-prototype .editorial-method-grid::before {
                display: none; /* Oculta línea continua en 2x2 */
            }

            .index-editorial-prototype .about-milestones {
                grid-template-columns: repeat(2, 1fr); /* 2x2 APROBADO */
            }
        }

        @media (max-width: 992px) {
            /* Cambio de 3 columnas a 1 columna para EVITAR tarjetas aisladas 2+1 */
            .index-editorial-prototype .editorial-cases-grid {
                grid-template-columns: 1fr;
                border-top: 1px solid var(--border-light);
                border-bottom: 1px solid var(--border-light);
            }

            .index-editorial-prototype .editorial-cases-grid .featured-card {
                border-left: 0;
                border-top: 1px solid var(--border-light);
            }

            .index-editorial-prototype .editorial-cases-grid .featured-card:first-child {
                border-top: 0;
            }

            .index-editorial-prototype .experience-grid {
                grid-template-columns: 1fr;
            }

            .index-editorial-prototype .more-cases-grid {
                grid-template-columns: 1fr;
            }

            .index-editorial-prototype .other-projects-grid {
                grid-template-columns: 1fr;
            }
        }

        @media (max-width: 640px) {
            .index-editorial-prototype .hero {
                padding-top: calc(70px + 2rem);
                padding-bottom: 3rem;
            }

            .index-editorial-prototype .editorial-process-summary {
                flex-direction: column;
                align-items: flex-start;
                gap: 0.5rem;
            }

            .index-editorial-prototype .editorial-process-summary i {
                transform: rotate(90deg);
                margin: 0.2rem 0;
            }

            .index-editorial-prototype .editorial-method-grid {
                grid-template-columns: 1fr;
                gap: 2rem;
            }

            .index-editorial-prototype .about-milestones {
                grid-template-columns: 1fr;
            }
        }

        @media (prefers-reduced-motion: reduce) {
            .index-editorial-prototype .editorial-cases-grid .featured-card-img,
            .index-editorial-prototype .secondary-card-img,
            .index-editorial-prototype .glass-card,
            .index-editorial-prototype .secondary-card {
                transition: none !important;
                transform: none !important;
            }
        }
    </style>"""

with open('index_2.html', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = re.compile(r'<style>.*?</style>', re.DOTALL)
new_content = pattern.sub(css_content, content)

with open('index_2.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("SUCCESSFULLY_UPDATED_INDEX_2_STYLE")
