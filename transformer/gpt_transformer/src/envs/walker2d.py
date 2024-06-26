import numpy as np
from gym import utils
import mujoco_py
import pyrootutils

path = pyrootutils.find_root(search_from=__file__, indicator=".project-root")
pyrootutils.set_root(path = path,
                     project_root_env_var = True,
                     dotenv = True,
                     pythonpath = True)

import transformer.gpt_transformer.src.envs.mujoco_env as mujoco_env



# class Walker2dEnv(mujoco_env.MujocoEnv, utils.EzPickle):
#     def __init__(self):
#         mujoco_env.MujocoEnv.__init__(self, "walker2d.xml", 4)
#         utils.EzPickle.__init__(self)

#     def step(self, a):
#         posbefore = self.sim.data.qpos[0]
#         self.do_simulation(a, self.frame_skip)
#         posafter, height, ang = self.sim.data.qpos[0:3]
#         alive_bonus = 1.0
#         reward = (posafter - posbefore) / self.dt
#         reward += alive_bonus
#         reward -= 1e-3 * np.square(a).sum()
#         done = not (height > 0.8 and height < 2.0 and ang > -1.0 and ang < 1.0)
#         ob = self._get_obs()
#         return ob, reward, done, {}

#     def _get_obs(self):
#         qpos = self.sim.data.qpos
#         qvel = self.sim.data.qvel
#         return np.concatenate([qpos[1:], np.clip(qvel, -10, 10)]).ravel()

#     def reset_model(self):
#         self.set_state(
#             self.init_qpos
#             + self.np_random.uniform(low=-0.005, high=0.005, size=self.model.nq),
#             self.init_qvel
#             + self.np_random.uniform(low=-0.005, high=0.005, size=self.model.nv),
#         )
#         return self._get_obs()

#     def viewer_setup(self):
#         self.viewer.cam.trackbodyid = 2
#         self.viewer.cam.distance = self.model.stat.extent * 0.5
#         self.viewer.cam.lookat[2] = 1.15
#         self.viewer.cam.elevation = -20



class ExtendedWalker2dEnv(mujoco_env.MujocoEnv, utils.EzPickle):
    def __init__(self):
        mujoco_env.MujocoEnv.__init__(self, "walker2d.xml", 4)
        utils.EzPickle.__init__(self)

    def step(self, a):
        posbefore = self.sim.data.qpos[0]
        self.do_simulation(a, self.frame_skip)
        posafter, height, ang = self.sim.data.qpos[0:3]
        alive_bonus = 1.0
        reward = (posafter - posbefore) / self.dt
        reward += alive_bonus
        reward -= 1e-3 * np.square(a).sum()
        done = not (height > 0.8 and height < 2.0 and ang > -1.0 and ang < 1.0)
        ob = self._get_obs()
        return ob, reward, done, {}

    def _get_obs(self):
        qpos = self.sim.data.qpos
        qvel = self.sim.data.qvel
        return np.concatenate([qpos[1:], np.clip(qvel, -10, 10)]).ravel()

    def reset_model_with_state(self, state):
        
        qpos = state[:self.model.nq-1]
        qvel = state[self.model.nq-1:]

        qvel = np.clip(qvel, -10, 10)

        old_state = self.sim.get_state()
        xpos = old_state.qpos[0]
        qpos = np.concatenate([[xpos], qpos])

        new_state = mujoco_py.MjSimState(
            old_state.time, qpos, qvel, old_state.act, old_state.udd_state
        )

        self.sim.set_state(new_state)
        self.sim.forward()

    def reset_model(self):
        self.set_state(
            self.init_qpos
            + self.np_random.uniform(low=-0.005, high=0.005, size=self.model.nq),
            self.init_qvel
            + self.np_random.uniform(low=-0.005, high=0.005, size=self.model.nv),
        )
        return self._get_obs()

    def viewer_setup(self):
        self.viewer.cam.trackbodyid = 2
        self.viewer.cam.distance = self.model.stat.extent * 0.5
        self.viewer.cam.lookat[2] = 1.15
        self.viewer.cam.elevation = -20
