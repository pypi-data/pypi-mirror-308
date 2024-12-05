from mx_stream_core.config.delta import delta_path, dims_delta_path


def get_delta_path(table_name=None) -> str:
    if table_name is not None:
        return f"{delta_path}/{table_name}"
    print("path: ", delta_path)
    return delta_path

def get_dims_delta_path(table_name=None) -> str:
    if table_name is not None:
        return f"{dims_delta_path}/{table_name}"
    print("path: ", dims_delta_path)
    return dims_delta_path