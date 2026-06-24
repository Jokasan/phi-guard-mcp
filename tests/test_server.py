from phi_guard_mcp.server import _package_version


def test_package_version_fallback() -> None:
    assert _package_version()
