import pytest
from mtqdm import mtqdm

def test_mtqdm_initialization():
    # Test with different input types
    progress_range = mtqdm(range(10))
    assert progress_range.total == 10
    assert progress_range.n == 0

    progress_list = mtqdm([1, 2, 3, 4, 5])
    assert progress_list.total == 5
    assert progress_list.n == 0

    # Test with explicit total
    progress_explicit = mtqdm(range(100), total=50)
    assert progress_explicit.total == 50
    assert progress_explicit.n == 0

def test_mtqdm_display_modes():
    # Test all display mode attributes exist
    display_modes = ['PERCENTAGE', 'BAR', 'TIME']
    for mode in display_modes:
        assert hasattr(mtqdm.DisplayMode, mode)
        assert isinstance(getattr(mtqdm.DisplayMode, mode), mtqdm.DisplayMode)

    # Test display modes are unique
    mode_values = [mode.value for mode in mtqdm.DisplayMode]
    assert len(mode_values) == len(set(mode_values)), "Display modes should have unique values"

def test_mtqdm_iteration():
    test_list = list(range(5))
    progress = mtqdm(test_list)
    
    # Test iteration works correctly
    collected = []
    for item in progress:
        collected.append(item)
        print(f"Current item: {item}")
        print(f"Progress n: {progress.n}")
        print(f"Collected length: {len(collected)}")
        assert progress.n == len(collected), f"Counter mismatch at item {item}: n={progress.n}, collected={len(collected)}"
    
    assert collected == test_list, f"Final collection mismatch: {collected} != {test_list}"
    assert progress.n == len(test_list), f"Final counter mismatch: {progress.n} != {len(test_list)}"

@pytest.mark.parametrize("total,expected", [
    (10, 10),
    (None, 5),
    (3, 3),
])
def test_mtqdm_total_parameter(total, expected):
    # Test different total parameter scenarios
    progress = mtqdm(range(5), total=total)
    assert progress.total == expected
