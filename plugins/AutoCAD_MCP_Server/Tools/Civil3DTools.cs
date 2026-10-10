using System;
using System.ComponentModel;
using System.Globalization;
using System.Linq;
using System.Text.Json;
using System.Threading.Tasks;
using AutoCAD_MCP_Server.Services;
using ModelContextProtocol.Server;

namespace AutoCAD_MCP_Server.Tools;

/// <summary>
/// Herramientas MCP para Autodesk Civil 3D 2027: superficies, cotas de terreno y alineamientos
/// (lectura y creación). Requieren Civil 3D con el Gateway activo.
/// </summary>
[McpServerToolType]
public sealed class Civil3DTools
{
    private readonly IAutoCADGatewayClient _gatewayClient;

    /// <summary>
    /// Inicializa una nueva instancia de la clase <see cref="Civil3DTools"/>.
    /// </summary>
    /// <param name="gatewayClient">El cliente para comunicación con el Gateway.</param>
    public Civil3DTools(IAutoCADGatewayClient gatewayClient)
    {
        _gatewayClient = gatewayClient ?? throw new ArgumentNullException(nameof(gatewayClient));
    }

    private static string Num(double v) => v.ToString("R", CultureInfo.InvariantCulture);

    private static string Err(string mensaje) =>
        JsonSerializer.Serialize(new { status = "error", message = mensaje });

    /// <summary>
    /// Convierte "v1,v2[,v3];..." en filas de números. Devuelve null si el formato es inválido.
    /// </summary>
    private static double[][]? ParsePuntos(string puntos, int columnas)
    {
        var filas = puntos.Split(';', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries);
        var resultado = new double[filas.Length][];
        for (int i = 0; i < filas.Length; i++)
        {
            var partes = filas[i].Split(',', StringSplitOptions.TrimEntries);
            if (partes.Length != columnas)
            {
                return null;
            }

            resultado[i] = new double[columnas];
            for (int j = 0; j < columnas; j++)
            {
                if (!double.TryParse(partes[j], NumberStyles.Float, CultureInfo.InvariantCulture, out resultado[i][j]))
                {
                    return null;
                }
            }
        }

        return resultado;
    }

    /// <summary>Verifica si el host activo es Civil 3D y resume superficies y alineamientos.</summary>
    [McpServerTool(Name = "verificar_estado_civil3d")]
    [Description("Verifica si el dibujo activo corre sobre Civil 3D 2027 y cuenta superficies y alineamientos. En AutoCAD estándar responde civil_available=false.")]
    public async Task<string> VerificarEstadoCivil3D() => await _gatewayClient.GetContextAsync("civil/status");

    /// <summary>Lista las superficies con cota mínima y máxima.</summary>
    [McpServerTool(Name = "listar_superficies_civil3d")]
    [Description("Lista las superficies topográficas (TIN) del dibujo con nombre, tipo, cota mínima, cota máxima y número de triángulos.")]
    public async Task<string> ListarSuperficies() => await _gatewayClient.GetContextAsync("civil/surfaces");

    /// <summary>Obtiene la cota del terreno en un punto.</summary>
    /// <param name="x">Coordenada Este (X) en metros.</param>
    /// <param name="y">Coordenada Norte (Y) en metros.</param>
    /// <param name="superficie">Nombre de la superficie; si se omite se usa la primera.</param>
    [McpServerTool(Name = "consultar_elevacion_terreno")]
    [Description("Devuelve la cota Z exacta del terreno (superficie TIN de Civil 3D) en el punto (x, y). Falla si el punto está fuera de la superficie.")]
    public async Task<string> ConsultarElevacion(double x, double y, string? superficie = null) =>
        await _gatewayClient.GetContextAsync(
            $"civil/surface/elevation?x={Num(x)}&y={Num(y)}" +
            (string.IsNullOrWhiteSpace(superficie) ? string.Empty : $"&surface={Uri.EscapeDataString(superficie)}"));

    /// <summary>Lista los alineamientos con sus progresivas.</summary>
    [McpServerTool(Name = "listar_alineamientos_civil3d")]
    [Description("Lista los alineamientos horizontales con nombre, progresiva inicial/final, estacas y longitud total.")]
    public async Task<string> ListarAlineamientos() => await _gatewayClient.GetContextAsync("civil/alignments");

    /// <summary>Calcula progresiva y desfase de un punto respecto a un alineamiento.</summary>
    /// <param name="x">Coordenada Este (X) en metros.</param>
    /// <param name="y">Coordenada Norte (Y) en metros.</param>
    /// <param name="alineamiento">Nombre del alineamiento; si se omite se usa el primero.</param>
    [McpServerTool(Name = "consultar_estacion_alineamiento")]
    [Description("Calcula la progresiva (estaca) y el desfase lateral de un punto (x, y) respecto a un alineamiento de Civil 3D.")]
    public async Task<string> ConsultarEstacion(double x, double y, string? alineamiento = null) =>
        await _gatewayClient.GetContextAsync(
            $"civil/alignment/station-offset?x={Num(x)}&y={Num(y)}" +
            (string.IsNullOrWhiteSpace(alineamiento) ? string.Empty : $"&alignment={Uri.EscapeDataString(alineamiento)}"));

    /// <summary>Obtiene la coordenada (X, Y) de una progresiva y desfase.</summary>
    /// <param name="progresiva">Progresiva en metros (por ejemplo 1250.5 = 1+250.50).</param>
    /// <param name="desfase">Desfase lateral en metros (+ derecha, - izquierda).</param>
    /// <param name="alineamiento">Nombre del alineamiento; si se omite se usa el primero.</param>
    [McpServerTool(Name = "obtener_coordenada_en_estacion")]
    [Description("Devuelve la coordenada (x, y) correspondiente a una progresiva y desfase sobre un alineamiento de Civil 3D.")]
    public async Task<string> ObtenerCoordenadaEnEstacion(double progresiva, double desfase = 0, string? alineamiento = null) =>
        await _gatewayClient.GetContextAsync(
            $"civil/alignment/point-at-station?station={Num(progresiva)}&offset={Num(desfase)}" +
            (string.IsNullOrWhiteSpace(alineamiento) ? string.Empty : $"&alignment={Uri.EscapeDataString(alineamiento)}"));

    /// <summary>Crea un alineamiento horizontal desde PIs.</summary>
    /// <param name="nombre">Nombre único del alineamiento.</param>
    /// <param name="puntos">PIs como "x1,y1;x2,y2;x3,y3" (mínimo 2, en orden de progresiva).</param>
    /// <param name="radio">Radio de curva circular en metros; 0 = sin curvas.</param>
    /// <param name="capa">Capa destino (se crea si no existe); por defecto "0".</param>
    [McpServerTool(Name = "crear_alineamiento_civil3d")]
    [Description("Crea un alineamiento horizontal en Civil 3D a partir de PIs 'x1,y1;x2,y2;...' con curvas circulares tangentes de radio fijo (0 = sin curvas). Rechaza nombres duplicados y radios que no caben en el trazo.")]
    public async Task<string> CrearAlineamiento(string nombre, string puntos, double radio = 0, string? capa = null)
    {
        var pts = ParsePuntos(puntos, 2);
        if (pts == null || pts.Length < 2)
        {
            return Err("Formato de 'puntos' invalido. Use 'x1,y1;x2,y2;...' con al menos 2 PIs numericos.");
        }

        string json = JsonSerializer.Serialize(new
        {
            nombre,
            puntos = pts.Select(p => new { x = p[0], y = p[1] }),
            radio,
            capa
        });
        return await _gatewayClient.PostJsonAsync("civil/alignment/create", json);
    }

    /// <summary>Crea una superficie TIN desde puntos topográficos.</summary>
    /// <param name="nombre">Nombre único de la superficie.</param>
    /// <param name="puntos">Puntos como "x1,y1,z1;x2,y2,z2;..." (mínimo 3, no colineales).</param>
    [McpServerTool(Name = "crear_superficie_civil3d")]
    [Description("Crea una superficie TIN en Civil 3D a partir de puntos topográficos 'x1,y1,z1;x2,y2,z2;...' (mínimo 3). Rechaza nombres duplicados.")]
    public async Task<string> CrearSuperficie(string nombre, string puntos)
    {
        var pts = ParsePuntos(puntos, 3);
        if (pts == null || pts.Length < 3)
        {
            return Err("Formato de 'puntos' invalido. Use 'x1,y1,z1;x2,y2,z2;...' con al menos 3 puntos numericos.");
        }

        string json = JsonSerializer.Serialize(new
        {
            nombre,
            puntos = pts.Select(p => new { x = p[0], y = p[1], z = p[2] })
        });
        return await _gatewayClient.PostJsonAsync("civil/surface/create", json);
    }
}
