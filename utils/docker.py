import os
import re


def split_image(image_raw):
    raw_split = image_raw.split(":")  # First split by the colon...
    tag = None
    if len(raw_split) == 3:
        # Then split the remainder by the forw. slash (/).
        # The first element is the port.
        port = raw_split[1].split("/")[0]
        img_name = "{repo}:{port}/{image}".format(
            repo=raw_split[0],
            port=port,
            # The image name is the rest of the remainder, minus the port, so...
            # Split by /. The first element is the port, don't use it. Join the rest with slashes.
            image="/".join(raw_split[1].split("/")[1:])
        )
    else:
        img_name = raw_split[0]
    try:
        # The last element of the splitted raw is the tag.
        tag = raw_split[-1]
    except IndexError:
        pass

    return img_name, tag


def parse_volumes(volumes, debug=False):
    """
    Parse volume definitions from argparse.
    """
    v_out = {}
    for v in volumes:
        if v == "":
            continue

        v_split = v.split(":")
        host_side = v_split[0].strip()

        if not os.path.isdir(host_side):
            raise FileNotFoundError(
                "Error: Directory {} on the host side doesn't exist."
                .format(host_side)
            )

        c_side = v_split[1].strip()
        mode = "rw"
        try:
            mode = v_split[2].strip()
            if mode not in ["rw", "ro"]:
                raise ValueError(
                    "Volume mode incorrect. Accepted values: rw, ro"
                )
        except IndexError:
            pass

        v_out[host_side] = {"bind": c_side, "mode": mode}
        if debug:
            print(
                "Binding directory '{}' to host's directory '{}'. Mode: {}"
                .format(c_side, host_side, mode)
                )
    return v_out


def parse_ports(ports, debug=False):
    """
    Parse the port definitions from argparse.
    """
    p_out = {}
    for p in ports:
        if p == "":
            continue

        p_split = p.lstrip().split(":")
        host_side = int(p_split[0])
        c_side = int(p_split[1])
        p_out[c_side] = host_side
        if debug:
            print(
                "Exposing port {} to host's port {}"
                .format(c_side, host_side)
            )
    return p_out


def parse_env(env_in):
    env_out = {}
    reg = re.compile(r'^(?P<var_name>[A-Z0-9_\-]+)=(?P<var_value>.+)$')
    env_all = env_in.split(" ")
    for e in env_all:
        if e == "":
            continue

        match = reg.match(e.lstrip())
        if not match:
            raise ValueError("Invalid Environment variable supplied.")

        var_name = match.group("var_name")
        var_value = match.group("var_value")
        env_out[var_name] = var_value

    return env_out


def parse_restart(rp, debug=False):
    if rp not in ["always", "on-failure"]:
        raise ValueError(
            "Invalid restart policy. Only 'on-failure' and 'always' are \
            supported."
            )
    if debug:
        print("'{}' restart policy will be applied.".format(rp))
    rp_out = {"Name": rp}
    if rp == "on-failure":
        rp_out["MaximumRetryCount"] = 5
    return rp_out
