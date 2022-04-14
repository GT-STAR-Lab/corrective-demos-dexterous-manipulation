"""
Wrapper around a gym env that provides convenience functions
"""

import pickle
import gym
import numpy as np
import copy


class EnvSpec(object):
    def __init__(self, obs_dim, act_dim, horizon):
        self.observation_dim = obs_dim
        self.action_dim = act_dim
        self.horizon = horizon


class GymEnv(object):
    def __init__(self, env, env_kwargs=None,
                 obs_mask=None, act_repeat=1, 
                 *args, **kwargs):
    
        # get the correct env behavior
        if type(env) == str:
            env = gym.make(env)
        elif isinstance(env, gym.Env):
            env = env
        elif callable(env):
            env = env(**env_kwargs)
        else:
            print("Unsupported environment format")
            raise AttributeError

        self.env = env
        self.env_id = env.spec.id
        self.act_repeat = act_repeat

        try:
            self._horizon = env.spec.max_episode_steps
        except AttributeError:
            self._horizon = env.spec._horizon

        assert self._horizon % act_repeat == 0
        self._horizon = self._horizon // self.act_repeat

        try:
            self._action_dim = self.env.env.action_dim
        except AttributeError:
            self._action_dim = self.env.action_space.shape[0]

        try:
            self._observation_dim = self.env.env.obs_dim
        except AttributeError:
            self._observation_dim = self.env.observation_space.shape[0]

        # Specs
        self.spec = EnvSpec(self._observation_dim, self._action_dim, self._horizon)

        # obs mask
        self.obs_mask = np.ones(self._observation_dim) if obs_mask is None else obs_mask

    @property
    def action_dim(self):
        return self._action_dim

    @property
    def observation_dim(self):
        return self._observation_dim

    @property
    def observation_space(self):
        return self.env.observation_space

    @property
    def action_space(self):
        return self.env.action_space

    @property
    def horizon(self):
        return self._horizon

    def reset(self, seed=None, mode='training', samples_filename=None, same_pos=False):
        try:
            self.env._elapsed_steps = 0
            return self.env.env.reset_model(seed=seed, mode=mode, samples_filename=samples_filename, same_pos=same_pos)
        except Exception as e:
            print("Exception in gym_env reset()", e)
            if seed is not None:
                self.set_seed(seed)
            return self.env.reset()

    def reset_model(self, seed=None):
        # overloading for legacy code
        return self.reset(seed)

    def step(self, action):
        action = action.clip(self.action_space.low, self.action_space.high)
        if self.act_repeat == 1: 
            obs, cum_reward, done, ifo = self.env.step(action)
        else:
            cum_reward = 0.0
            for i in range(self.act_repeat):
                obs, reward, done, ifo = self.env.step(action)
                cum_reward += reward
                if done: break
        return self.obs_mask * obs, cum_reward, done, ifo

    def render(self):
        try:
            self.env.env.mujoco_render_frames = True
            self.env.env.mj_render()
        except:
            self.env.render()

    def set_seed(self, seed=123):
        try:
            self.env.seed(seed)
        except AttributeError:
            self.env._seed(seed)

    def get_obs(self):
        try:
            return self.obs_mask * self.env.env.get_obs()
        except:
            return self.obs_mask * self.env.env._get_obs()

    def get_env_infos(self):
        try:
            return self.env.env.get_env_infos()
        except:
            return {}

    # ===========================================
    # Trajectory optimization related
    # Envs should support these functions in case of trajopt

    def get_env_state(self):
        try:
            return self.env.env.get_env_state()
        except:
            raise NotImplementedError

    def set_env_state(self, state_dict):
        try:
            self.env.env.set_env_state(state_dict)
        except:
            raise NotImplementedError

    def real_env_step(self, bool_val):
        try:
            self.env.env.real_step = bool_val
        except:
            raise NotImplementedError

    # ===========================================

    def visualize_policy(self, policy, horizon=1000, num_episodes=1, mode='exploration', **kwargs):
        success_threshold = 25
        success_run = 0
        episodes = []
        total_score = 0.0
        unsuccessful_rollout_states = []
        ep = 0
        while ep < num_episodes:
            # print("Episode %d" % ep)
            o = self.reset(samples_filename=kwargs['samples_filename'])
            d = False
            t = 0
            score = 0.0
            episode_data = {
                'init_state_dict': copy.deepcopy(self.get_env_state()),
                'actions': [],
                'observations': [],
                'rewards': [],
                'goal_achieved': [],
                'cumulative_reward': 0
            }
            while t < horizon and d is False:
                episode_data['observations'].append(o)
                a = policy.get_action(o)[0] if mode == 'exploration' else policy.get_action(o)[1]['evaluation']
                o, r, d, goal_achieved = self.step(a)
                episode_data['actions'].append(a)
                episode_data['rewards'].append(r)
                episode_data['cumulative_reward'] += r
                episode_data['goal_achieved'].append(goal_achieved['goal_achieved'])
                
                # iterate the success run if the ball is at the target
                success_run = success_run + 1 if goal_achieved['goal_achieved'] else 0
                
                score = score + r
                if not kwargs['record']:
                    self.render()
                t = t+1
            episodes.append(copy.deepcopy(episode_data))
            total_score += score
            success = success_run >= success_threshold
            # print("Episode score = %f, Success = %d" % (score, success))
            if not success:
                unsuccessful_rollout_states.append((episode_data['cumulative_reward'], copy.deepcopy(episode_data['init_state_dict'])))
            ep += 1
        print("Average score = %f" % (total_score / len(episodes)))
        successful_episodes = list(filter(lambda episode: sum(episode['goal_achieved']) > success_threshold, episodes))
        print("Success rate = %f" % (len(successful_episodes) / len(episodes)))
        if len(unsuccessful_rollout_states) and kwargs['failure_file_path']:
            # get the worst failure cases
            worst_unsuccessful_rollout_states = [x[1] for x in sorted(unsuccessful_rollout_states)[:kwargs['num_failures']]]
            with open(kwargs['failure_file_path'], 'wb') as failure_cases:
                pickle.dump(worst_unsuccessful_rollout_states, failure_cases)

    def visualize_policy_from_demos(self, policy, demos, horizon=1000, num_episodes=1, mode='exploration'):
        for idx in range(len(demos)):
            print("Episode %d" % idx)
            self.reset()
            self.set_env_state(demos[idx]['init_state_dict'])
            o = self.get_obs()
            d = False
            t = 0
            score = 0.0
            while t < horizon and d is False:
                a = policy.get_action(o)[0] if mode == 'exploration' else policy.get_action(o)[1]['evaluation']
                o, r, d, _ = self.step(a)
                score = score + r
                self.render()
                t = t+1
            print("Episode score = %f" % score)

    def evaluate_policy(self, policy,
                        num_episodes=5,
                        horizon=None,
                        gamma=1,
                        visual=False,
                        percentile=[],
                        get_full_dist=False,
                        mean_action=False,
                        init_env_state=None,
                        terminate_at_done=True,
                        seed=123):

        self.set_seed(seed)
        horizon = self._horizon if horizon is None else horizon
        mean_eval, std, min_eval, max_eval = 0.0, 0.0, -1e8, -1e8
        ep_returns = np.zeros(num_episodes)

        for ep in range(num_episodes):
            self.reset()
            if init_env_state is not None:
                self.set_env_state(init_env_state)
            t, done = 0, False
            while t < horizon and (done == False or terminate_at_done == False):
                self.render() if visual is True else None
                o = self.get_obs()
                a = policy.get_action(o)[1]['evaluation'] if mean_action is True else policy.get_action(o)[0]
                o, r, done, _ = self.step(a)
                ep_returns[ep] += (gamma ** t) * r
                t += 1

        mean_eval, std = np.mean(ep_returns), np.std(ep_returns)
        min_eval, max_eval = np.amin(ep_returns), np.amax(ep_returns)
        base_stats = [mean_eval, std, min_eval, max_eval]

        percentile_stats = []
        for p in percentile:
            percentile_stats.append(np.percentile(ep_returns, p))

        full_dist = ep_returns if get_full_dist is True else None

        return [base_stats, percentile_stats, full_dist]
