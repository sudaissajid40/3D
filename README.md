# City General Hospital - 3D Walkthrough Game & Interactive Explorer

This project features a **two-story stacked 3D Hospital** with a **playable Doctor character** that can walk inside and explore every room just like in a video game!

---

## 🎮 How to Play / Explore

Open **[`index.html`](file:///c:/Users/dell/Desktop/3D/index.html)** in any web browser (Chrome, Edge, Firefox).

### Game Controls:
| Action | Key / Input |
|---|---|
| **Move Forward / Backward** | <kbd>W</kbd> / <kbd>S</kbd> or <kbd>↑</kbd> / <kbd>↓</kbd> |
| **Strafe Left / Right** | <kbd>A</kbd> / <kbd>D</kbd> or <kbd>←</kbd> / <kbd>→</kbd> |
| **Sprint / Run** | Hold <kbd>Shift</kbd> |
| **Look Around** | Click + Drag Mouse across the screen |
| **Toggle 1st / 3rd Person View** | <kbd>V</kbd> (switch between seeing your doctor or seeing through doctor's eyes) |
| **Interact / Elevator** | <kbd>E</kbd> (when near the elevator core) |
| **On-Screen D-Pad** | On-screen arrow buttons for touch screen or mouse clicks |

---

## 🏢 Two Stacked Floors & Vertical Travel

1. **Floor Stacking**:
   - **Floor 1 (Ground Floor)** sits at ground level ($Y = 0\text{ m}$).
   - **Floor 2 (Second Floor)** sits directly on top at $Y = 3.6\text{ m}$.
2. **Climbing the Stairs**:
   - Walk into the central stairwell at $X: 13.0 - 17.0\text{ m}, Z: 8.5 - 14.2\text{ m}$.
   - As you walk forward up the steps, your character smoothly climbs from Floor 1 to Floor 2! Walking down returns you to Floor 1.
3. **Taking the Elevator**:
   - Step into the glass elevator cabin located in the central lobby ($X: 25.5\text{ m}, Z: 12.0\text{ m}$).
   - Press <kbd>E</kbd> or click the interaction prompt to open the Elevator Control Panel.
   - Choose **Floor 1** or **Floor 2** to experience a smooth elevator ride with authentic chime sounds and sliding doors!

---

## 📍 Live GPS Minimap & Location HUD

- **Top Banner**: Real-time room tracker (e.g. `📍 FLOOR 1 • Emergency Room (101)`). When entering any room, a chime rings and the room's clinical equipment details drawer appears!
- **Top-Right Radar Minimap**: Displays a 2D floor blueprint of the current level, with a blue blip and vision cone tracking your character's position and orientation.
- **Audio Synthesizer**: Procedural footstep sounds, elevator chimes, and room arrival alerts (toggleable via the Sound button).

---

## 🌐 Orbit Overview Mode
Want to see the entire building from outside?
- Click the **"🌐 Orbit Overview Mode"** button to switch instantly between game character walkthrough and free-flying 3D orbit controls!
- Toggle cutaways and full ceilings on and off.
