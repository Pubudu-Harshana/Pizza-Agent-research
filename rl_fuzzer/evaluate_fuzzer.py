import time
import os
from stable_baselines3 import PPO
from pizza_env import PizzaEnv, ACTIONS

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "attacker_model")

def main():
    if not os.path.exists(MODEL_PATH + ".zip"):
        print(f"Model not found at {MODEL_PATH}.zip. Please run train_fuzzer.py first.")
        return

    print("Loading Attacker Model...")
    model = PPO.load(MODEL_PATH)
    
    print("Setting up PizzaEnv...")
    env = PizzaEnv()
    
    obs, info = env.reset()
    
    print("\n--- BEGIN EVALUATION ---")
    
    for i in range(15):  # match the new 15-turn episode horizon
        print(f"\n[Turn {i+1}] Current State Obs: {obs}")
        
        # RL Agent decides what to do based on the state
        action, _states = model.predict(obs, deterministic=True)
        action_idx = int(action)
        
        print(f"🤖 RL Attacker chose action: {ACTIONS[action_idx]}")
        
        # Take step
        obs, reward, done, truncated, info = env.step(action_idx)
        
        print(f"💰 Reward received: {reward}")
        print(f"🔎 Leakage detected: {info.get('leakage', False)}  |  Response length: {info.get('resp_len', 0)} chars")

        # Print a snippet of the agent's response to show what happened
        resp = info['output']
        # Extract just the latest Agent response
        if "Agent:" in resp:
            agent_text = resp.split("Agent:")[-1].split("\xe2\x94\x94")[0].strip()
            print(f"🍕 Target System Response:\n{agent_text}")
        else:
            print(f"🍕 Target System Output (raw):\n{resp}")
            
        if done:
            print("\n🚨 Episode finished (Vulnerability found or max turns reached)!")
            break
            
    env.close()
    print("--- EVALUATION COMPLETE ---")

if __name__ == "__main__":
    main()
