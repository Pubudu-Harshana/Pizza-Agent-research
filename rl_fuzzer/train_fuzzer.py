import os
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from pizza_env import PizzaEnv, ACTIONS

# Set up paths
MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
os.makedirs(MODELS_DIR, exist_ok=True)
MODEL_PATH = os.path.join(MODELS_DIR, "attacker_model")

def main():
    print("Setting up PizzaEnv...")
    env = PizzaEnv()
    print(f"Action space: {len(ACTIONS)} payloads loaded")
    
    # print("Checking environment compatibility...")
    # check_env(env)
    
    print("Initializing PPO Agent...")
    # Use PPO, the standard reliable RL algorithm
    model = PPO("MlpPolicy", env, verbose=1, learning_rate=0.001)
    
    # Increased from 20 to 2000 — mock mode makes this fast
    TIMESTEPS = 2000
    
    print(f"Training for {TIMESTEPS} timesteps (this may take a while)...")
    model.learn(total_timesteps=TIMESTEPS)
    
    print("Saving model...")
    model.save(MODEL_PATH)
    
    env.close()
    print(f"Training complete. Model saved to {MODEL_PATH}.zip")

if __name__ == "__main__":
    main()
