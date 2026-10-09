using System;
using Autodesk.AutoCAD.Runtime;
using Autodesk.AutoCAD.ApplicationServices;
using Autodesk.AutoCAD.EditorInput;
using AutoCAD_AI_Gateway.Server;

namespace AutoCAD_AI_Gateway.Commands;

/// <summary>
/// Registra y gestiona los comandos de consola de AutoCAD para controlar el ciclo de vida del AI Gateway.
/// </summary>
public sealed class GatewayCommands
{
    private const string DefaultServerUrl = "http://localhost:5055/";

    /// <summary>
    /// Comando de consola de AutoCAD 'AI_START_SERVER' que inicializa el servidor HTTP en el puerto 5055.
    /// </summary>
    [CommandMethod("AI_START_SERVER")]
    public void StartServerCommand()
    {
        Document? doc = Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument;
        if (doc == null) return;
        Editor ed = doc.Editor;

        try
        {
            if (HttpGatewayServer.Instance.IsRunning)
            {
                ed.WriteMessage($"\n>>> [AVISO] AI Gateway Server ya se encuentra en ejecucion en {DefaultServerUrl}\n");
                return;
            }

            HttpGatewayServer.Instance.Start(DefaultServerUrl);
            ed.WriteMessage($"\n>>> [ON] AI Gateway Server escuchando exitosamente en {DefaultServerUrl}\n");
        }
        catch (System.Exception ex)
        {
            ed.WriteMessage($"\n>>> [ERROR] No se pudo iniciar el servidor Gateway: {ex.Message}\n");
        }
    }

    /// <summary>
    /// Comando de consola de AutoCAD 'AI_STOP_SERVER' que apaga el servidor HTTP.
    /// </summary>
    [CommandMethod("AI_STOP_SERVER")]
    public void StopServerCommand()
    {
        Document? doc = Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument;
        if (doc == null) return;
        Editor ed = doc.Editor;

        try
        {
            HttpGatewayServer.Instance.Stop();
            ed.WriteMessage("\n>>> [OFF] AI Gateway Server detenido correctamente.\n");
        }
        catch (System.Exception ex)
        {
            ed.WriteMessage($"\n>>> [ERROR] Error al detener el servidor Gateway: {ex.Message}\n");
        }
    }
}
