import optparse

from pip._internal.network.session import PipSession

def pip_self_version_check(session: PipSession, options: optparse.Values) -> None:
  # we're being naughty, so don't bother checking pip versions
  pass

print("PoC: Wheel-of-Despair code execution.")

