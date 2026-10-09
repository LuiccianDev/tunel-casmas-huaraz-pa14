using System;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using AutoCAD_MCP_Server.Services;
using AutoCAD_MCP_Server.Tools;

var builder = Host.CreateApplicationBuilder(args);

// Configuración obligatoria para servidores MCP STDIO:
// Se eliminan los proveedores de logging hacia Console.Out (salida estándar)
// para proteger el flujo de tramas JSON-RPC del protocolo Model Context Protocol.
builder.Logging.ClearProviders();

// Registro de servicios: Cliente HTTP tipado hacia el Gateway de AutoCAD en puerto 5055
builder.Services.AddHttpClient<IAutoCADGatewayClient, AutoCADGatewayClient>(client =>
{
    client.BaseAddress = new Uri("http://localhost:5055/");
    client.Timeout = TimeSpan.FromSeconds(15);
    string token = Environment.GetEnvironmentVariable("AUTOCAD_GATEWAY_TOKEN") ?? "pa14-autocad-token-casmas-2026";
    client.DefaultRequestHeaders.Add("X-Gateway-Token", token);
});

// Registro del servidor MCP con sus clases modulares de herramientas
builder.Services.AddMcpServer(options =>
{
    options.ServerInfo = new()
    {
        Name = "AutoCAD_AI_Context_Server",
        Version = "1.0.0"
    };
})
.WithStdioServerTransport()
.WithTools<ContextTools>()
.WithTools<ExecutionTools>();

var host = builder.Build();
await host.RunAsync();
