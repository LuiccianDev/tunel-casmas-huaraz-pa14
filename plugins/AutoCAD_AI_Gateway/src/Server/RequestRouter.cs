using System;
using System.IO;
using System.Net;
using System.Text.Json;
using System.Threading.Tasks;
using AutoCAD_AI_Gateway.Core;
using AutoCAD_AI_Gateway.Core.Models;
using AutoCAD_AI_Gateway.Services;

namespace AutoCAD_AI_Gateway.Server;

/// <summary>
/// Enruta las solicitudes HTTP entrantes hacia el despachador de comandos o el lector de contexto correspondiente.
/// </summary>
public sealed class RequestRouter
{
    private readonly IAutoCADCommandDispatcher _dispatcher;
    private readonly IAutoCADContextReader _contextReader;

    /// <summary>
    /// Inicializa una nueva instancia de la clase <see cref="RequestRouter"/>.
    /// </summary>
    /// <param name="dispatcher">El despachador de comandos de AutoCAD.</param>
    /// <param name="contextReader">El lector de contexto y base de datos de AutoCAD.</param>
    public RequestRouter(IAutoCADCommandDispatcher dispatcher, IAutoCADContextReader contextReader)
    {
        _dispatcher = dispatcher ?? throw new ArgumentNullException(nameof(dispatcher));
        _contextReader = contextReader ?? throw new ArgumentNullException(nameof(contextReader));
    }

    /// <summary>
    /// Procesa una solicitud HTTP y genera la tupla de código de estado y cuerpo de respuesta JSON.
    /// </summary>
    /// <param name="request">La solicitud HTTP recibida por el listener.</param>
    /// <returns>Una tarea asíncrona con el código de estado HTTP y el contenido JSON devuelto.</returns>
    public async Task<(int StatusCode, string ResponseBody)> RouteRequestAsync(HttpListenerRequest request)
    {
        string path = request.Url?.AbsolutePath ?? string.Empty;
        string method = request.HttpMethod;

        try
        {
            if (method == "POST" && path == "/execute")
            {
                using var reader = new StreamReader(request.InputStream, request.ContentEncoding);
                string payload = await reader.ReadToEndAsync();

                if (string.IsNullOrWhiteSpace(payload))
                {
                    return (400, "{\"status\": \"error\", \"message\": \"El cuerpo de la solicitud no puede estar vacio.\"}");
                }

                CommandRequest? cmdRequest;
                try
                {
                    cmdRequest = JsonSerializer.Deserialize<CommandRequest>(payload);
                }
                catch (JsonException ex)
                {
                    return (400, $"{{\"status\": \"error\", \"message\": \"JSON invalido: {ex.Message}\"}}");
                }

                if (cmdRequest == null || string.IsNullOrEmpty(cmdRequest.Command))
                {
                    return (400, "{\"status\": \"error\", \"message\": \"JSON invalido. Se requiere la clave 'command' con contenido.\"}");
                }

                _dispatcher.EnqueueCommand(cmdRequest.Command);
                return (200, "{\"status\": \"success\", \"message\": \"Comando encolado correctamente\"}");
            }

            if (method == "GET")
            {
                return path switch
                {
                    "/context/selection" => (200, await _contextReader.ReadSelectionCountAsync()),
                    "/context/entities"  => (200, await _contextReader.ReadEntityCountsAsync()),
                    "/context/info"      => (200, await _contextReader.ReadDrawingInfoAsync()),
                    "/context/layers"    => (200, await _contextReader.ReadLayersAsync()),
                    "/context/extents"   => (200, await _contextReader.ReadExtentsAsync()),
                    "/context/texts"     => (200, await _contextReader.ReadTextsAsync()),
                    "/context/blocks"    => (200, await _contextReader.ReadBlocksAsync()),
                    _                    => (404, "{\"status\": \"error\", \"message\": \"Ruta no encontrada.\"}")
                };
            }

            return (405, "{\"status\": \"error\", \"message\": \"Metodo HTTP no permitido.\"}");
        }
        catch (Exception ex)
        {
            return (500, $"{{\"status\": \"error\", \"message\": \"Error interno en el Gateway: {ex.Message}\"}}");
        }
    }
}
