using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

var builder = Host.CreateApplicationBuilder(args);

// Configuración obligatoria para servidores MCP STDIO:
// Evitamos que los logs internos escriban en Console.Out (salida estándar),
// ya que la salida estándar se usa exclusivamente para los mensajes JSON-RPC del MCP.
builder.Logging.ClearProviders();

// Registramos el servidor MCP
builder.Services.AddMcpServer(options => 
{
    options.ServerInfo = new()
    {
        Name = "AutoCAD_AI_Context_Server",
        Version = "1.0.0"
    };
})
.WithStdioServerTransport()        // Comunicación por STDIO (estándar para IA local)
.WithTools<AutoCAD_MCP_Server.AutoCADTools>(); // Registramos la clase de herramientas

var host = builder.Build();
await host.RunAsync();
