from catask.config import get_config
from ase.io import read, write

from catask.atom_utils import remove_via_tags


def main():
    cfg = get_config()
    atoms_list = read("data/oc22_ooh.extxyz", index=":")
    bare_surfaces = [remove_via_tags(atoms) for atoms in atoms_list]
    write("data/oc22_ooh_bare.extxyz", bare_surfaces)


if __name__ == "__main__":
    main()
