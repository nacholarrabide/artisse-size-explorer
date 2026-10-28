# Prompt para Cursor en el proyecto que sirve angioseg.arroyoseco.tech

Quiero desplegar el prototipo Contour Explorer en la misma máquina y dominio de
Angioseg, mediante la ruta canónica:

https://angioseg.arroyoseco.tech/contour.html

Podés usar /contour/ como alias con redirección. No crear un subdominio ni un
alojamiento nuevo. El dominio ya llega a esta máquina mediante un reverse proxy;
identificá primero la configuración ACTIVA, sin asumir que el nginx del repo sea
el que está en uso.

## Fuente y alcance

La fuente canónica es /home/nacho/devel/artisse_size_explorer/contour.html,
repositorio git@github.com:nacholarrabide/artisse-size-explorer.git. Usá el archivo
actual confirmado y registrá commit y SHA-256 del archivo desplegado. No hagas
pull ni descartes cambios locales sin inspeccionar antes el estado. Si la fuente
no está disponible, pedime la ubicación; no reconstruyas ni reemplaces el modelo.

Es un único HTML con CSS/JS/SVG embebidos, sin backend de cálculo, dependencias,
GPU, base de datos o peticiones externas para funcionar. Tiene presets visuales,
comparaciones, banco de experimentos y exportación/importación local JSON/SVG.
Conservá la interfaz en inglés y todas las advertencias de modelo sintético no
validado. No modificar las ecuaciones durante este despliegue.

El código fuente se mantiene en su repo. En Angioseg, incorporá un procedimiento
reproducible para copiar/publicar una versión explícita y verificar su checksum;
no conviertas dos copias editables en fuentes divergentes. Serví exclusivamente
el archivo necesario, nunca el checkout completo ni carpetas padre.

## Acceso

Para este piloto de equipo, prepará la ruta con autenticación de Angioseg y una
lista explícita de usuarios autorizados o un permiso equivalente. Un usuario
registrado no implica automáticamente permiso para este prototipo. Reutilizá la
sesión existente, sin crear un segundo sistema de contraseñas. Si faltan los
usuarios autorizados, completá y probá el mecanismo y pedime sus identificadores
antes de habilitar acceso real; no inventes destinatarios ni abras la ruta como
alternativa. El acceso se debe verificar en el servidor ANTES de entregar el HTML,
no solo mediante ocultación en la interfaz o JavaScript.

Si el sistema no dispone de esa autorización, explicá la alternativa más pequeña
compatible con el despliegue existente. No uses una URL difícil de adivinar como
control de acceso. Evitá cachear la respuesta protegida públicamente; comprobá
que proxy, cookies, redirecciones y políticas de seguridad no anulan la protección.

## Procedimiento

1. Leé AGENTS.md y las instrucciones del proyecto destino. Identificá servicios,
   puerto local, mecanismo de despliegue, proxy activo y autenticación actual.
   No imprimas credenciales ni tokens. Inspeccioná cambios locales antes de editar.
2. Proponé y ejecutá un cambio pequeño, reversible y registrado en el plan/etapa
   que exija el repositorio. Si FastAPI ya sirve el sitio, una ruta que entregue
   un FileResponse protegido puede ser suficiente; verificá el middleware real.
3. Revisá CSP para el HTML autocontenido, sin relajar globalmente las protecciones
   de Angioseg. No añadir servicios públicos de desarrollo ni exponer nuevos
   puertos a Internet. No tocar inferencia, GPU, datasets ni módulos del motor.
4. Prepará rollback del archivo y configuración. Ejecutá las pruebas exigidas por
   el proyecto y pruebas específicas de la ruta: anónimo sin HTML, usuario sin
   permiso denegado, usuario autorizado con HTML. Probá también los alias para
   evitar rutas alternativas sin protección.
5. Mostrame el cambio concreto, pruebas y procedimiento de activación antes de
   modificar el servicio activo. Con mi aprobación, desplegá usando el mecanismo
   existente y recargá/reiniciá solo el servicio necesario. Verificá desde el
   dominio externo tanto acceso autorizado como denegado; una prueba localhost
   sola no confirma el despliegue externo.
6. En navegador, verificá los tres presets (C5, C7, C9, sin comparación inicial), sliders,
   adaptación de ambas copas, barridos, JSON y SVG. Confirmá que los experimentos
   funcionan en el navegador sin enviar sus datos al servidor.
7. Comprobá que login, interfaz y salud de Angioseg siguen funcionando. Registrá
   versión desplegada, checksum, URL, política de acceso, pruebas y rollback.
   Hacé commit/push según las instrucciones del repo destino. Si una comprobación
   externa no es posible, indicá qué quedó sin verificar; no declares éxito total.

## Datos

No hay autorización para publicar casos clínicos. Los aneurismas y dispositivos
reales segmentados se incorporarán más adelante en un flujo privado, fuera de
ambos repositorios públicos y de las carpetas servidas. No cargar ni buscar esos
datos para este despliegue. Los presets actuales son completamente sintéticos.

Resultado esperado: una instalación reproducible, accesible al equipo autorizado
mediante el dominio indicado, con el resto de Angioseg intacto y sin presentar el
explorer como herramienta clínicamente validada.
