# simulated_eye_tracking_bot
A real-time computer vision bridge linking Python OpenCV eye and face tracking to Unity 3D via an optimized, multi-threaded UDP network pipeline.

## Key Features
* **Dual-Stage Cascade Intelligence:** Leverages nested Haar Cascades for robust, localized face and eye bounding box isolation.
* **Single Point of Transmission (SPT):** Decouples calculation logic from the network trigger to guarantee a forced, constant network frame rate.
* **Fault-Tolerant State Latching:** Implements a global variable persistence model to smoothly handle blink dropouts and tracking gaps without signal loss or system crashes.
* **Low-Latency UDP Socketing:** Streams formatted telemetry as serialized ASCII byte arrays over local loopback (`127.0.0.1:5008`).
