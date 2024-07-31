def pytest_runtest_makereport(item, call):
    if not item.config.getoption("capture"):
        input("Press Enter to continue to the next test case...")
