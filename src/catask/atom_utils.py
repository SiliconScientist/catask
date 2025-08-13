from ase import Atoms


def remove_via_tags(atoms: Atoms, adsorbate_tag: int = 2):
    tags = atoms.get_tags()
    mask = tags != adsorbate_tag
    new_atoms = atoms[mask]
    return new_atoms
