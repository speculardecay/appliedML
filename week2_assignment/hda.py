import hou

# Houdini Session shared memory used to store npc original position
if not hasattr(hou.session, "npc_data_store"):
    hou.session.npc_data_store = []

npc_data = hou.session.npc_data_store


# Save NPC original position into shared memory
def save_npc_position(kwargs):
    clean_npc_data(kwargs)

    node = kwargs["node"]
    parm = kwargs["parm"]
    npc_path = parm.eval().strip()
    npc_data = hou.session.npc_data_store

    if not npc_path:
        return

    multiparm_parms = node.parm("npcs").multiParmInstances()
    current_paths = [p.eval().strip() for p in multiparm_parms if p.eval().strip()]
    num_matches = current_paths.count(npc_path)

    # If object used as NPC is already in the list, clear parameter field
    if num_matches > 1:
        hou.ui.displayMessage(f"Duplicate NPC object '{npc_path}' detected. Clearing parameter.", severity=hou.severityType.Error)
        parm.set("")
        return
    
    # If object used as NPC doesn't exist, clear parameter field
    npc_node = hou.node(npc_path)
    if not npc_node:
        hou.ui.displayMessage(f"Object not found: {npc_path}. Clearing parameter.", severity=hou.severityType.Error)
        parm.set("")
        return

    # Get NPC Position
    t = npc_node.parmTuple("t").eval()
    x, z = t[0], t[2]

    # Update or append to shared memory
    for entry in npc_data:
        if entry["parm"] == npc_path:
            entry["x"] = x
            entry["z"] = z
            return

    npc_data.append({"parm": npc_path, "x": x, "z": z})

    
# Clean shared memory of NPC data not associated to any NPC
def clean_npc_data(kwargs):
    node = kwargs["node"]
    npc_data = hou.session.npc_data_store

    instance_parms = node.parm("npcs").multiParmInstances()

    # All current NPCs
    current_paths = set()
    for p in instance_parms:
        path = p.eval().strip()
        if path:
            current_paths.add(path)

    # Remove unused NPC data from shared memory
    before = len(npc_data)
    npc_data[:] = [e for e in npc_data if e["parm"] in current_paths]


# Print NPC data from shared memory
def print_npc_data():
    print("NPC Data in Memory:")
    for entry in npc_data:
        print(f"  NPC {entry['parm']}: X={entry['x']}, Z={entry['z']}")
