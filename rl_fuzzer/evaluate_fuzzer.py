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
    vulnerabilities = []  # Collect all found vulnerabilities
    
    for i in range(15):  # match the new 15-turn episode horizon
        print(f"\n[Turn {i+1}] Current State Obs: {obs}")
        
        # RL Agent decides what to do based on the state
        # deterministic=False → sample from the policy distribution,
        # producing diverse payloads instead of always picking one best action.
        action, _states = model.predict(obs, deterministic=False)
        action_idx = int(action)
        
        print(f"RL Attacker chose action: {ACTIONS[action_idx]}")
        
        # Take step
        obs, reward, done, truncated, info = env.step(action_idx)
        
        print(f"Reward received: {reward}")
        print(f"Leakage detected: {info.get('leakage', False)}  |  Response length: {info.get('resp_len', 0)} chars")

        # Collect vulnerability if one was found
        vuln = info.get("vuln_type")
        if vuln:
            vulnerabilities.append({
                "turn":    i + 1,
                "payload": ACTIONS[action_idx],
                "type":    vuln,
            })

        # Print a snippet of the agent's response to show what happened
        resp = info['output']
        # Extract just the latest Agent response
        if "Agent:" in resp:
            agent_text = resp.split("Agent:")[-1].split("\xe2\x94\x94")[0].strip()
            print(f"Target System Response:\n{agent_text}")
        else:
            print(f"Target System Output (raw):\n{resp}")
            
        if done:
            print("\nEpisode finished (Vulnerability found or max turns reached)!")
            break
            
    env.close()

    # ── Vulnerability Report ──────────────────────────────────────────
    sep = "-" * 50
    print(f"\n{sep}")
    print("  VULNERABILITY REPORT")
    print(sep)
    if vulnerabilities:
        for idx, v in enumerate(vulnerabilities, 1):
            print(f"  [{idx}]  Turn {v['turn']}  |  Type: {v['type']}")
            print(f"       Payload : {v['payload']}")
            print()
        print(f"  Total vulnerabilities found: {len(vulnerabilities)}")
    else:
        print("  No vulnerabilities detected this episode.")
    print(sep)
    print("\n--- EVALUATION COMPLETE ---")

if __name__ == "__main__":
    main()
