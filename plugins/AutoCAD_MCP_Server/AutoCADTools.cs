using System.ComponentModel;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using System;
using ModelContextProtocol;
using ModelContextProtocol.Server;

namespace AutoCAD_MCP_Server;

[McpServerToolType]
public class AutoCADTools
{
    private readonly HttpClient _httpClient;

    public AutoCADTools()
    {
        _httpClient = new HttpClient();
        // Conexión al Gateway de AutoCAD que corre en .NET 10 dentro del proceso de AutoCAD
        _httpClient.BaseAddress = new Uri("http://localhost:5055/");
    }

    private async Task<string> GetJsonAsync(string endpoint)
    {
        try
        {
            var response = await _httpClient.GetAsync(endpoint);
            if (response.IsSuccessStatusCode)
            {
                return await response.Content.ReadAsStringAsync();
            }
            return $"{{\"status\": \"error\", \"code\": {(int)response.StatusCode}, \"message\": \"Gateway devolvió error {response.StatusCode}\"}}";
        }
        catch (Exception ex)
        {
            return $"{{\"status\": \"error\", \"message\": \"Fallo al conectar con el Gateway en puerto 5055: {ex.Message}\"}}";
        }
    }

    [McpServerTool(Name = "ping_autocad_gateway")]
    [Description("Envía un ping al Gateway de AutoCAD para verificar la conectividad.")]
    public async Task<string> PingAutoCAD()
    {
        try
        {
            var payload = new { command = " \n" };
            var content = new StringContent(JsonSerializer.Serialize(payload), Encoding.UTF8, "application/json");
            var response = await _httpClient.PostAsync("execute", content);

            if (response.IsSuccessStatusCode)
                return "¡Conexión exitosa con el AutoCAD AI Gateway!";

            return $"Conectado al Gateway, pero devolvió el estado: {response.StatusCode}";
        }
        catch (Exception ex)
        {
            return $"Fallo crítico al conectar con el Gateway de AutoCAD. Asegúrate de que AutoCAD esté abierto y el Gateway ejecutándose en el puerto 5055. Error: {ex.Message}";
        }
    }

    [McpServerTool(Name = "obtener_info_dibujo")]
    [Description("Obtiene metadatos del dibujo activo en AutoCAD: nombre de archivo DWG, estado de solo lectura y unidades configuradas.")]
    public async Task<string> ObtenerInfoDibujo() => await GetJsonAsync("context/info");

    [McpServerTool(Name = "leer_objetos_autocad")]
    [Description("Lee y devuelve un resumen (conteos por tipo) de todas las entidades y objetos que existen actualmente en el dibujo de AutoCAD (ModelSpace).")]
    public async Task<string> LeerObjetosAutoCAD() => await GetJsonAsync("context/entities");

    [McpServerTool(Name = "leer_capas_autocad")]
    [Description("Obtiene la lista completa de capas del dibujo de AutoCAD con sus estados (bloqueada, congelada, apagada) y código de color.")]
    public async Task<string> LeerCapasAutoCAD() => await GetJsonAsync("context/layers");

    [McpServerTool(Name = "leer_textos_autocad")]
    [Description("Lista todos los textos (DBText y MText) del dibujo con sus contenidos, coordenadas exactas (X, Y) y capa para ubicar ambientes (ej. DORMITORIO, SALA, BAÑO).")]
    public async Task<string> LeerTextosAutoCAD() => await GetJsonAsync("context/texts");

    [McpServerTool(Name = "obtener_limites_dibujo")]
    [Description("Obtiene las coordenadas mínimas (X, Y) y máximas (X, Y) del dibujo actual (Extmin y Extmax) para calcular áreas de diseño libres.")]
    public async Task<string> ObtenerLimitesDibujo() => await GetJsonAsync("context/extents");

    [McpServerTool(Name = "leer_seleccion_autocad")]
    [Description("Obtiene el número de entidades seleccionadas actualmente por el usuario con el ratón en AutoCAD.")]
    public async Task<string> LeerSeleccionAutoCAD() => await GetJsonAsync("context/selection");

    [McpServerTool(Name = "listar_bloques_disponibles")]
    [Description("Obtiene los nombres de todas las definiciones de bloques cargadas en el archivo actual.")]
    public async Task<string> ListarBloquesDisponibles() => await GetJsonAsync("context/blocks");

    [McpServerTool(Name = "ejecutar_comando_autocad")]
    [Description("Envía comandos de dibujo, macros AutoLISP o comandos YQArch (ej. WW, JJ, AD, WD, ZXW) directamente a AutoCAD a través del Gateway. Los comandos deben incluir saltos de línea (\\n) donde se requiera pulsar Enter.")]
    public async Task<string> EjecutarComandoAutoCAD(string command)
    {
        try
        {
            var payload = new { command = command };
            var content = new StringContent(JsonSerializer.Serialize(payload), Encoding.UTF8, "application/json");

            var response = await _httpClient.PostAsync("execute", content);

            if (response.IsSuccessStatusCode)
            {
                return "Éxito: El comando se inyectó correctamente en AutoCAD.";
            }
            else
            {
                string errorDetalle = await response.Content.ReadAsStringAsync();
                return $"Error del Gateway ({response.StatusCode}): {errorDetalle}";
            }
        }
        catch (Exception ex)
        {
            return $"Fallo crítico de conexión con el Gateway de AutoCAD. Asegúrate de que el puerto 5055 esté encendido. Error: {ex.Message}";
        }
    }

    [McpServerTool(Name = "zoom_extension")]
    [Description("Ejecuta un Zoom Extensión ('_.ZOOM E') en AutoCAD para encuadrar y centrar automáticamente todos los elementos en pantalla.")]
    public async Task<string> ZoomExtension() => await EjecutarComandoAutoCAD("_.ZOOM\nE\n");

    [McpServerTool(Name = "guardar_dibujo")]
    [Description("Guarda el archivo de dibujo actual en AutoCAD ('_.QSAVE').")]
    public async Task<string> GuardarDibujo() => await EjecutarComandoAutoCAD("_.QSAVE\n");

    [McpServerTool(Name = "configurar_entorno_dibujo")]
    [Description("Configura el entorno de trabajo activo en AutoCAD a METROS (INSUNITS=4, MEASUREMENT=1, LUNITS=2, LUPREC=3) y calibra las escalas de cotas/textos para evitar anotaciones gigantescas o microscópicas.")]
    public async Task<string> ConfigurarEntornoDibujo()
    {
        string script =
            "_.-SETVAR\nINSUNITS\n4\n" +
            "_.-SETVAR\nMEASUREMENT\n1\n" +
            "_.-SETVAR\nLUNITS\n2\n" +
            "_.-SETVAR\nLUPREC\n3\n" +
            "_.-SETVAR\nAUNITS\n0\n" +
            "_.-SETVAR\nANGBASE\n0.0\n" +
            "_.-SETVAR\nANGDIR\n0\n" +
            "_.-SETVAR\nDIMTXT\n0.22\n" +
            "_.-SETVAR\nDIMASZ\n0.18\n" +
            "_.-SETVAR\nDIMEXE\n0.11\n" +
            "_.-SETVAR\nDIMEXO\n0.06\n" +
            "_.-SETVAR\nDIMGAP\n0.08\n" +
            "_.-SETVAR\nDIMDEC\n2\n" +
            "_.-SETVAR\nDIMTAD\n1\n" +
            "_.UCS\nW\n";
        return await EjecutarComandoAutoCAD(script);
    }
}
