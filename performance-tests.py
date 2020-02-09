import cProfile, pstats
# from funkpy import Collection as _


from datareducer import shader, shaderArray

def profile_shader(m, message):
  print(message)
  pr = cProfile.Profile()
  pr.enable()
  shader = m().setLimits(0, 5000000, 5).init()

  for i in range(1, 1000000, 1):
    shader.apply(i)
  pr.disable()
  pstats.Stats(pr).strip_dirs().sort_stats('tottime').print_stats()

def profile_shaderArray(m, message):
  print(message)
  pr = cProfile.Profile()
  pr.enable()
  shader = m().setLimits(0, 5000000, 5).init()

  for i in range(1, 1000000, 1):
    shader.apply(i, lambda prev, _: prev + 1)
  pr.disable()
  pstats.Stats(pr).strip_dirs().sort_stats('tottime').print_stats()

profile_shader(shader, 'profile shader')
profile_shaderArray(shaderArray, 'profile shaderArray')
