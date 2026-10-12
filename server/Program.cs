using System.Net.WebSockets;
using System.Text;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/health", () => Results.Ok(new { service = "digital-world-server", version = "0.2.0", status = "ok" }));
app.UseWebSockets();

app.Map("/ws", async context =>
{
    if (!context.WebSockets.IsWebSocketRequest)
    {
        context.Response.StatusCode = StatusCodes.Status400BadRequest;
        return;
    }

    // Handshake/echo for integration tests only: not an authoritative multiplayer server.
    using var socket = await context.WebSockets.AcceptWebSocketAsync();
    var buffer = new byte[4096];
    while (socket.State == WebSocketState.Open)
    {
        var result = await socket.ReceiveAsync(new ArraySegment<byte>(buffer), context.RequestAborted);
        if (result.MessageType == WebSocketMessageType.Close)
        {
            await socket.CloseAsync(WebSocketCloseStatus.NormalClosure, "bye", CancellationToken.None);
            break;
        }

        var response = Encoding.UTF8.GetBytes("{\"type\":\"ack\",\"status\":\"prototype\"}");
        await socket.SendAsync(new ArraySegment<byte>(response), WebSocketMessageType.Text, true, context.RequestAborted);
    }
});

app.Run();
