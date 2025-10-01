# 🏅 AI-Powered Mobile Platform for Democratizing Sports Talent Assessment  
### Team Loud (ID: 64517)

---

## 📌 Introduction & Problem Context
India possesses vast, untapped athletic talent, especially in rural and remote regions. However, systemic issues—primarily high costs, lack of infrastructure, and reliance on subjective, manual scouting—have historically prevented this talent from being discovered.

This project offers an innovative solution by transforming the low-cost smartphone into a professional-grade, standardized, and unbiased tool for athletic assessment. By harnessing **Edge AI (TinyML)** and **Computer Vision**, we decentralize the talent discovery process, ensuring that every athlete is evaluated purely on their dedication and performance, regardless of their location or financial status. This creates a genuine level playing field, which is critical for India's sporting future.

---

## 🚀 Current Achievements & System Status

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

## 🏗 Technical Architecture: A Deep Dive

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

## 🧠 The Brain: Activity-Specific Analysis Models

(Full list of 20+ models for Sit-ups, Broad Jump, Shuttle Run, Medicine Ball Throw, Push-ups, Plank, etc. — all implemented with CNN-LSTM, Transformers, and Hybrid Pose+Object trackers.)

---

## 🔒 Trustworthiness & Security

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
<p align="center">
  <img src="./Public/Flutter/Flutter_0.jpeg" alt="Flutter Screen 0" height="500"/>
  <img src="./Public/Flutter/Flutter_1.jpeg" alt="Flutter Screen 1" height="500"/>
  <img src="./Public/Flutter/Flutter_2.jpeg" alt="Flutter Screen 2" height="500"/>
  <img src="./Public/Flutter/Flutter_3.jpeg" alt="Flutter Screen 3" height="500"/>
  <img src="./Public/Flutter/Flutter_4.jpeg" alt="Flutter Screen 4" height="500"/>
</p>

---

### Sample Output Videos
- [Sit-ups Video](./Public/Output/Sit-ups.mp4)  
- [Broad Jump Video](./Public/Output/broad-jump.mp4)  
- [Medicine Ball Video](./Public/Output/medicine-ball.mp4)  
- [Shuttle Run Video](./Public/Output/shuttle-run.mp4)  

---

## 🖼️ System Visuals

### AI Models Overview  
![AI Models](./Public/Team_Loud_Project_Architecture/Team_Loud_AI_Models.png)

### Cheat Detection Pipeline  
![Cheat Detection](./Public/Team_Loud_Project_Architecture/Team_Loud_Cheat_Detection.png)

### Project Architecture  
![Architecture](./Public/Team_Loud_Project_Architecture/Team_Loud_Project_Architecture.png)


---

## 🛣 Future Roadmap

- **Wearable Fusion:** Integrate vision data with physiological data from low-cost smart bands and GPS watches.  
- **Advanced Predictive Analytics:** Forecast injury risk, burnout, and performance peaks.  
- **AI-Driven Career Guidance:** Match athletes to optimal sports via recommendation engines.  
- **National Integration:** Full multilingual support + official integration with Khelo India Games.  

---

## 🤝 Contributing / Contact

**Team Name – Team Loud**  
**Team ID – 64517**  
