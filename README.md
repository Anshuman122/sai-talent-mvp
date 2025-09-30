# AI-Powered Mobile Platform for Democratizing Sports Talent Assessment

## Introduction & Problem Context
India possesses vast, untapped athletic talent, especially in rural and remote regions. However, systemic issues—primarily high costs, lack of infrastructure, and reliance on subjective, manual scouting—have historically prevented this talent from being discovered.

This project offers an innovative solution by transforming the low-cost smartphone into a professional-grade, standardized, and unbiased tool for athletic assessment. By harnessing **Edge AI (TinyML)** and **Computer Vision**, we decentralize the talent discovery process, ensuring that every athlete is evaluated purely on their dedication and performance, regardless of their location or financial status. This creates a genuine level playing field, which is critical for India's sporting future.

---

## Current Achievements & System Status

### Offline-First Mobile Application  
- Developed using **Flutter/Dart** for seamless, single-codebase deployment on Android and iOS.  
- The core assessment logic runs fully offline, ensuring accessibility in areas with poor or no internet connectivity.

### Edge AI Deployment  
- All AI models are successfully converted, optimized, and deployed in the **TensorFlow Lite (<50MB)** format.  
- Achieves reliable, real-time inference on common low-end smartphones.

### Comprehensive Model Suite  
- Full array of activity-specific, validated biomechanical models for standardized fitness tests.

### Robust Security  
- Multi-layered **Cheat Detection pipeline** operational, protecting data integrity against video manipulation and performance fraud.

### Scalable Backend  
- Built on secure, decoupled, and containerized microservices ready to handle massive, concurrent result loads from a nationwide user base.

---

## Technical Architecture: A Deep Dive

### I. Frontend & On-Device Processing (The Edge)

| Component | Technology | Detailed Implementation & Optimization |
|-----------|-------------|----------------------------------------|
| Mobile App | Flutter / Dart | Single codebase optimized for native performance. Offline-First architecture using local SQLite database. UI designed for low digital literacy with icons, localized tutorials, and voice prompts. |
| Video Capture | Native Camera APIs | Enforces standardized input at 30 FPS. Users select 720p (Optimized) or 1080p (Accurate) based on device. |
| Preprocessing | Optimized OpenCV | Intelligent Frame Sampling, Keyframe Selection, Gaussian Blur, Histogram Equalization to ensure data quality. |
| Pose Estimation | MediaPipe BlazePose (Fine-tuned) | Extracts 33 distinct 3D skeletal keypoints per frame. Fine-tuned MobileNetV3 CNN backbone specialized for athletic movements. |
| Data Normalization | Custom Python Logic (TFLite Runtime) | Scale and Rotation Normalization ensure results are independent of camera distance and angle. |

---

### II. Core AI Pipeline & Model Optimization

| Technique | Goal | Technical Details |
|-----------|------|-------------------|
| Model Compression | Reduce model size and memory footprint | Magnitude-based Weight Pruning removes up to 30% of weights. |
| Quantization | Increase inference speed | Full Integer Post-Training Quantization (INT8) reduces model size ~75%. |
| Knowledge Distillation | Maintain high accuracy in small footprint | Teacher-student model approach transfers knowledge to a smaller model. |
| Robustness | Counter real-world noise and adversarial attempts | Corruption Augmentation for low-quality or manipulated input. |
| Deployment Format | Maximize hardware efficiency | Models converted to .tflite and use NNAPI/CoreML for acceleration. |

---

### III. Backend & Cloud Infrastructure

| Component | Technology | Role in Talent Ecosystem |
|-----------|-------------|--------------------------|
| API Layer | Node.js + Express.js | RESTful API endpoints secured with JWT Authentication and SSL/TLS. |
| Data Ingestion | Apache Kafka | Message broker buffering massive concurrent result submissions. |
| Database | MongoDB | Flexible high-performance storage for performance reports and athlete profiles. |
| Deployment | Docker & NginX | Containerized microservices with Kubernetes orchestration and load balancing. |
| Security/Integrity | Cryptographic Hashing / Blockchain Prototype | Immutable, verifiable audit trail for official records. |

---

## 🧠 The Brain: Activity-Specific Analysis Models (The Core Innovation)

| # | Activity/Test | Model Architecture | Core Logic & Focus | Metric Calculation |
|---|---------------|--------------------|-------------------|--------------------|
| 1 | Vertical & Broad Jump (Power) | CNN-LSTM Regression | Predicts initial take-off velocity (v₀) from CoM. | Jump height (h = v₀² / 2g). |
| 2 | Sit and Reach (Flexibility) | Pose Estimation + Temporal Analysis | Tracks furthest wrist position relative to hip/ankle anchor. | Horizontal distance (cm). |
| 3 | 4x10m Shuttle Run (Agility) | Transformer-based Sequence Model | Detects valid turns and sprint phases. | Total time via frame count. |
| 4 | Sit-ups (Muscular Endurance) | CNN-LSTM Classification | Calculates torso-thigh angle thresholds for valid reps. | Count of valid/partial/invalid reps. |
| 5 | Medicine Ball Throw (Power) | Pose + Object Tracker Hybrid | Tracks kinetic chain and ball trajectory. | Estimates release velocity & angle to predict distance. |
| 6 | 30m Sprint (Linear Speed) | DeepSORT Tracking | Tracks athlete torso bounding box start to finish. | Time via frame counting. |
| 7 | Endurance Runs (Gait Analysis) | Sensor Fusion (Vision + GPS) | Combines stride length, cadence, fatigue prediction. | Stride length, cadence, fatigue score. |
| 8 | Height and Weight | Scale Calibration via Landmark Ratios | Estimates real-world height from normalized landmarks. | Height (cm), predicted Weight (kg). |
| 9 | Push-ups (Upper Body Endurance) | Temporal CNN Classification | Valid reps based on elbow angle & torso alignment. | Count and Form Score. |
| 10 | Plank Hold (Core Strength) | Anomaly Detection | Monitors hip-shoulder-knee alignment. | Total time until form break. |
| 11 | T-Test Agility (Lateral Agility) | DeepSORT + Transition Classifier | Confirms valid cone touch-down/direction changes. | Time + penalty for misses. |
| 12 | Overhead Squat Assessment (Mobility) | Regression on Key Joint Angles | Predicts Mobility Score and flags faults. | Score (0-100). |
| 13 | Single Leg Balance (Stability) | Time Series Stability Model | Analyzes micromotions of torso/ankle keypoints. | Stable time and Stability Index. |
| 14 | Power Clean/Snatch Form (Weightlifting) | HMM on Angle Input | Models kinematic phases for technique. | Technical Score and weakest phase. |
| 15 | Tennis Serve Velocity (Skill/Speed) | Object Tracking + Pose | Tracks ball exit velocity and kinetic chain. | Ball speed (km/h), Efficiency Score. |
| 16 | Bowling Action Analysis (Cricket) | Temporal Graph Neural Network | Detects illegal arm flexion and alignment. | Arm Flexion Angle and Performance Score. |
| 17 | Yo-Yo Intermittent Recovery Test | DeepSORT + Activity Recognition | Tracks acceleration, deceleration, and recovery. | Distance covered and recovery flags. |
| 18 | Vertical Power Jumps (Plyometrics) | Kinematic Symmetry Detector | Siamese Network compares left/right kinematics. | Asymmetry Index and contact time. |
| 19 | Reaction Time Test (Cognitive Speed) | Event Detection CNN | Monitors visual cue change to movement onset. | Reaction time (ms). |
| 20 | Side Plank (Lateral Core Strength) | Classification Head on Angle Variance | Monitors lateral sag angle over time. | Total time until sag exceeds threshold. |

---

## Trustworthiness & Security

| Module | Purpose | Mechanism |
|--------|---------|-----------|
| Cheat Detection Pipeline | Prevents data manipulation/fraud | Motion Consistency Analysis, Biomechanical Anomaly Detection. |
| Environmental Validation | Ensures fair and consistent conditions | Metadata checks, spatiotemporal consistency tracking. |
| Adversarial Defense | Protects models from malicious input | Corruption Augmentation for robustness. |
| Impersonation Prevention | Ensures recorded athlete is registered user | One-time Biometric Liveness Verification assigning unique athlete ID. |
| Data Privacy | Compliance with Indian regulations | Strict adherence to DPDPA. Raw video never leaves the device. |

---

## 📸 Showcase & Demo

### Flutter App Screens
Here are resized **portrait screenshots** of the mobile app interface:

<p align="center">
  <img src="./Public/Flutter/Flutter_0.jpeg" alt="Flutter Screen 0" height="500"/>
  <img src="./Public/Flutter/Flutter_1.jpeg" alt="Flutter Screen 1" height="500"/>
  <img src="./Public/Flutter/Flutter_2.jpeg" alt="Flutter Screen 2" height="500"/>
  <img src="./Public/Flutter/Flutter_3.jpeg" alt="Flutter Screen 3" height="500"/>
  <img src="./Public/Flutter/Flutter_4.jpeg" alt="Flutter Screen 4" height="500"/>
</p>

---

### Sample Output Videos
These are example video outputs generated by the AI pipeline (resized with controls):

<video src="./Public/Output/Sit-ups.mp4" width="500" controls></video>  
<video src="./Public/Output/broad-jump.mp4" width="500" controls></video>  
<video src="./Public/Output/medicine-ball.mp4" width="500" controls></video>  
<video src="./Public/Output/shuttle-run.mp4" width="500" controls></video>  

---

## Future Roadmap (Long-Term Vision)

- **Wearable Fusion:** Integrate vision data with physiological data from low-cost smart bands and GPS watches for holistic performance analysis.
- **Advanced Predictive Analytics:** Forecast injury risk, monitor burnout potential, and predict peak performance windows.
- **AI-Driven Career Guidance:** Match athletes’ profiles to suitable sports using recommendation engines.
- **National Integration:** Achieve full multilingual support and integrate as the official screening tool for the Khelo India Games.

---

## Contributing / Contact


**Team Name – Team Loud **

**Team ID – 64517**

