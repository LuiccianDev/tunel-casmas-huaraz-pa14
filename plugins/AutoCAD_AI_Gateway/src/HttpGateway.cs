using System;
using System.IO;
using System.Net;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Text.Json;
using System.Collections.Concurrent;
using System.Collections.Generic;
using Autodesk.AutoCAD.ApplicationServices;
using Autodesk.AutoCAD.DatabaseServices;

namespace AutoCAD_AI_Gateway
{
    public static class HttpGateway
    {
        private static HttpListener? _listener;
        private static CancellationTokenSource? _cts;
        
        private static EventHandler? _idleHandler;
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
                    if (_listener == null) break;
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

            string path = request.Url?.AbsolutePath ?? "";

            if (request.HttpMethod == "POST" && path == "/execute")
            {
                using (StreamReader reader = new StreamReader(request.InputStream, request.ContentEncoding))
                {
                    string payload = reader.ReadToEnd();
                    try
                    {
                        var jsonDoc = JsonDocument.Parse(payload);
                        if (jsonDoc.RootElement.TryGetProperty("command", out JsonElement cmdElement))
                        {
                            string? commandStr = cmdElement.GetString();
                            if (!string.IsNullOrEmpty(commandStr))
                            {
                                // Encolar el comando en la sala de espera segura
                                _commandQueue.Enqueue(commandStr);
                                
                                // Avisar a AutoCAD que hay trabajo pendiente
                                if (_idleHandler != null)
                                {
                                    Autodesk.AutoCAD.ApplicationServices.Application.Idle += _idleHandler;
                                }
                                
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
            else if (request.HttpMethod == "GET" && path == "/context/selection")
            {
                try
                {
                    string jsonResponse = LeerSeleccionDesdeAutoCAD();
                    SendResponse(response, 200, jsonResponse);
                }
                catch (Exception ex)
                {
                    SendResponse(response, 500, $"{{\"status\": \"error\", \"message\": \"{ex.Message}\"}}");
                }
            }
            else if (request.HttpMethod == "GET" && path == "/context/entities")
            {
                try
                {
                    string jsonResponse = LeerEntidadesDesdeAutoCAD();
                    SendResponse(response, 200, jsonResponse);
                }
                catch (Exception ex)
                {
                    SendResponse(response, 500, $"{{\"status\": \"error\", \"message\": \"{ex.Message}\"}}");
                }
            }
            else if (request.HttpMethod == "GET" && path == "/context/info")
            {
                try
                {
                    string jsonResponse = LeerInfoDesdeAutoCAD();
                    SendResponse(response, 200, jsonResponse);
                }
                catch (Exception ex)
                {
                    SendResponse(response, 500, $"{{\"status\": \"error\", \"message\": \"{ex.Message}\"}}");
                }
            }
            else if (request.HttpMethod == "GET" && path == "/context/layers")
            {
                try
                {
                    string jsonResponse = LeerCapasDesdeAutoCAD();
                    SendResponse(response, 200, jsonResponse);
                }
                catch (Exception ex)
                {
                    SendResponse(response, 500, $"{{\"status\": \"error\", \"message\": \"{ex.Message}\"}}");
                }
            }
            else if (request.HttpMethod == "GET" && path == "/context/extents")
            {
                try
                {
                    string jsonResponse = LeerLimitesDesdeAutoCAD();
                    SendResponse(response, 200, jsonResponse);
                }
                catch (Exception ex)
                {
                    SendResponse(response, 500, $"{{\"status\": \"error\", \"message\": \"{ex.Message}\"}}");
                }
            }
            else if (request.HttpMethod == "GET" && path == "/context/texts")
            {
                try
                {
                    string jsonResponse = LeerTextosDesdeAutoCAD();
                    SendResponse(response, 200, jsonResponse);
                }
                catch (Exception ex)
                {
                    SendResponse(response, 500, $"{{\"status\": \"error\", \"message\": \"{ex.Message}\"}}");
                }
            }
            else if (request.HttpMethod == "GET" && path == "/context/blocks")
            {
                try
                {
                    string jsonResponse = LeerBloquesDesdeAutoCAD();
                    SendResponse(response, 200, jsonResponse);
                }
                catch (Exception ex)
                {
                    SendResponse(response, 500, $"{{\"status\": \"error\", \"message\": \"{ex.Message}\"}}");
                }
            }
            else
            {
                SendResponse(response, 404, "{\"status\": \"error\", \"message\": \"Ruta no encontrada.\"}");
            }
        }

        private static void ExecuteCommandOnIdle(object? sender, EventArgs e)
        {
            // Desvincular de inmediato para evitar ejecucion fantasma
            if (_idleHandler != null)
            {
                Autodesk.AutoCAD.ApplicationServices.Application.Idle -= _idleHandler;
            }
            
            Document doc = Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument;
            if (doc != null)
            {
                // Extraer todos los comandos de la cola secuencialmente
                while (_commandQueue.TryDequeue(out string? cmd))
                {
                    if (string.IsNullOrEmpty(cmd)) continue;

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

        private static string LeerSeleccionDesdeAutoCAD()
        {
            var tcs = new TaskCompletionSource<string>();
            EventHandler? handler = null;
            handler = (s, e) =>
            {
                if (handler != null)
                {
                    Autodesk.AutoCAD.ApplicationServices.Application.Idle -= handler;
                }
                try
                {
                    Document doc = Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument;
                    if (doc == null) 
                    { 
                        tcs.SetResult("{\"status\": \"error\", \"message\": \"No hay documento abierto\"}"); 
                        return; 
                    }

                    var editor = doc.Editor;
                    var selection = editor.SelectImplied(); 
                    
                    if (selection.Status == Autodesk.AutoCAD.EditorInput.PromptStatus.OK)
                    {
                        var ids = selection.Value.GetObjectIds();
                        tcs.SetResult($"{{\"status\": \"success\", \"cantidad_seleccionada\": {ids.Length}}}");
                    }
                    else
                    {
                        tcs.SetResult("{\"status\": \"success\", \"cantidad_seleccionada\": 0}");
                    }
                }
                catch (Exception ex)
                {
                    tcs.SetException(ex);
                }
            };

            Autodesk.AutoCAD.ApplicationServices.Application.Idle += handler;
            return tcs.Task.Result; // Bloquea hasta que Idle se dispare en el hilo principal
        }

        private static string LeerEntidadesDesdeAutoCAD()
        {
            var tcs = new TaskCompletionSource<string>();
            EventHandler? handler = null;
            handler = (s, e) =>
            {
                if (handler != null)
                {
                    Autodesk.AutoCAD.ApplicationServices.Application.Idle -= handler;
                }
                try
                {
                    Document doc = Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument;
                    if (doc == null) 
                    { 
                        tcs.SetResult("{\"status\": \"error\", \"message\": \"No hay documento abierto\"}"); 
                        return; 
                    }

                    var db = doc.Database;
                    var entityCounts = new System.Collections.Generic.Dictionary<string, int>();

                    using (var tr = doc.TransactionManager.StartTransaction())
                    {
                        var bt = (Autodesk.AutoCAD.DatabaseServices.BlockTable)tr.GetObject(db.BlockTableId, Autodesk.AutoCAD.DatabaseServices.OpenMode.ForRead);
                        var btr = (Autodesk.AutoCAD.DatabaseServices.BlockTableRecord)tr.GetObject(bt[Autodesk.AutoCAD.DatabaseServices.BlockTableRecord.ModelSpace], Autodesk.AutoCAD.DatabaseServices.OpenMode.ForRead);

                        foreach (var objId in btr)
                        {
                            var ent = (Autodesk.AutoCAD.DatabaseServices.Entity)tr.GetObject(objId, Autodesk.AutoCAD.DatabaseServices.OpenMode.ForRead);
                            string tipo = ent.GetType().Name;
                            if (entityCounts.ContainsKey(tipo))
                                entityCounts[tipo]++;
                            else
                                entityCounts[tipo] = 1;
                        }
                        tr.Commit();
                    }

                    var options = new JsonSerializerOptions { WriteIndented = true };
                    string json = JsonSerializer.Serialize(new { status = "success", data = entityCounts }, options);
                    tcs.SetResult(json);
                }
                catch (Exception ex)
                {
                    tcs.SetException(ex);
                }
            };

            Autodesk.AutoCAD.ApplicationServices.Application.Idle += handler;
            return tcs.Task.Result;
        }

        private static string LeerInfoDesdeAutoCAD()
        {
            var tcs = new TaskCompletionSource<string>();
            EventHandler? handler = null;
            handler = (s, e) =>
            {
                if (handler != null)
                {
                    Autodesk.AutoCAD.ApplicationServices.Application.Idle -= handler;
                }
                try
                {
                    Document doc = Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument;
                    if (doc == null)
                    {
                        tcs.SetResult("{\"status\": \"error\", \"message\": \"No hay documento abierto\"}");
                        return;
                    }

                    var info = new
                    {
                        nombre = doc.Name,
                        soloLectura = doc.IsReadOnly,
                        unidades = doc.Database.Insunits.ToString()
                    };
                    tcs.SetResult(JsonSerializer.Serialize(new { status = "success", data = info }));
                }
                catch (Exception ex)
                {
                    tcs.SetException(ex);
                }
            };
            Autodesk.AutoCAD.ApplicationServices.Application.Idle += handler;
            return tcs.Task.Result;
        }

        private static string LeerCapasDesdeAutoCAD()
        {
            var tcs = new TaskCompletionSource<string>();
            EventHandler? handler = null;
            handler = (s, e) =>
            {
                if (handler != null)
                {
                    Autodesk.AutoCAD.ApplicationServices.Application.Idle -= handler;
                }
                try
                {
                    Document doc = Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument;
                    if (doc == null)
                    {
                        tcs.SetResult("{\"status\": \"error\", \"message\": \"No hay documento abierto\"}");
                        return;
                    }

                    var lista = new List<object>();
                    using (var tr = doc.TransactionManager.StartTransaction())
                    {
                        var lt = (LayerTable)tr.GetObject(doc.Database.LayerTableId, OpenMode.ForRead);
                        foreach (ObjectId id in lt)
                        {
                            var ltr = (LayerTableRecord)tr.GetObject(id, OpenMode.ForRead);
                            lista.Add(new
                            {
                                nombre = ltr.Name,
                                bloqueada = ltr.IsLocked,
                                congelada = ltr.IsFrozen,
                                apagada = ltr.IsOff,
                                color = ltr.Color.ColorIndex
                            });
                        }
                        tr.Commit();
                    }
                    tcs.SetResult(JsonSerializer.Serialize(new { status = "success", data = lista }));
                }
                catch (Exception ex)
                {
                    tcs.SetException(ex);
                }
            };
            Autodesk.AutoCAD.ApplicationServices.Application.Idle += handler;
            return tcs.Task.Result;
        }

        private static string LeerLimitesDesdeAutoCAD()
        {
            var tcs = new TaskCompletionSource<string>();
            EventHandler? handler = null;
            handler = (s, e) =>
            {
                if (handler != null)
                {
                    Autodesk.AutoCAD.ApplicationServices.Application.Idle -= handler;
                }
                try
                {
                    Document doc = Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument;
                    if (doc == null)
                    {
                        tcs.SetResult("{\"status\": \"error\", \"message\": \"No hay documento abierto\"}");
                        return;
                    }

                    var extmin = doc.Database.Extmin;
                    var extmax = doc.Database.Extmax;
                    var extents = new
                    {
                        minX = extmin.X,
                        minY = extmin.Y,
                        minZ = extmin.Z,
                        maxX = extmax.X,
                        maxY = extmax.Y,
                        maxZ = extmax.Z
                    };
                    tcs.SetResult(JsonSerializer.Serialize(new { status = "success", data = extents }));
                }
                catch (Exception ex)
                {
                    tcs.SetException(ex);
                }
            };
            Autodesk.AutoCAD.ApplicationServices.Application.Idle += handler;
            return tcs.Task.Result;
        }

        private static string LeerTextosDesdeAutoCAD()
        {
            var tcs = new TaskCompletionSource<string>();
            EventHandler? handler = null;
            handler = (s, e) =>
            {
                if (handler != null)
                {
                    Autodesk.AutoCAD.ApplicationServices.Application.Idle -= handler;
                }
                try
                {
                    Document doc = Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument;
                    if (doc == null)
                    {
                        tcs.SetResult("{\"status\": \"error\", \"message\": \"No hay documento abierto\"}");
                        return;
                    }

                    var lista = new List<object>();
                    using (var tr = doc.TransactionManager.StartTransaction())
                    {
                        var bt = (BlockTable)tr.GetObject(doc.Database.BlockTableId, OpenMode.ForRead);
                        var btr = (BlockTableRecord)tr.GetObject(bt[BlockTableRecord.ModelSpace], OpenMode.ForRead);

                        foreach (ObjectId objId in btr)
                        {
                            var ent = tr.GetObject(objId, OpenMode.ForRead);
                            if (ent is DBText dbText)
                            {
                                lista.Add(new
                                {
                                    tipo = "DBText",
                                    texto = dbText.TextString,
                                    x = dbText.Position.X,
                                    y = dbText.Position.Y,
                                    capa = dbText.Layer
                                });
                            }
                            else if (ent is MText mText)
                            {
                                lista.Add(new
                                {
                                    tipo = "MText",
                                    texto = mText.Contents,
                                    x = mText.Location.X,
                                    y = mText.Location.Y,
                                    capa = mText.Layer
                                });
                            }
                        }
                        tr.Commit();
                    }
                    tcs.SetResult(JsonSerializer.Serialize(new { status = "success", data = lista }));
                }
                catch (Exception ex)
                {
                    tcs.SetException(ex);
                }
            };
            Autodesk.AutoCAD.ApplicationServices.Application.Idle += handler;
            return tcs.Task.Result;
        }

        private static string LeerBloquesDesdeAutoCAD()
        {
            var tcs = new TaskCompletionSource<string>();
            EventHandler? handler = null;
            handler = (s, e) =>
            {
                if (handler != null)
                {
                    Autodesk.AutoCAD.ApplicationServices.Application.Idle -= handler;
                }
                try
                {
                    Document doc = Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument;
                    if (doc == null)
                    {
                        tcs.SetResult("{\"status\": \"error\", \"message\": \"No hay documento abierto\"}");
                        return;
                    }

                    var lista = new List<string>();
                    using (var tr = doc.TransactionManager.StartTransaction())
                    {
                        var bt = (BlockTable)tr.GetObject(doc.Database.BlockTableId, OpenMode.ForRead);
                        foreach (ObjectId objId in bt)
                        {
                            var btr = (BlockTableRecord)tr.GetObject(objId, OpenMode.ForRead);
                            if (!btr.IsAnonymous && !btr.IsLayout)
                            {
                                lista.Add(btr.Name);
                            }
                        }
                        tr.Commit();
                    }
                    tcs.SetResult(JsonSerializer.Serialize(new { status = "success", data = lista }));
                }
                catch (Exception ex)
                {
                    tcs.SetException(ex);
                }
            };
            Autodesk.AutoCAD.ApplicationServices.Application.Idle += handler;
            return tcs.Task.Result;
        }
    }
}
