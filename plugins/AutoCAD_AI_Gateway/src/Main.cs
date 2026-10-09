using System;
using Autodesk.AutoCAD.Runtime;
using Autodesk.AutoCAD.ApplicationServices;
using Autodesk.AutoCAD.EditorInput;

[assembly: ExtensionApplication(typeof(AutoCAD_AI_Gateway.Main))]
[assembly: CommandClass(typeof(AutoCAD_AI_Gateway.Commands))]

namespace AutoCAD_AI_Gateway
{
    public class Main : IExtensionApplication
    {
        public void Initialize()
        {
            Editor ed = Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument.Editor;
            ed.WriteMessage("\n=======================================================\n");
            ed.WriteMessage(">>> AutoCAD AI Gateway Plugin Cargado exitosamente.\n");
            ed.WriteMessage(">>> Escribe 'AI_START_SERVER' para iniciar el puente IA.\n");
            ed.WriteMessage("=======================================================\n");
        }

        public void Terminate()
        {
            // Apagar el servidor si AutoCAD se cierra
            HttpGateway.StopServer();
        }
    }

    public class Commands
    {
        [CommandMethod("AI_START_SERVER")]
        public void StartServerCommand()
        {
            Editor ed = Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument.Editor;
            try
            {
                HttpGateway.StartServer("http://localhost:5055/");
                ed.WriteMessage("\n>>> [ON] AI Gateway Server escuchando en http://localhost:5055/\n");
            }
            catch (System.Exception ex)
            {
                ed.WriteMessage($"\n>>> [ERROR] No se pudo iniciar el servidor: {ex.Message}\n");
            }
        }
        
        [CommandMethod("AI_STOP_SERVER")]
        public void StopServerCommand()
        {
            Editor ed = Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument.Editor;
            HttpGateway.StopServer();
            ed.WriteMessage("\n>>> [OFF] AI Gateway Server detenido.\n");
        }
    }
}
