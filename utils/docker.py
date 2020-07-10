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
