from gym.envs.registration import register

register(
    id='Connect5-v0',
    entry_point='connect5.envs:Connect5Env',
)


