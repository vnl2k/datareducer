import cProfile, pstats

from datareducer.reducers import npArray, pyArray

def profile_npArray(m, message):
  print(message)
  pr = cProfile.Profile()
  pr.enable()
  shader = m().setLimits(0, 5000000, 5).init()

  for i in range(1, 1000000, 1):
    shader.apply(i)
  pr.disable()
  pstats.Stats(pr).strip_dirs().sort_stats('tottime').print_stats()

def profile_pyArray(m, message):
  print(message)
  pr = cProfile.Profile()
  pr.enable()
  shader = m().setLimits(0, 5000000, 5).init()

  for i in range(1, 1000000, 1):
    shader.apply(i, lambda prev, _: prev + 1)
  pr.disable()
  pstats.Stats(pr).strip_dirs().sort_stats('tottime').print_stats()

profile_npArray(npArray, 'profile shader')
profile_pyArray(pyArray, 'profile shaderArray')
