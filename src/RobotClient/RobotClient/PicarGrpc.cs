// <auto-generated>
//     Generated by the protocol buffer compiler.  DO NOT EDIT!
//     source: picar.proto
// </auto-generated>
#pragma warning disable 0414, 1591
#region Designer generated code

using grpc = global::Grpc.Core;

namespace RobotClient {
  /// <summary>
  ///Interface exported by the server
  /// </summary>
  public static partial class PiCar
  {
    static readonly string __ServiceName = "CapstoneRobot.PiCar";

    static readonly grpc::Marshaller<global::RobotClient.ConnectRequest> __Marshaller_CapstoneRobot_ConnectRequest = grpc::Marshallers.Create((arg) => global::Google.Protobuf.MessageExtensions.ToByteArray(arg), global::RobotClient.ConnectRequest.Parser.ParseFrom);
    static readonly grpc::Marshaller<global::RobotClient.ConnectAck> __Marshaller_CapstoneRobot_ConnectAck = grpc::Marshallers.Create((arg) => global::Google.Protobuf.MessageExtensions.ToByteArray(arg), global::RobotClient.ConnectAck.Parser.ParseFrom);
    static readonly grpc::Marshaller<global::RobotClient.ModeRequest> __Marshaller_CapstoneRobot_ModeRequest = grpc::Marshallers.Create((arg) => global::Google.Protobuf.MessageExtensions.ToByteArray(arg), global::RobotClient.ModeRequest.Parser.ParseFrom);
    static readonly grpc::Marshaller<global::RobotClient.ModeAck> __Marshaller_CapstoneRobot_ModeAck = grpc::Marshallers.Create((arg) => global::Google.Protobuf.MessageExtensions.ToByteArray(arg), global::RobotClient.ModeAck.Parser.ParseFrom);
    static readonly grpc::Marshaller<global::RobotClient.SetMotion> __Marshaller_CapstoneRobot_SetMotion = grpc::Marshallers.Create((arg) => global::Google.Protobuf.MessageExtensions.ToByteArray(arg), global::RobotClient.SetMotion.Parser.ParseFrom);
    static readonly grpc::Marshaller<global::RobotClient.Empty> __Marshaller_CapstoneRobot_Empty = grpc::Marshallers.Create((arg) => global::Google.Protobuf.MessageExtensions.ToByteArray(arg), global::RobotClient.Empty.Parser.ParseFrom);
    static readonly grpc::Marshaller<global::RobotClient.StartStreaming> __Marshaller_CapstoneRobot_StartStreaming = grpc::Marshallers.Create((arg) => global::Google.Protobuf.MessageExtensions.ToByteArray(arg), global::RobotClient.StartStreaming.Parser.ParseFrom);
    static readonly grpc::Marshaller<global::RobotClient.StreamData> __Marshaller_CapstoneRobot_StreamData = grpc::Marshallers.Create((arg) => global::Google.Protobuf.MessageExtensions.ToByteArray(arg), global::RobotClient.StreamData.Parser.ParseFrom);
    static readonly grpc::Marshaller<global::RobotClient.StopStreaming> __Marshaller_CapstoneRobot_StopStreaming = grpc::Marshallers.Create((arg) => global::Google.Protobuf.MessageExtensions.ToByteArray(arg), global::RobotClient.StopStreaming.Parser.ParseFrom);
    static readonly grpc::Marshaller<global::RobotClient.ModelVersion> __Marshaller_CapstoneRobot_ModelVersion = grpc::Marshallers.Create((arg) => global::Google.Protobuf.MessageExtensions.ToByteArray(arg), global::RobotClient.ModelVersion.Parser.ParseFrom);
    static readonly grpc::Marshaller<global::RobotClient.SwitchModelAck> __Marshaller_CapstoneRobot_SwitchModelAck = grpc::Marshallers.Create((arg) => global::Google.Protobuf.MessageExtensions.ToByteArray(arg), global::RobotClient.SwitchModelAck.Parser.ParseFrom);

    static readonly grpc::Method<global::RobotClient.ConnectRequest, global::RobotClient.ConnectAck> __Method_ReceiveConnection = new grpc::Method<global::RobotClient.ConnectRequest, global::RobotClient.ConnectAck>(
        grpc::MethodType.Unary,
        __ServiceName,
        "ReceiveConnection",
        __Marshaller_CapstoneRobot_ConnectRequest,
        __Marshaller_CapstoneRobot_ConnectAck);

    static readonly grpc::Method<global::RobotClient.ModeRequest, global::RobotClient.ModeAck> __Method_SwitchMode = new grpc::Method<global::RobotClient.ModeRequest, global::RobotClient.ModeAck>(
        grpc::MethodType.Unary,
        __ServiceName,
        "SwitchMode",
        __Marshaller_CapstoneRobot_ModeRequest,
        __Marshaller_CapstoneRobot_ModeAck);

    static readonly grpc::Method<global::RobotClient.SetMotion, global::RobotClient.Empty> __Method_RemoteControl = new grpc::Method<global::RobotClient.SetMotion, global::RobotClient.Empty>(
        grpc::MethodType.ClientStreaming,
        __ServiceName,
        "RemoteControl",
        __Marshaller_CapstoneRobot_SetMotion,
        __Marshaller_CapstoneRobot_Empty);

    static readonly grpc::Method<global::RobotClient.StartStreaming, global::RobotClient.StreamData> __Method_StartStream = new grpc::Method<global::RobotClient.StartStreaming, global::RobotClient.StreamData>(
        grpc::MethodType.ServerStreaming,
        __ServiceName,
        "StartStream",
        __Marshaller_CapstoneRobot_StartStreaming,
        __Marshaller_CapstoneRobot_StreamData);

    static readonly grpc::Method<global::RobotClient.StopStreaming, global::RobotClient.Empty> __Method_StopStream = new grpc::Method<global::RobotClient.StopStreaming, global::RobotClient.Empty>(
        grpc::MethodType.Unary,
        __ServiceName,
        "StopStream",
        __Marshaller_CapstoneRobot_StopStreaming,
        __Marshaller_CapstoneRobot_Empty);

    static readonly grpc::Method<global::RobotClient.ModelVersion, global::RobotClient.SwitchModelAck> __Method_SwitchFollowerModel = new grpc::Method<global::RobotClient.ModelVersion, global::RobotClient.SwitchModelAck>(
        grpc::MethodType.Unary,
        __ServiceName,
        "SwitchFollowerModel",
        __Marshaller_CapstoneRobot_ModelVersion,
        __Marshaller_CapstoneRobot_SwitchModelAck);

    /// <summary>Service descriptor</summary>
    public static global::Google.Protobuf.Reflection.ServiceDescriptor Descriptor
    {
      get { return global::RobotClient.PicarReflection.Descriptor.Services[0]; }
    }

    /// <summary>Base class for server-side implementations of PiCar</summary>
    public abstract partial class PiCarBase
    {
      /// <summary>
      /// Handshake between PiCar and desktop application.
      /// All clients starting from the initial version expect this. Do not change.
      /// </summary>
      /// <param name="request">The request received from the client.</param>
      /// <param name="context">The context of the server-side call handler being invoked.</param>
      /// <returns>The response to send back to the client (wrapped by a task).</returns>
      public virtual global::System.Threading.Tasks.Task<global::RobotClient.ConnectAck> ReceiveConnection(global::RobotClient.ConnectRequest request, grpc::ServerCallContext context)
      {
        throw new grpc::RpcException(new grpc::Status(grpc::StatusCode.Unimplemented, ""));
      }

      /// <summary>
      ///Changes the operating mode of the PiCar
      /// </summary>
      /// <param name="request">The request received from the client.</param>
      /// <param name="context">The context of the server-side call handler being invoked.</param>
      /// <returns>The response to send back to the client (wrapped by a task).</returns>
      public virtual global::System.Threading.Tasks.Task<global::RobotClient.ModeAck> SwitchMode(global::RobotClient.ModeRequest request, grpc::ServerCallContext context)
      {
        throw new grpc::RpcException(new grpc::Status(grpc::StatusCode.Unimplemented, ""));
      }

      /// <summary>
      ///Receive control data from desktop application
      /// </summary>
      /// <param name="requestStream">Used for reading requests from the client.</param>
      /// <param name="context">The context of the server-side call handler being invoked.</param>
      /// <returns>The response to send back to the client (wrapped by a task).</returns>
      public virtual global::System.Threading.Tasks.Task<global::RobotClient.Empty> RemoteControl(grpc::IAsyncStreamReader<global::RobotClient.SetMotion> requestStream, grpc::ServerCallContext context)
      {
        throw new grpc::RpcException(new grpc::Status(grpc::StatusCode.Unimplemented, ""));
      }

      /// <summary>
      ///Begin video/action streaming
      /// </summary>
      /// <param name="request">The request received from the client.</param>
      /// <param name="responseStream">Used for sending responses back to the client.</param>
      /// <param name="context">The context of the server-side call handler being invoked.</param>
      /// <returns>A task indicating completion of the handler.</returns>
      public virtual global::System.Threading.Tasks.Task StartStream(global::RobotClient.StartStreaming request, grpc::IServerStreamWriter<global::RobotClient.StreamData> responseStream, grpc::ServerCallContext context)
      {
        throw new grpc::RpcException(new grpc::Status(grpc::StatusCode.Unimplemented, ""));
      }

      /// <summary>
      ///End video/action streaming
      /// </summary>
      /// <param name="request">The request received from the client.</param>
      /// <param name="context">The context of the server-side call handler being invoked.</param>
      /// <returns>The response to send back to the client (wrapped by a task).</returns>
      public virtual global::System.Threading.Tasks.Task<global::RobotClient.Empty> StopStream(global::RobotClient.StopStreaming request, grpc::ServerCallContext context)
      {
        throw new grpc::RpcException(new grpc::Status(grpc::StatusCode.Unimplemented, ""));
      }

      /// <summary>
      /// Switch model
      /// </summary>
      /// <param name="request">The request received from the client.</param>
      /// <param name="context">The context of the server-side call handler being invoked.</param>
      /// <returns>The response to send back to the client (wrapped by a task).</returns>
      public virtual global::System.Threading.Tasks.Task<global::RobotClient.SwitchModelAck> SwitchFollowerModel(global::RobotClient.ModelVersion request, grpc::ServerCallContext context)
      {
        throw new grpc::RpcException(new grpc::Status(grpc::StatusCode.Unimplemented, ""));
      }

    }

    /// <summary>Client for PiCar</summary>
    public partial class PiCarClient : grpc::ClientBase<PiCarClient>
    {
      /// <summary>Creates a new client for PiCar</summary>
      /// <param name="channel">The channel to use to make remote calls.</param>
      public PiCarClient(grpc::Channel channel) : base(channel)
      {
      }
      /// <summary>Creates a new client for PiCar that uses a custom <c>CallInvoker</c>.</summary>
      /// <param name="callInvoker">The callInvoker to use to make remote calls.</param>
      public PiCarClient(grpc::CallInvoker callInvoker) : base(callInvoker)
      {
      }
      /// <summary>Protected parameterless constructor to allow creation of test doubles.</summary>
      protected PiCarClient() : base()
      {
      }
      /// <summary>Protected constructor to allow creation of configured clients.</summary>
      /// <param name="configuration">The client configuration.</param>
      protected PiCarClient(ClientBaseConfiguration configuration) : base(configuration)
      {
      }

      /// <summary>
      /// Handshake between PiCar and desktop application.
      /// All clients starting from the initial version expect this. Do not change.
      /// </summary>
      /// <param name="request">The request to send to the server.</param>
      /// <param name="headers">The initial metadata to send with the call. This parameter is optional.</param>
      /// <param name="deadline">An optional deadline for the call. The call will be cancelled if deadline is hit.</param>
      /// <param name="cancellationToken">An optional token for canceling the call.</param>
      /// <returns>The response received from the server.</returns>
      public virtual global::RobotClient.ConnectAck ReceiveConnection(global::RobotClient.ConnectRequest request, grpc::Metadata headers = null, global::System.DateTime? deadline = null, global::System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
      {
        return ReceiveConnection(request, new grpc::CallOptions(headers, deadline, cancellationToken));
      }
      /// <summary>
      /// Handshake between PiCar and desktop application.
      /// All clients starting from the initial version expect this. Do not change.
      /// </summary>
      /// <param name="request">The request to send to the server.</param>
      /// <param name="options">The options for the call.</param>
      /// <returns>The response received from the server.</returns>
      public virtual global::RobotClient.ConnectAck ReceiveConnection(global::RobotClient.ConnectRequest request, grpc::CallOptions options)
      {
        return CallInvoker.BlockingUnaryCall(__Method_ReceiveConnection, null, options, request);
      }
      /// <summary>
      /// Handshake between PiCar and desktop application.
      /// All clients starting from the initial version expect this. Do not change.
      /// </summary>
      /// <param name="request">The request to send to the server.</param>
      /// <param name="headers">The initial metadata to send with the call. This parameter is optional.</param>
      /// <param name="deadline">An optional deadline for the call. The call will be cancelled if deadline is hit.</param>
      /// <param name="cancellationToken">An optional token for canceling the call.</param>
      /// <returns>The call object.</returns>
      public virtual grpc::AsyncUnaryCall<global::RobotClient.ConnectAck> ReceiveConnectionAsync(global::RobotClient.ConnectRequest request, grpc::Metadata headers = null, global::System.DateTime? deadline = null, global::System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
      {
        return ReceiveConnectionAsync(request, new grpc::CallOptions(headers, deadline, cancellationToken));
      }
      /// <summary>
      /// Handshake between PiCar and desktop application.
      /// All clients starting from the initial version expect this. Do not change.
      /// </summary>
      /// <param name="request">The request to send to the server.</param>
      /// <param name="options">The options for the call.</param>
      /// <returns>The call object.</returns>
      public virtual grpc::AsyncUnaryCall<global::RobotClient.ConnectAck> ReceiveConnectionAsync(global::RobotClient.ConnectRequest request, grpc::CallOptions options)
      {
        return CallInvoker.AsyncUnaryCall(__Method_ReceiveConnection, null, options, request);
      }
      /// <summary>
      ///Changes the operating mode of the PiCar
      /// </summary>
      /// <param name="request">The request to send to the server.</param>
      /// <param name="headers">The initial metadata to send with the call. This parameter is optional.</param>
      /// <param name="deadline">An optional deadline for the call. The call will be cancelled if deadline is hit.</param>
      /// <param name="cancellationToken">An optional token for canceling the call.</param>
      /// <returns>The response received from the server.</returns>
      public virtual global::RobotClient.ModeAck SwitchMode(global::RobotClient.ModeRequest request, grpc::Metadata headers = null, global::System.DateTime? deadline = null, global::System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
      {
        return SwitchMode(request, new grpc::CallOptions(headers, deadline, cancellationToken));
      }
      /// <summary>
      ///Changes the operating mode of the PiCar
      /// </summary>
      /// <param name="request">The request to send to the server.</param>
      /// <param name="options">The options for the call.</param>
      /// <returns>The response received from the server.</returns>
      public virtual global::RobotClient.ModeAck SwitchMode(global::RobotClient.ModeRequest request, grpc::CallOptions options)
      {
        return CallInvoker.BlockingUnaryCall(__Method_SwitchMode, null, options, request);
      }
      /// <summary>
      ///Changes the operating mode of the PiCar
      /// </summary>
      /// <param name="request">The request to send to the server.</param>
      /// <param name="headers">The initial metadata to send with the call. This parameter is optional.</param>
      /// <param name="deadline">An optional deadline for the call. The call will be cancelled if deadline is hit.</param>
      /// <param name="cancellationToken">An optional token for canceling the call.</param>
      /// <returns>The call object.</returns>
      public virtual grpc::AsyncUnaryCall<global::RobotClient.ModeAck> SwitchModeAsync(global::RobotClient.ModeRequest request, grpc::Metadata headers = null, global::System.DateTime? deadline = null, global::System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
      {
        return SwitchModeAsync(request, new grpc::CallOptions(headers, deadline, cancellationToken));
      }
      /// <summary>
      ///Changes the operating mode of the PiCar
      /// </summary>
      /// <param name="request">The request to send to the server.</param>
      /// <param name="options">The options for the call.</param>
      /// <returns>The call object.</returns>
      public virtual grpc::AsyncUnaryCall<global::RobotClient.ModeAck> SwitchModeAsync(global::RobotClient.ModeRequest request, grpc::CallOptions options)
      {
        return CallInvoker.AsyncUnaryCall(__Method_SwitchMode, null, options, request);
      }
      /// <summary>
      ///Receive control data from desktop application
      /// </summary>
      /// <param name="headers">The initial metadata to send with the call. This parameter is optional.</param>
      /// <param name="deadline">An optional deadline for the call. The call will be cancelled if deadline is hit.</param>
      /// <param name="cancellationToken">An optional token for canceling the call.</param>
      /// <returns>The call object.</returns>
      public virtual grpc::AsyncClientStreamingCall<global::RobotClient.SetMotion, global::RobotClient.Empty> RemoteControl(grpc::Metadata headers = null, global::System.DateTime? deadline = null, global::System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
      {
        return RemoteControl(new grpc::CallOptions(headers, deadline, cancellationToken));
      }
      /// <summary>
      ///Receive control data from desktop application
      /// </summary>
      /// <param name="options">The options for the call.</param>
      /// <returns>The call object.</returns>
      public virtual grpc::AsyncClientStreamingCall<global::RobotClient.SetMotion, global::RobotClient.Empty> RemoteControl(grpc::CallOptions options)
      {
        return CallInvoker.AsyncClientStreamingCall(__Method_RemoteControl, null, options);
      }
      /// <summary>
      ///Begin video/action streaming
      /// </summary>
      /// <param name="request">The request to send to the server.</param>
      /// <param name="headers">The initial metadata to send with the call. This parameter is optional.</param>
      /// <param name="deadline">An optional deadline for the call. The call will be cancelled if deadline is hit.</param>
      /// <param name="cancellationToken">An optional token for canceling the call.</param>
      /// <returns>The call object.</returns>
      public virtual grpc::AsyncServerStreamingCall<global::RobotClient.StreamData> StartStream(global::RobotClient.StartStreaming request, grpc::Metadata headers = null, global::System.DateTime? deadline = null, global::System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
      {
        return StartStream(request, new grpc::CallOptions(headers, deadline, cancellationToken));
      }
      /// <summary>
      ///Begin video/action streaming
      /// </summary>
      /// <param name="request">The request to send to the server.</param>
      /// <param name="options">The options for the call.</param>
      /// <returns>The call object.</returns>
      public virtual grpc::AsyncServerStreamingCall<global::RobotClient.StreamData> StartStream(global::RobotClient.StartStreaming request, grpc::CallOptions options)
      {
        return CallInvoker.AsyncServerStreamingCall(__Method_StartStream, null, options, request);
      }
      /// <summary>
      ///End video/action streaming
      /// </summary>
      /// <param name="request">The request to send to the server.</param>
      /// <param name="headers">The initial metadata to send with the call. This parameter is optional.</param>
      /// <param name="deadline">An optional deadline for the call. The call will be cancelled if deadline is hit.</param>
      /// <param name="cancellationToken">An optional token for canceling the call.</param>
      /// <returns>The response received from the server.</returns>
      public virtual global::RobotClient.Empty StopStream(global::RobotClient.StopStreaming request, grpc::Metadata headers = null, global::System.DateTime? deadline = null, global::System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
      {
        return StopStream(request, new grpc::CallOptions(headers, deadline, cancellationToken));
      }
      /// <summary>
      ///End video/action streaming
      /// </summary>
      /// <param name="request">The request to send to the server.</param>
      /// <param name="options">The options for the call.</param>
      /// <returns>The response received from the server.</returns>
      public virtual global::RobotClient.Empty StopStream(global::RobotClient.StopStreaming request, grpc::CallOptions options)
      {
        return CallInvoker.BlockingUnaryCall(__Method_StopStream, null, options, request);
      }
      /// <summary>
      ///End video/action streaming
      /// </summary>
      /// <param name="request">The request to send to the server.</param>
      /// <param name="headers">The initial metadata to send with the call. This parameter is optional.</param>
      /// <param name="deadline">An optional deadline for the call. The call will be cancelled if deadline is hit.</param>
      /// <param name="cancellationToken">An optional token for canceling the call.</param>
      /// <returns>The call object.</returns>
      public virtual grpc::AsyncUnaryCall<global::RobotClient.Empty> StopStreamAsync(global::RobotClient.StopStreaming request, grpc::Metadata headers = null, global::System.DateTime? deadline = null, global::System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
      {
        return StopStreamAsync(request, new grpc::CallOptions(headers, deadline, cancellationToken));
      }
      /// <summary>
      ///End video/action streaming
      /// </summary>
      /// <param name="request">The request to send to the server.</param>
      /// <param name="options">The options for the call.</param>
      /// <returns>The call object.</returns>
      public virtual grpc::AsyncUnaryCall<global::RobotClient.Empty> StopStreamAsync(global::RobotClient.StopStreaming request, grpc::CallOptions options)
      {
        return CallInvoker.AsyncUnaryCall(__Method_StopStream, null, options, request);
      }
      /// <summary>
      /// Switch model
      /// </summary>
      /// <param name="request">The request to send to the server.</param>
      /// <param name="headers">The initial metadata to send with the call. This parameter is optional.</param>
      /// <param name="deadline">An optional deadline for the call. The call will be cancelled if deadline is hit.</param>
      /// <param name="cancellationToken">An optional token for canceling the call.</param>
      /// <returns>The response received from the server.</returns>
      public virtual global::RobotClient.SwitchModelAck SwitchFollowerModel(global::RobotClient.ModelVersion request, grpc::Metadata headers = null, global::System.DateTime? deadline = null, global::System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
      {
        return SwitchFollowerModel(request, new grpc::CallOptions(headers, deadline, cancellationToken));
      }
      /// <summary>
      /// Switch model
      /// </summary>
      /// <param name="request">The request to send to the server.</param>
      /// <param name="options">The options for the call.</param>
      /// <returns>The response received from the server.</returns>
      public virtual global::RobotClient.SwitchModelAck SwitchFollowerModel(global::RobotClient.ModelVersion request, grpc::CallOptions options)
      {
        return CallInvoker.BlockingUnaryCall(__Method_SwitchFollowerModel, null, options, request);
      }
      /// <summary>
      /// Switch model
      /// </summary>
      /// <param name="request">The request to send to the server.</param>
      /// <param name="headers">The initial metadata to send with the call. This parameter is optional.</param>
      /// <param name="deadline">An optional deadline for the call. The call will be cancelled if deadline is hit.</param>
      /// <param name="cancellationToken">An optional token for canceling the call.</param>
      /// <returns>The call object.</returns>
      public virtual grpc::AsyncUnaryCall<global::RobotClient.SwitchModelAck> SwitchFollowerModelAsync(global::RobotClient.ModelVersion request, grpc::Metadata headers = null, global::System.DateTime? deadline = null, global::System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
      {
        return SwitchFollowerModelAsync(request, new grpc::CallOptions(headers, deadline, cancellationToken));
      }
      /// <summary>
      /// Switch model
      /// </summary>
      /// <param name="request">The request to send to the server.</param>
      /// <param name="options">The options for the call.</param>
      /// <returns>The call object.</returns>
      public virtual grpc::AsyncUnaryCall<global::RobotClient.SwitchModelAck> SwitchFollowerModelAsync(global::RobotClient.ModelVersion request, grpc::CallOptions options)
      {
        return CallInvoker.AsyncUnaryCall(__Method_SwitchFollowerModel, null, options, request);
      }
      /// <summary>Creates a new instance of client from given <c>ClientBaseConfiguration</c>.</summary>
      protected override PiCarClient NewInstance(ClientBaseConfiguration configuration)
      {
        return new PiCarClient(configuration);
      }
    }

    /// <summary>Creates service definition that can be registered with a server</summary>
    /// <param name="serviceImpl">An object implementing the server-side handling logic.</param>
    public static grpc::ServerServiceDefinition BindService(PiCarBase serviceImpl)
    {
      return grpc::ServerServiceDefinition.CreateBuilder()
          .AddMethod(__Method_ReceiveConnection, serviceImpl.ReceiveConnection)
          .AddMethod(__Method_SwitchMode, serviceImpl.SwitchMode)
          .AddMethod(__Method_RemoteControl, serviceImpl.RemoteControl)
          .AddMethod(__Method_StartStream, serviceImpl.StartStream)
          .AddMethod(__Method_StopStream, serviceImpl.StopStream)
          .AddMethod(__Method_SwitchFollowerModel, serviceImpl.SwitchFollowerModel).Build();
    }

  }
}
#endregion
