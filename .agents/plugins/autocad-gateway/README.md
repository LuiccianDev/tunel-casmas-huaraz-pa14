# AutoCAD & Civil 3D AI Gateway (`autocad-gateway`)

Bundle de integración interactiva en tiempo real con **AutoCAD 2027** y **Civil 3D 2027** mediante el plugin nativo en C# (.NET 10) y el servidor Model Context Protocol (`autocad-mcp`).

## Contenido del Paquete

- **Servidor MCP (`mcp_config.json`)**:
  - `autocad-mcp`: Expone 20 herramientas MCP v2.2 para inspección bidireccional del dibujo, ejecución de comandos seguros en el puerto `5055` y operaciones viales en Civil 3D.
- **Reglas (`rules/AGENTS.md`)**:
  - Estándares C#/.NET 10, seguridad de hilos (`Application.Idle`), transporte autenticado (`X-Gateway-Token`) y calibración métrica estricta (`INSUNITS = 4`).
- **Skills (`skills/`)**:
  - `clean-code`: Principios de diseño limpio y refactorización.
  - `csharp-docs`: Documentación XML estándar para tipos y métodos C#.
  - `dotnet-backend-patterns`: Patrones asíncronos, inyección de dependencias y arquitectura .NET.
  - `dotnet-best-practices`: Buenas prácticas de compilación y nulabilidad en .NET 10.
  - `dotnet-mcp-builder`: Construcción y mantenimiento de servidores MCP v2.x en C#.
  - `yqarch-fast-drafting`: Flujo secuencial para planos arquitectónicos con YQArch e índice de referencia en `references/yqarch_commands.md`.
