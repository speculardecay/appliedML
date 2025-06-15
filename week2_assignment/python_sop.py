import math
import sys
sys.path.append(r"D:\ML\ML for 3D and VFX Course\Week2\Assignment\scripts")

from a_star import AStarPathFinding

def get_maze_from_grid():
    grid = hou.pwd().parm('../../a_star/grid_path').eval()
    geo = hou.node(grid).geometry()
    
    prims = geo.prims()
    num_rows = num_columns = int(math.sqrt(len(prims)))
    
    # Initialize the matrix
    grid_matrix = []

    # Populate the matrix
    for row in range(num_rows):
        row_data = []
        for col in range(num_columns):
            prim_index = row * num_columns + col
            prim = geo.prim(prim_index)
            color = prim.attribValue("Cd")  
            row_data.append(1 if color == (1.0,1.0,1.0) else 0)  
        grid_matrix.append(row_data)
 
    return grid_matrix
    
def position_object(obj_path, row, col,cell_size=1): 
    
    main_char = hou.node(obj_path)
    world_x = col * cell_size
    world_z = row * cell_size
    
    center = main_char.parmTuple("t").eval()
    main_char.parmTuple("t").set((world_x, 0, world_z))
    
    pos = (row, col)
    return pos

def solve_maze():
    node = hou.pwd().parent()

    main_char_path = node.parm("main_char").eval()
    target_node = hou.node(main_char_path)
    if not target_node:
        print("Main character node not found.")
        return

    target_col = int(target_node.parm("tx").eval())
    target_row = int(target_node.parm("tz").eval())
    target_pos = position_object(obj_path=main_char_path, row=target_row, col=target_col)

    maze1 = get_maze_from_grid()

    # Loop through actual multiparm instances
    npc_parms = node.parm("npcs").multiParmInstances()

    for parm in npc_parms:
        npc_path = parm.eval().strip()
        if not npc_path:
            continue

        npc_node = hou.node(npc_path)
        if not npc_node:
            print(f"NPC node not found for path: {npc_path}")
            continue

        current_col = int(npc_node.parm("tx").eval())
        current_row = int(npc_node.parm("tz").eval())
        start_pos = position_object(obj_path=npc_path, row=current_row, col=current_col)

        pathfinder = AStarPathFinding(maze1, start_pos, target_pos)
        path = pathfinder.find_path()

        if path and len(path) > 1:
            print(f"{npc_path}: Moving to {path[1]}")
            npc_node.parm("tz").set(path[1][0])
            npc_node.parm("tx").set(path[1][1])
        else:
            print(f"{npc_path}: No path found")


# Get NPC original position from shared memory
def restore_npcs():
    npc_data = getattr(hou.session, "npc_data_store", [])
    if not npc_data:
        return

    for entry in npc_data:
        npc_path = entry["parm"]  # stored full path
        x = entry["x"]
        z = entry["z"]

        npc_node = hou.node(npc_path)
        if npc_node:
            try:
                npc_node.parmTuple("t").set((x, 0, z))
                print(f"Restored NPC at {npc_path}: X={x}, Z={z}")
            except Exception as e:
                print(f"Error restoring NPC at {npc_path}: {e}")
        else:
            print(f"NPC node not found at path: {npc_path}")


# If frame is 1, get NPC data from shared memory
if hou.frame() == 1:
    restore_npcs()
else:
    solve_maze()