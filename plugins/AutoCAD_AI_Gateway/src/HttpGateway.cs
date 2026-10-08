using System;
using System.IO;
using System.Net;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Text.Json;
using System.Collections.Concurrent;
using Autodesk.AutoCAD.ApplicationServices;

namespace AutoCAD_AI_Gateway
{
    public static class HttpGateway
    {
        private static HttpListener _listener;
        private static CancellationTokenSource _cts;
        
        private static EventHandler _idleHandler;
        // Cola concurrente segura para evitar perdida de datos o condiciones de carrera
        private static ConcurrentQueue<string> _commandQueue = new ConcurrentQueue<string>();

        public static void StartServer(string url)
        {
            if (_listener != null && _listener.IsListening) return;

            if (_idleHandler == null)
            {
                _idleHandler = new EventHandler(ExecuteCommandOnIdle);
            }

            _listener = new HttpListener();
            _listener.Prefixes.Add(url);
            _listener.Start();

            _cts = new CancellationTokenSource();
            Task.Run(() => ListenAsync(_cts.Token));
        }

        public static void StopServer()
        {
            if (_listener != null)
            {
                _cts?.Cancel();
                _listener.Stop();
                _listener.Close();
                _listener = null;
            }
        }

        private static async Task ListenAsync(CancellationToken token)
        {
            while (!token.IsCancellationRequested)
            {
                try
                {
                    HttpListenerContext context = await _listener.GetContextAsync();
                    ProcessRequest(context);
                }
                catch (HttpListenerException)
                {
                    break;
                }
                catch (System.Exception)
                {
                }
            }
        }

        private static void ProcessRequest(HttpListenerContext context)
        {
            HttpListenerRequest request = context.Request;
            HttpListenerResponse response = context.Response;

            response.AppendHeader("Access-Control-Allow-Origin", "*");
            response.AppendHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
            
            if (request.HttpMethod == "OPTIONS")
            {
                SendResponse(response, 200, "");
                return;
            }

            if (request.HttpMethod == "POST" && request.Url.AbsolutePath == "/execute")
            {
                using (StreamReader reader = new StreamReader(request.InputStream, request.ContentEncoding))
                {
                    string payload = reader.ReadToEnd();
                    try
                    {
                        var jsonDoc = JsonDocument.Parse(payload);
                        if (jsonDoc.RootElement.TryGetProperty("command", out JsonElement cmdElement))
                        {
                            string commandStr = cmdElement.GetString();
                            if (!string.IsNullOrEmpty(commandStr))
                            {
                                // Encolar el comando en la sala de espera segura
                                _commandQueue.Enqueue(commandStr);
                                
                                // Avisar a AutoCAD que hay trabajo pendiente
                                Autodesk.AutoCAD.ApplicationServices.Application.Idle += _idleHandler;
                                
                                SendResponse(response, 200, "{\"status\": \"success\", \"message\": \"Comando encolado correctamente\"}");
                                return;
                            }
                        }
                        SendResponse(response, 400, "{\"status\": \"error\", \"message\": \"JSON invalido. Se requiere la clave 'command'.\"}");
                    }
                    catch (System.Exception ex)
                    {
                        SendResponse(response, 400, $"{{\"status\": \"error\", \"message\": \"{ex.Message}\"}}");
                    }
                }
            }
            else
            {
                SendResponse(response, 404, "{\"status\": \"error\", \"message\": \"Ruta no encontrada. Usa POST /execute\"}");
            }
        }

        private static void ExecuteCommandOnIdle(object sender, EventArgs e)
        {
            // Desvincular de inmediato para evitar ejecucion fantasma
            Autodesk.AutoCAD.ApplicationServices.Application.Idle -= _idleHandler;
            
            Document doc = Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument;
            if (doc != null)
            {
                // Extraer todos los comandos de la cola secuencialmente
                while (_commandQueue.TryDequeue(out string cmd))
                {
                    // DIRECTIVA DE SEGURIDAD:
                    // 1. \x03\x03 al inicio para cancelar cualquier comando previo o pegado
                    // 2. Ejecutar el comando de la IA con total control (la IA decide si manda \n o no al final)
                    string safeCommand = "\x03\x03" + cmd;

                    
                    doc.SendStringToExecute(safeCommand, true, false, false);
                }
            }
        }

        private static void SendResponse(HttpListenerResponse response, int statusCode, string responseString)
        {
            byte[] buffer = Encoding.UTF8.GetBytes(responseString);
            response.StatusCode = statusCode;
            response.ContentType = "application/json";
            response.ContentLength64 = buffer.Length;
            System.IO.Stream output = response.OutputStream;
            output.Write(buffer, 0, buffer.Length);
            output.Close();
        }
    }
}
