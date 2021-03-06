import os


def safe_mkdir(sdc_home: str, relative_path: str=None) -> None:
    '''
    Safely create directories while checking permissions along the way.
    '''
    check_dir_permissions(sdc_home)

    if not relative_path:
        return

    full_path = os.path.join(sdc_home, relative_path)
    if not full_path == os.path.abspath(full_path):
        raise ValueError('Path is not absolute: {}'.format(full_path))

    path_components = split_path(relative_path)

    path_so_far = sdc_home
    for component in path_components:
        path_so_far = os.path.join(path_so_far, component)
        check_dir_permissions(path_so_far)
        os.makedirs(path_so_far, 0o0700, exist_ok=True)


def check_dir_permissions(dir_path: str) -> None:
    '''
    Check that a directory has ``700`` as the final 3 bytes. Raises a
    ``RuntimeError`` otherwise.
    '''
    if os.path.exists(dir_path):
        stat_res = os.stat(dir_path).st_mode
        masked = stat_res & 0o777
        if masked & 0o077:
            raise RuntimeError('Unsafe permissions ({}) on {}'
                               .format(oct(stat_res), dir_path))


def split_path(path: str) -> list:
    out = []

    while path:
        path, tail = os.path.split(path)
        out.append(tail)

    out.reverse()
    return out
