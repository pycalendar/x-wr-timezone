"""Check PyPI project links."""

import setup


def test_funding_links_are_exposed_to_pypi():
    """Funding links should be included in package metadata."""
    project_urls = setup.SETUPTOOLS_METADATA["project_urls"]

    assert project_urls["GitHub Sponsors"] == "https://github.com/sponsors/niccokunzmann"
    assert project_urls["Open Collective"] == "https://opencollective.com/open-web-calendar/"
    assert project_urls["Polar"] == "https://polar.sh/niccokunzmann"
    assert project_urls["thanks.dev"] == "https://thanks.dev"
    assert (
        project_urls["Tidelift"]
        == "https://tidelift.com/lifter/search/pypi/x-wr-timezone"
    )
