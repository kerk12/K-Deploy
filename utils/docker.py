import os
import re

def split_image(image_raw):
    raw_split = image_raw.split(":")  # TODO Escape only the second occurence of the :. Some guys use registries on different ports.
    tag = None
    img_name = raw_split[0]
    try:
        tag = raw_split[1]
    except IndexError:
        pass

    return img_name, tag

def parse_volumes(volumes):
    """
    Parse volume definitions from argparse.
    """
    v_out = {}
    for v in volumes:
        v_split = v.split(":")
        host_side = v_split[0].strip()

        if not os.path.isdir(host_side):
            raise FileNotFoundError("Error: Directory {} on the host side doesn't exist.".format(host_side))

        c_side = v_split[1].strip()
        mode = "rw"
        try:
            mode = v_split[2].strip()
            if mode not in ["rw", "ro"]:
                raise ValueError("Volume mode incorrect. Accepted values: rw, ro")
        except IndexError:
            pass

        v_out[host_side] = {"bind": c_side, "mode": mode}
    return v_out

def parse_ports(ports):
    """
    Parse the port definitions from argparse.
    """
    p_out = {}
    for p in ports:
        p_split = p.split(":")
        host_side = p_split[0]
        c_side = p_split[1]
        p_out[c_side] = host_side
    return p_out

def parse_env(env_in):
    env_out = {}
    reg = re.compile(r'^(?P<var_name>[A-Z0-9_\-]+)=(?P<var_value>.+)$')
    env_all = env_in.split(" ")[1:]
    for e in env_all:
        match = reg.match(e.lstrip())
        if not match:
            raise ValueError("Invalid Environment variable supplied.")

        var_name = match.group("var_name")
        var_value = match.group("var_value")
        env_out[var_name] = var_value
        
    return env_out