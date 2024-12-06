
def test_version():
  import dominix
  version = '2.0.0'
  assert dominix.version == version
  assert dominix.__version__ == version

#780f21db-b9b0-4faf-bc19-80e4e8ce69d8