# Actualizaciones del cliente

El manifest público (`manifests/release.json`, `manifests/dims-subset.json`) puede actualizarse **como máximo una vez al día** cuando hay cambios verificados en el backend del operador.

Los usuarios del repo clonado:

```bash
./scripts/update.sh
```

Ver [actualizaciones.md](actualizaciones.md).

El pipeline de publicación (cron, git push) es **operación del proveedor** — no forma parte de la instalación estándar del cliente.
