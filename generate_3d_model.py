"""
Generates 3D Wavefront OBJ and MTL models for City General Hospital
with Floor 2 stacked directly on top of Floor 1 as a realistic two-story building.
Includes real doorways, staircases, and elevator shafts.
"""

import os

def create_stacked_hospital_obj():
    obj_file = "City_General_Hospital_3D.obj"
    mtl_file = "City_General_Hospital_3D.mtl"

    materials = {
        "Wall_Exterior": (0.88, 0.89, 0.92, 1.0),
        "Wall_Interior": (0.94, 0.94, 0.95, 1.0),
        "Wall_Core": (0.35, 0.40, 0.48, 1.0),
        "Floor_Slab": (0.92, 0.93, 0.95, 1.0),
        "Floor_Lobby": (0.94, 0.94, 0.96, 1.0),
        "Floor_Emergency": (0.96, 0.55, 0.55, 1.0),
        "Floor_Maternity": (0.96, 0.65, 0.75, 1.0),
        "Floor_Surgery": (0.45, 0.78, 0.82, 1.0),
        "Floor_ICU": (0.55, 0.78, 0.90, 1.0),
        "Floor_Ward": (0.65, 0.85, 0.72, 1.0),
        "Floor_Doctor": (0.75, 0.75, 0.88, 1.0),
        "Floor_Diagnostics": (0.68, 0.84, 0.92, 1.0),
        "Floor_Facilities": (0.95, 0.82, 0.60, 1.0),
        "Floor_Admin": (0.65, 0.85, 0.80, 1.0),
        "Glass": (0.60, 0.85, 0.95, 0.4),
        "Metal_Stairs": (0.32, 0.35, 0.40, 1.0),
        "Furniture_Blue": (0.18, 0.45, 0.78, 1.0),
        "Furniture_Wood": (0.68, 0.48, 0.32, 1.0),
        "Bed_White": (0.98, 0.98, 0.98, 1.0),
        "Road_Asphalt": (0.15, 0.16, 0.18, 1.0),
        "Grass": (0.30, 0.58, 0.28, 1.0)
    }

    vertices = []
    faces = []

    def add_box(x, y, z, dx, dy, dz, mat_name):
        v_start = len(vertices) + 1
        pts = [
            (x, y, z),
            (x + dx, y, z),
            (x + dx, y + dy, z),
            (x, y + dy, z),
            (x, y, z + dz),
            (x + dx, y, z + dz),
            (x + dx, y + dy, z + dz),
            (x, y + dy, z + dz),
        ]
        vertices.extend(pts)
        quads = [
            [v_start+0, v_start+1, v_start+2, v_start+3],
            [v_start+5, v_start+4, v_start+7, v_start+6],
            [v_start+3, v_start+2, v_start+6, v_start+7],
            [v_start+4, v_start+5, v_start+1, v_start+0],
            [v_start+4, v_start+0, v_start+3, v_start+7],
            [v_start+1, v_start+5, v_start+6, v_start+2],
        ]
        for q in quads:
            faces.append((mat_name, q))

    floor1_rooms = [
        ("112", "Restroom", 0.0, 0.0, 7.0, 6.0, "Floor_Facilities"),
        ("113", "Cafeteria", 7.0, 0.0, 10.0, 6.0, "Floor_Facilities"),
        ("114", "Waiting Area", 17.0, 0.0, 6.0, 6.0, "Floor_Diagnostics"),
        ("115", "Information Desk", 23.0, 0.0, 6.0, 6.0, "Floor_Diagnostics"),
        ("116", "Administration", 29.0, 0.0, 11.0, 6.0, "Floor_Admin"),
        ("109", "General Ward", 0.0, 8.0, 11.0, 4.5, "Floor_Ward"),
        ("108", "Cardiology", 0.0, 12.5, 11.0, 4.5, "Floor_Doctor"),
        ("111", "Isolation Room", 29.0, 8.0, 11.0, 4.5, "Floor_Ward"),
        ("110", "General Ward", 29.0, 12.5, 11.0, 4.5, "Floor_Ward"),
        ("101", "Emergency Room", 0.0, 19.0, 7.0, 6.0, "Floor_Emergency"),
        ("102", "Reception", 7.0, 19.0, 6.0, 6.0, "Floor_Diagnostics"),
        ("103", "OPD Consultation", 13.0, 19.0, 6.0, 6.0, "Floor_Diagnostics"),
        ("104", "Pharmacy", 19.0, 19.0, 5.0, 6.0, "Floor_Diagnostics"),
        ("105", "Laboratory", 24.0, 19.0, 5.0, 6.0, "Floor_Diagnostics"),
        ("106", "Radiology", 29.0, 19.0, 5.5, 6.0, "Floor_Diagnostics"),
        ("107", "Ultrasound", 34.5, 19.0, 5.5, 6.0, "Floor_Diagnostics"),
    ]

    floor2_rooms = [
        ("212", "Conference Room", 0.0, 0.0, 9.0, 6.0, "Floor_Facilities"),
        ("213", "Training Room", 9.0, 0.0, 7.0, 6.0, "Floor_Facilities"),
        ("214", "Pantry", 16.0, 0.0, 6.0, 6.0, "Floor_Facilities"),
        ("215", "Restroom", 22.0, 0.0, 6.0, 6.0, "Floor_Facilities"),
        ("216", "Staff Lounge", 28.0, 0.0, 12.0, 6.0, "Floor_Facilities"),
        ("209", "Doctors' Offices", 0.0, 8.0, 11.0, 3.0, "Floor_Doctor"),
        ("208", "Doctors' Offices", 0.0, 11.0, 11.0, 3.0, "Floor_Doctor"),
        ("207", "Doctors' Offices", 0.0, 14.0, 11.0, 3.0, "Floor_Doctor"),
        ("211", "Pediatrics Ward", 29.0, 8.0, 11.0, 4.5, "Floor_Ward"),
        ("210", "Pediatrics Ward", 29.0, 12.5, 11.0, 4.5, "Floor_Ward"),
        ("201", "ICU", 0.0, 19.0, 7.0, 6.0, "Floor_ICU"),
        ("202", "ICU Support", 7.0, 19.0, 5.0, 6.0, "Floor_ICU"),
        ("203", "Operation Theatre 1", 12.0, 19.0, 7.0, 6.0, "Floor_Surgery"),
        ("204", "Operation Theatre 2", 19.0, 19.0, 7.0, 6.0, "Floor_Surgery"),
        ("205", "Sterilization", 26.0, 19.0, 6.0, 6.0, "Floor_Surgery"),
        ("206", "Maternity Ward", 32.0, 19.0, 8.0, 6.0, "Floor_Maternity"),
    ]

    floor_h = 3.6
    wall_h = 2.4
    wt = 0.2

    def build_stacked_floor(rooms, baseY, is_upper=False):
        # Floor base slab
        add_box(0.0, baseY, 0.0, 40.0, 0.25, 25.0, "Floor_Slab")

        # Room color floor tiles
        for rid, rname, rx, rz, rw, rd, rmat in rooms:
            add_box(rx + 0.1, baseY + 0.25, rz + 0.1, rw - 0.2, 0.03, rd - 0.2, rmat)

        # Exterior Perimeter Walls
        if not is_upper:
            # Main entrance gap at X: 18 to 22
            add_box(0.0, baseY + 0.25, 0.0, 18.0, wall_h, wt, "Wall_Exterior")
            add_box(22.0, baseY + 0.25, 0.0, 18.0, wall_h, wt, "Wall_Exterior")
        else:
            add_box(0.0, baseY + 0.25, 0.0, 40.0, wall_h, wt, "Wall_Exterior")
        add_box(0.0, baseY + 0.25, 25.0 - wt, 40.0, wall_h, wt, "Wall_Exterior")
        add_box(0.0, baseY + 0.25, 0.0, wt, wall_h, 25.0, "Wall_Exterior")
        add_box(40.0 - wt, baseY + 0.25, 0.0, wt, wall_h, 25.0, "Wall_Exterior")

        # Corridors
        add_box(0.0, baseY + 0.25, 6.0 - wt, 40.0, wall_h, wt, "Wall_Interior")
        add_box(0.0, baseY + 0.25, 19.0, 40.0, wall_h, wt, "Wall_Interior")

        # Left / Right wing walls
        add_box(11.0, baseY + 0.25, 8.0, wt, wall_h, 9.0, "Wall_Interior")
        add_box(29.0 - wt, baseY + 0.25, 8.0, wt, wall_h, 9.0, "Wall_Interior")

        # Room internal partitions
        for rid, rname, rx, rz, rw, rd, rmat in rooms:
            if rx > 0.1 and rx + rw < 39.9:
                add_box(rx, baseY + 0.25, rz, wt, wall_h, rd, "Wall_Interior")

    # Build Floor 1 at Y = 0
    build_stacked_floor(floor1_rooms, 0.0, is_upper=False)

    # Build Floor 2 directly on top at Y = 3.6
    build_stacked_floor(floor2_rooms, floor_h, is_upper=True)

    # Continuous Staircase from Floor 1 to Floor 2
    for s in range(18):
        sy = 0.25 + s * (floor_h / 18.0)
        sz = 8.5 + s * (5.7 / 18.0)
        add_box(13.4, sy, sz, 3.2, 0.18, 0.35, "Metal_Stairs")

    # Central Elevator core tower
    add_box(24.0, 0.0, 9.5, 3.0, floor_h * 2 + 0.5, 5.0, "Wall_Core")

    # Surrounding ground
    add_box(-10.0, -0.15, -10.0, 60.0, 0.15, 45.0, "Road_Asphalt")
    add_box(-9.0, 0.0, -9.0, 6.0, 0.05, 43.0, "Grass")
    add_box(43.0, 0.0, -9.0, 6.0, 0.05, 43.0, "Grass")

    # Write MTL
    with open(mtl_file, "w", encoding="utf-8") as f:
        f.write("# City General Hospital Materials (Stacked 2-Story)\n")
        for mat_name, (r, g, b, a) in materials.items():
            f.write(f"\nnewmtl {mat_name}\n")
            f.write(f"Kd {r:.4f} {g:.4f} {b:.4f}\n")
            f.write(f"Ka {r*0.4:.4f} {g*0.4:.4f} {b*0.4:.4f}\n")
            f.write(f"Ks 0.15 0.15 0.15\n")
            f.write(f"d {a:.2f}\n")
            f.write("illum 2\n")

    # Write OBJ
    with open(obj_file, "w", encoding="utf-8") as f:
        f.write("# City General Hospital 3D Model (Stacked 2-Story)\n")
        f.write(f"mtllib {mtl_file}\n\n")
        for v in vertices:
            f.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")
        f.write("\n")
        curr_mat = None
        for mat, face in faces:
            if mat != curr_mat:
                f.write(f"usemtl {mat}\n")
                curr_mat = mat
            f.write(f"f {' '.join(str(i) for i in face)}\n")

    print(f"Generated stacked {obj_file} and {mtl_file}")

if __name__ == "__main__":
    create_stacked_hospital_obj()
