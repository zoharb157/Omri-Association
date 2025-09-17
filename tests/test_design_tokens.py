from ui.design_system.modern_tokens import ModernDesignSystem


def test_spacing_aliases_exist():
    base_keys = ["0", "1", "2", "3", "4", "5", "6", "8", "10", "12", "16", "20", "24", "32"]
    for key in base_keys:
        alias = f"space_{key}"
        assert ModernDesignSystem.SPACING[key] == ModernDesignSystem.SPACING[alias]


def test_radius_aliases_exist():
    for key in ["none", "sm", "md", "lg", "xl", "2xl", "full"]:
        alias = f"radius_{key}"
        assert ModernDesignSystem.BORDER_RADIUS[key] == ModernDesignSystem.BORDER_RADIUS[alias]


def test_shadow_aliases_exist():
    for key in ["none", "sm", "md", "lg", "xl"]:
        alias = f"shadow_{key}"
        assert ModernDesignSystem.SHADOWS[key] == ModernDesignSystem.SHADOWS[alias]

def test_legacy_design_system_maps_to_modern():
    from ui.design_tokens import DesignSystem

    assert DesignSystem.COLORS["primary"] == ModernDesignSystem.COLORS["primary"]
    assert DesignSystem.SPACING["sm"] == ModernDesignSystem.SPACING["space_2"]
    assert DesignSystem.BORDER_RADIUS["md"] == ModernDesignSystem.BORDER_RADIUS["radius_md"]
