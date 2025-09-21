import 'package:camera/camera.dart';
import 'package:flutter/foundation.dart';

class CameraService {
  CameraController? _controller;
  List<CameraDescription>? _cameras;

  /// Initialize camera service
  Future<void> initialize() async {
    try {
      _cameras = await availableCameras();
      if (_cameras!.isNotEmpty) {
        _controller = CameraController(
          _cameras!.first,
          ResolutionPreset.high,
          enableAudio: true,
        );
        await _controller!.initialize();
      }
    } catch (e) {
      debugPrint('Error initializing camera: $e');
      throw Exception('Failed to initialize camera: $e');
    }
  }

  /// Get camera controller
  CameraController? get controller => _controller;

  /// Get available cameras
  List<CameraDescription>? get cameras => _cameras;

  /// Start video recording
  Future<void> startRecording() async {
    if (_controller == null || !_controller!.value.isInitialized) {
      throw Exception('Camera not initialized');
    }

    try {
      await _controller!.startVideoRecording();
    } catch (e) {
      debugPrint('Error starting recording: $e');
      throw Exception('Failed to start recording: $e');
    }
  }

  /// Stop video recording
  Future<String> stopRecording() async {
    if (_controller == null) {
      throw Exception('Camera not initialized');
    }

    try {
      final XFile videoFile = await _controller!.stopVideoRecording();
      return videoFile.path;
    } catch (e) {
      debugPrint('Error stopping recording: $e');
      throw Exception('Failed to stop recording: $e');
    }
  }

  /// Check if camera is recording
  bool get isRecording => _controller?.value.isRecordingVideo ?? false;

  /// Dispose camera resources
  void dispose() {
    _controller?.dispose();
    _controller = null;
  }

  /// Switch camera (front/back)
  Future<void> switchCamera() async {
    if (_cameras == null || _cameras!.length < 2) {
      return;
    }

    try {
      final currentCamera = _controller?.description;
      final newCamera = _cameras!.firstWhere(
        (camera) => camera.lensDirection != currentCamera?.lensDirection,
      );

      await _controller?.dispose();
      _controller = CameraController(
        newCamera,
        ResolutionPreset.high,
        enableAudio: true,
      );
      await _controller!.initialize();
    } catch (e) {
      debugPrint('Error switching camera: $e');
    }
  }

  /// Get camera flash mode
  FlashMode get flashMode => _controller?.value.flashMode ?? FlashMode.off;

  /// Set camera flash mode
  Future<void> setFlashMode(FlashMode mode) async {
    if (_controller == null) return;

    try {
      await _controller!.setFlashMode(mode);
    } catch (e) {
      debugPrint('Error setting flash mode: $e');
    }
  }
}
