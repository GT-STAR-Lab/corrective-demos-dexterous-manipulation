# TODO for HRI 2022

## Experiment setup
1. 1500 random initial states.
2. Divide this into 500 states for training (Training set) and 1000 states for testing (Test set).
3. Sample 30 initial states from the Training set for collecting demonstrations. (**User Study Phase I**)
4. Train policies using 10, 15, 20 and 30 demonstrations called p_10, p_15, p_20 and p_30 respectively.
5. Rollout these policies to collect failure cases on Training set (Scenario 1) and Testing set (Scenario 2). We will collect 20 for p_10, 
15 for p_15, and 10 for p_20, for each scenario. 
7. Collect corrective demonstrations for all the failure cases across the two scenarios (20+15+10+0 x 2). (**User Study Phase II**) We can try optimizing unique 
initial states for failure cases so the total corrective demonstrations are reduced.
6. Retrain the policies with both demonstrations and corrections (p_10_20_s1, p_15_15_s1, p_20_10_s1, p_10_20_s2, p_15_15_s2, p_20_10_s2).
7. Rollout all 10 policies on Test set and analyze.

## Jan 22 (Saturday) completion
1. Training sampling and testing sampling, collecting 1500 samples, diving into 500 (train) and 1000 (test), storing samples in seperate files
2. Logic to read 30, 500, 1000 samples from relevant files when initializing states using the --sampling_mode=['demos', 'failures', 'test'] flag
* CHANGE SCRIPTS TO USE THIS NEW FLAG
3. Sorting failures by worst reward for the failure collection
* CHANGE SCRIPTS TO REFLECT THIS (# of rollouts, episodes (500-failures, 1000-test), added flags for number of failures to collect)
4. Have demos end automatically with 25 consecutive frames at the target, repeated logic for the failure collection
* CHANGE LEAP MOTION RANGE TO BE WITHIN BOUNDS