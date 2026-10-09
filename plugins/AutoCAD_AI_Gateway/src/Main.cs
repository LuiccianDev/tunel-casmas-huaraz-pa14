using Autodesk.AutoCAD.Runtime;
using Autodesk.AutoCAD.ApplicationServices;
using Autodesk.AutoCAD.EditorInput;
using AutoCAD_AI_Gateway.Server;

[assembly: ExtensionApplication(typeof(AutoCAD_AI_Gateway.Main))]
[assembly: CommandClass(typeof(AutoCAD_AI_Gateway.Commands.GatewayCommands))]

namespace AutoCAD_AI_Gateway;

/// <summary>
/// Gestiona el ciclo de vida del ensamblado de extensión de AutoCAD (inicialización y terminación).
/// </summary>
public sealed class Main : IExtensionApplication
{
    /// <inheritdoc/>
    public void Initialize()
    {
        Document? doc = Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument;
        if (doc != null)
        {
            Editor ed = doc.Editor;
            ed.WriteMessage("\n=======================================================\n");
            ed.WriteMessage(">>> AutoCAD AI Gateway Plugin Cargado exitosamente.\n");
            ed.WriteMessage(">>> Escribe 'AI_START_SERVER' para iniciar el puente IA.\n");
            ed.WriteMessage("=======================================================\n");
        }
    }

    /// <inheritdoc/>
    public void Terminate()
    {
        // Garantizar que el servidor HTTP se detenga ordenadamente al cerrar AutoCAD
        HttpGatewayServer.Instance.Stop();
    }
}
