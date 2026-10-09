using System;
using System.Collections.Generic;
using System.Text.Json;
using System.Threading.Tasks;
using Autodesk.AutoCAD.ApplicationServices;
using Autodesk.AutoCAD.DatabaseServices;
using AutoCAD_AI_Gateway.Core.Models;

namespace AutoCAD_AI_Gateway.Services;

/// <summary>
/// Implementación para la lectura segura de la base de datos de AutoCAD en el hilo principal.
/// </summary>
public sealed class AutoCADContextReader : IAutoCADContextReader
{
    /// <summary>
    /// Ejecuta una función de consulta sobre el documento activo en el hilo principal mediante el evento Idle.
    /// </summary>
    /// <param name="query">La función delegada que recibe el documento activo y retorna una cadena serializada.</param>
    /// <returns>Una tarea asíncrona con el resultado devuelto por la consulta.</returns>
    private static Task<string> RunOnIdleAsync(Func<Document, string> query)
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

                string result = query(doc);
                tcs.SetResult(result);
            }
            catch (Exception ex)
            {
                tcs.SetException(ex);
            }
        };

        Autodesk.AutoCAD.ApplicationServices.Application.Idle += handler;
        return tcs.Task;
    }

    /// <inheritdoc/>
    public Task<string> ReadSelectionCountAsync()
    {
        return RunOnIdleAsync(doc =>
        {
            var editor = doc.Editor;
            var selection = editor.SelectImplied();

            int count = selection.Status == Autodesk.AutoCAD.EditorInput.PromptStatus.OK
                ? selection.Value.GetObjectIds().Length
                : 0;

            return JsonSerializer.Serialize(new { status = "success", cantidad_seleccionada = count });
        });
    }

    /// <inheritdoc/>
    public Task<string> ReadEntityCountsAsync()
    {
        return RunOnIdleAsync(doc =>
        {
            var db = doc.Database;
            var entityCounts = new Dictionary<string, int>();

            using (var tr = doc.TransactionManager.StartTransaction())
            {
                var bt = (BlockTable)tr.GetObject(db.BlockTableId, OpenMode.ForRead);
                var btr = (BlockTableRecord)tr.GetObject(bt[BlockTableRecord.ModelSpace], OpenMode.ForRead);

                foreach (var objId in btr)
                {
                    var ent = (Entity)tr.GetObject(objId, OpenMode.ForRead);
                    string tipo = ent.GetType().Name;
                    entityCounts[tipo] = entityCounts.TryGetValue(tipo, out int c) ? c + 1 : 1;
                }
                tr.Commit();
            }

            var options = new JsonSerializerOptions { WriteIndented = true };
            return JsonSerializer.Serialize(new { status = "success", data = entityCounts }, options);
        });
    }

    /// <inheritdoc/>
    public Task<string> ReadDrawingInfoAsync()
    {
        return RunOnIdleAsync(doc =>
        {
            var info = new DrawingInfo
            {
                Nombre = doc.Name,
                SoloLectura = doc.IsReadOnly,
                Unidades = doc.Database.Insunits.ToString()
            };
            return JsonSerializer.Serialize(new { status = "success", data = info });
        });
    }

    /// <inheritdoc/>
    public Task<string> ReadLayersAsync()
    {
        return RunOnIdleAsync(doc =>
        {
            var lista = new List<LayerInfo>();
            using (var tr = doc.TransactionManager.StartTransaction())
            {
                var lt = (LayerTable)tr.GetObject(doc.Database.LayerTableId, OpenMode.ForRead);
                foreach (ObjectId id in lt)
                {
                    var ltr = (LayerTableRecord)tr.GetObject(id, OpenMode.ForRead);
                    lista.Add(new LayerInfo
                    {
                        Nombre = ltr.Name,
                        Bloqueada = ltr.IsLocked,
                        Congelada = ltr.IsFrozen,
                        Apagada = ltr.IsOff,
                        Color = ltr.Color.ColorIndex
                    });
                }
                tr.Commit();
            }
            return JsonSerializer.Serialize(new { status = "success", data = lista });
        });
    }

    /// <inheritdoc/>
    public Task<string> ReadExtentsAsync()
    {
        return RunOnIdleAsync(doc =>
        {
            var extmin = doc.Database.Extmin;
            var extmax = doc.Database.Extmax;
            var extents = new DrawingExtentsInfo
            {
                MinX = extmin.X,
                MinY = extmin.Y,
                MinZ = extmin.Z,
                MaxX = extmax.X,
                MaxY = extmax.Y,
                MaxZ = extmax.Z
            };
            return JsonSerializer.Serialize(new { status = "success", data = extents });
        });
    }

    /// <inheritdoc/>
    public Task<string> ReadTextsAsync()
    {
        return RunOnIdleAsync(doc =>
        {
            var lista = new List<TextEntityInfo>();
            using (var tr = doc.TransactionManager.StartTransaction())
            {
                var bt = (BlockTable)tr.GetObject(doc.Database.BlockTableId, OpenMode.ForRead);
                var btr = (BlockTableRecord)tr.GetObject(bt[BlockTableRecord.ModelSpace], OpenMode.ForRead);

                foreach (ObjectId objId in btr)
                {
                    var ent = tr.GetObject(objId, OpenMode.ForRead);
                    if (ent is DBText dbText)
                    {
                        lista.Add(new TextEntityInfo
                        {
                            Tipo = "DBText",
                            Texto = dbText.TextString,
                            X = dbText.Position.X,
                            Y = dbText.Position.Y,
                            Capa = dbText.Layer
                        });
                    }
                    else if (ent is MText mText)
                    {
                        lista.Add(new TextEntityInfo
                        {
                            Tipo = "MText",
                            Texto = mText.Contents,
                            X = mText.Location.X,
                            Y = mText.Location.Y,
                            Capa = mText.Layer
                        });
                    }
                }
                tr.Commit();
            }
            return JsonSerializer.Serialize(new { status = "success", data = lista });
        });
    }

    /// <inheritdoc/>
    public Task<string> ReadBlocksAsync()
    {
        return RunOnIdleAsync(doc =>
        {
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
            return JsonSerializer.Serialize(new { status = "success", data = lista });
        });
    }
}
