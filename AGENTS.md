# AGENTS.md — Guía para trabajar en esta landing page

Este archivo le dice a Claude (y a cualquier otro agente de código) cómo trabajar en este proyecto. Si sos la persona que va a mantener esta landing y no programás: no hace falta que leas esto en detalle. Conversá con Claude Code y pedile lo que necesites en lenguaje normal — "cambiá el color del botón a azul", "agregá una sección de testimonios", "el texto del hero debería decir esto otro" — y Claude va a seguir las reglas de acá abajo automáticamente.

## Qué es este proyecto

Una landing page hecha con **HTML, CSS y JavaScript planos**. Sin frameworks (nada de React/Next/Vue), sin bundlers, sin paso de build, sin `npm install`. Se abre directo en el navegador y listo.

Esto es intencional: mantenerlo simple para que se pueda editar, entender y desplegar sin herramientas complejas. El despliegue y CI/CD los maneja el dueño del repo por fuera de este flujo — no hace falta configurar nada de eso acá.

## Estructura de archivos

- `index.html` — página principal.
- `css/styles.css` — todos los estilos. Usa variables CSS (`:root { --color-primario: ...; }`) para colores, tipografías y espaciados, así cambiar la identidad visual es cuestión de tocar pocas líneas en un solo lugar.
- `js/main.js` — cualquier interactividad (menú móvil, formulario, animaciones simples). Solo JS vanilla, sin librerías salvo que sea estrictamente necesario y se justifique primero.
  - Excepción aprobada: **GSAP vía CDN** (`<script src="https://cdn.jsdelivr.net/npm/gsap@3.15/dist/gsap.min.js">`) para animaciones. No usar otras librerías de animación sin preguntar.
- `assets/img/` — imágenes e íconos.
- Si el sitio crece a más de una página, cada página es un `.html` nuevo en la raíz (ej. `contacto.html`), reutilizando el mismo `css/styles.css`.

No crear carpetas de build ni agregar `package.json`/dependencias salvo que el dueño del proyecto lo pida explícitamente.

## Cómo trabajar

- HTML semántico (`<header>`, `<nav>`, `<main>`, `<section>`, `<footer>`) en vez de `<div>` genéricos.
- Mobile-first: el sitio debe verse bien en celular antes que en escritorio.
- El contenido esencial debe funcionar sin JavaScript.
- Sin comentarios explicando qué hace el código, salvo que algo no sea obvio.
- No introducir frameworks, bundlers ni dependencias externas sin preguntar antes — es una decisión de arquitectura, no algo para decidir sobre la marcha.
- Si hay texto o imágenes de relleno ("lorem ipsum", placeholders) porque todavía no hay contenido real, marcarlo de forma obvia (ej. comentario HTML `<!-- TODO: reemplazar por foto real -->`) para que quede claro qué falta.
- Cuando el pedido sea ambiguo ("hacelo más lindo", "que se vea más profesional"), preguntar qué estilo o referencia tiene en mente, o proponer 2-3 opciones concretas en vez de adivinar y rehacer todo.

## Deploy

- **URL de producción**: https://landingboda-landingboda-pn8vrl-da8444-13-140-162-46.sslip.io
- Desplegado en **Dokploy** (build type **Static**, sirve el repo directo con NGINX vía un `Dockerfile` que genera Dokploy automáticamente — no hay `Dockerfile` en el repo).
- **Trigger**: cada `git push` a `main` redeploya solo (Trigger Type: On Push).
- El dominio es un subdominio temporal de `sslip.io` (no soporta HTTPS real); cuando haya un dominio propio, actualizar esta URL.
- **Rama de trabajo**: `main` — no hay otras ramas ni entornos de staging, todo lo que se pushea ahí queda en producción directo.
- Los colaboradores del repo con permiso de escritura pueden hacer `commit` y `push` a `main` directamente cuando necesiten disparar un deploy — no hace falta pasar por Pull Request para publicar cambios.
