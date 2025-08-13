# test_remove_via_tags.py
import numpy as np
from ase import Atoms

from catask.atom_utils import remove_via_tags


def make_atoms():
    # H2O with an extra H, tagged: H(1), O(2), H(1), H(2)
    atoms = Atoms(
        "H2OH",
        positions=[
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 1.0],
            [0.9, 0.0, 0.0],
            [2.0, 0.0, 0.0],
        ],
        cell=[5, 5, 5],
        pbc=[True, True, True],
    )
    atoms.set_tags([1, 2, 1, 2])
    return atoms


def test_basic_filtering(adsorbate_tag=2):
    atoms = make_atoms()
    out = remove_via_tags(atoms, adsorbate_tag=adsorbate_tag)

    # All kept tags must be != adsorbate_tag
    assert np.all(out.get_tags() != adsorbate_tag)

    # Count should match the number of non-adsorbate_tag tags in the input
    expected_len = int((atoms.get_tags() != adsorbate_tag).sum())
    assert len(out) == expected_len


def test_preserves_geometry_and_cell():
    atoms = make_atoms()
    # Keep atoms with tag 1, which are indices 0 and 2
    expected_positions = atoms.get_positions()[[0, 2]]
    expected_cell = atoms.cell.copy()
    expected_pbc = atoms.pbc.copy()

    out = remove_via_tags(atoms, adsorbate_tag=2)

    np.testing.assert_allclose(out.get_positions(), expected_positions)
    np.testing.assert_allclose(out.cell.array, expected_cell.array)
    assert np.all(out.pbc == expected_pbc)


def test_no_matching_tags_returns_all():
    atoms = make_atoms()
    # Choose a tag that is not present
    out = remove_via_tags(atoms, adsorbate_tag=99)
    assert len(out) == len(atoms)
    # Not the same object, but same contents
    assert out is not atoms
    np.testing.assert_allclose(out.get_positions(), atoms.get_positions())
    assert out.get_chemical_symbols() == atoms.get_chemical_symbols()
    np.testing.assert_array_equal(out.get_tags(), atoms.get_tags())


def test_all_matching_tags_returns_empty():
    atoms = make_atoms()
    atoms.set_tags([2, 2, 2, 2])
    out = remove_via_tags(atoms, adsorbate_tag=2)
    assert len(out) == 0


def test_input_is_unchanged():
    atoms = make_atoms()
    symbols_before = atoms.get_chemical_symbols()
    tags_before = atoms.get_tags().copy()
    pos_before = atoms.get_positions().copy()

    _ = remove_via_tags(atoms, adsorbate_tag=2)

    # Original must be unchanged
    assert atoms.get_chemical_symbols() == symbols_before
    np.testing.assert_array_equal(atoms.get_tags(), tags_before)
    np.testing.assert_allclose(atoms.get_positions(), pos_before)
