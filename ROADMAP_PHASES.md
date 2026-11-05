# Digital Twin Korea: Progressive Enhancement Roadmap (Phase 1 to 4)

To ensure systematic and structured execution, autonomous contributors should follow this strict multi-phase priority sequence.

---

## 🎯 Step-by-Step Priority Sequence

### 🟢 Phase 1: Complete Nationwide Geographic Base (Current Active Phase)
- **Objective**: Cover all 250 administrative districts with standard block packages.
- **Scope**:
  - District BBox and Center coordinates
  - 5 prominent landmarks with detailed source URLs
  - Historical and cultural overview (>=30 chars)
  - Open data license attribution
- **Action**: Fulfill `ALL_KOREA_250_TASKS.md` completely.

---

### 🟡 Phase 2: 3D Cinematic & Visual Detail Enhancement (1st Post-Base Priority)
Once Phase 1 base coverage is complete, upgrade blocks with 3D viewing attributes:
1. **`camera_view`**:
   - Optimal 3D cinematic camera view per landmark:
     ```json
     "camera_view": {
       "altitude": 150,
       "pitch": -30,
       "heading": 45
     }
     ```
2. **`image_url`**:
   - High-resolution public domain photo URL (e.g. Wikimedia Commons, KOGL Type 1).

---

### 🟠 Phase 3: Virtual 3D Tour Flight Courses (2nd Post-Base Priority)
Construct experiential travel routes connecting landmarks:
- **`tours`**:
  - Sequence of landmarks for virtual drone tours:
    ```json
    "tours": [
      {
        "tour_name": "Historic & Waterfront Half-Day Trail",
        "description": "Scenic flight connecting coastlines and key cultural spots.",
        "order": ["해운대해수욕장", "동백섬", "영화의전당"],
        "duration_hours": 3.5
      }
    ]
    ```

---

### 🟣 Phase 4: Local Living Culture & Culinary Layer (3rd Post-Base Priority)
Expand with heritage culinary and local marketplace data:
- **`dining`**:
  - 3 to 5 government-certified heritage restaurants (e.g. Baeknyeon Store, local specialty spots):
    ```json
    "dining": [
      {
        "name": "Local Heritage Bakery",
        "lat": 35.1580,
        "lng": 129.1610,
        "specialty": "Traditional Seafood Stew",
        "category": "Korean"
      }
    ]
    ```
